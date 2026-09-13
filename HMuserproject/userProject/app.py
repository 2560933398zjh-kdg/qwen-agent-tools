import io
import json
import os
import random
import time
import uuid

from flask import Flask, jsonify, render_template, request, send_file, session
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-me"

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")

CODE_STORE = {}
GRAPHIC_STORE = {}

CODE_TTL = 300
GRAPHIC_TTL = 300
BIZ_PHONE_LOGIN = "1"

DEMO_ACCOUNTS = {
    "120666666673": {
        "passwd": "888itcast.CN764%...",
        "nickname": "测试学员",
        "avatar": "/static/cat.jpg",
    },
}


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def ensure_demo_users():
    users = load_users()
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    changed = False
    for phone, info in DEMO_ACCOUNTS.items():
        if phone not in users:
            users[phone] = {
                "phone": phone,
                "passwd": info["passwd"],
                "nickname": info["nickname"],
                "avatar": info["avatar"],
                "created_at": now,
                "last_login": now,
                "accessToken": uuid.uuid4().hex,
                "renewalToken": uuid.uuid4().hex,
            }
            changed = True
        else:
            for key in ("passwd", "nickname", "avatar"):
                if info.get(key) and users[phone].get(key) != info[key]:
                    users[phone][key] = info[key]
                    changed = True
    if changed:
        save_users(users)


ensure_demo_users()


def service_ok(result=None, msg="success"):
    return jsonify({
        "code": 200,
        "msg": msg,
        "resTime": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "result": result,
        "tips": "",
    })


def service_fail(msg, code=300):
    return jsonify({
        "code": code,
        "msg": msg,
        "resTime": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "result": None,
        "tips": "",
    })


def graphic_key(phone, biz_type):
    return f"{phone}:{biz_type}"


def random_graphic_code(length=4):
    chars = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
    return "".join(random.choices(chars, k=length))


def generate_captcha_image(text):
    width, height = 108, 42
    image = Image.new("RGB", (width, height), (245, 247, 250))
    draw = ImageDraw.Draw(image)

    for _ in range(6):
        draw.line(
            (
                random.randint(0, width),
                random.randint(0, height),
                random.randint(0, width),
                random.randint(0, height),
            ),
            fill=(random.randint(160, 220), random.randint(160, 220), random.randint(160, 220)),
            width=1,
        )

    try:
        font = ImageFont.truetype("arial.ttf", 22)
    except OSError:
        font = ImageFont.load_default()

    char_width = width // (len(text) + 1)
    for i, ch in enumerate(text):
        x = char_width * (i + 1) - 8
        y = random.randint(6, 12)
        draw.text(
            (x, y),
            ch,
            fill=(random.randint(20, 80), random.randint(20, 80), random.randint(20, 80)),
            font=font,
        )

    for _ in range(40):
        draw.point((random.randint(0, width - 1), random.randint(0, height - 1)), fill=(180, 180, 180))

    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    return buf


def build_login_result(phone, users):
    user = users[phone]
    return {
        "accessToken": user.get("accessToken"),
        "avatar": user.get("avatar", ""),
        "nickname": user.get("nickname", f"用户{phone[-4:]}"),
        "renewalToken": user.get("renewalToken"),
    }


def save_or_update_user(phone):
    users = load_users()
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    token = uuid.uuid4().hex

    if phone in users:
        users[phone]["last_login"] = now
        users[phone]["accessToken"] = token
        users[phone]["renewalToken"] = uuid.uuid4().hex
    else:
        users[phone] = {
            "phone": phone,
            "nickname": f"用户{phone[-4:]}",
            "avatar": "",
            "passwd": "",
            "created_at": now,
            "last_login": now,
            "accessToken": token,
            "renewalToken": uuid.uuid4().hex,
        }

    save_users(users)
    return users


def complete_login(phone):
    users = save_or_update_user(phone)
    session["phone"] = phone
    return build_login_result(phone, users)


def get_current_phone():
    phone = session.get("phone")
    if phone:
        return phone

    token = (request.headers.get("Authorization") or "").strip()
    if not token:
        return None

    for p, user in load_users().items():
        if user.get("accessToken") == token:
            return p
    return None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/code/graphic")
def code_graphic():
    phone = (request.args.get("phone") or "").strip()
    biz_type = request.args.get("bizType", BIZ_PHONE_LOGIN)

    if not phone:
        return service_fail("手机号不能为空"), 400

    code = random_graphic_code()
    key = graphic_key(phone, biz_type)
    GRAPHIC_STORE[key] = {
        "code": code,
        "expire": time.time() + GRAPHIC_TTL,
        "passed": False,
    }

    print(f"[图形验证码] phone={phone}, code={code}")
    return send_file(generate_captcha_image(code), mimetype="image/png")


@app.route("/code/graphic/check", methods=["POST"])
def code_graphic_check():
    data = request.get_json(silent=True) or {}
    phone = (data.get("phone") or "").strip()
    biz_type = str(data.get("bizType", BIZ_PHONE_LOGIN))
    verify_code = (data.get("verifyCode") or "").strip().upper()

    key = graphic_key(phone, biz_type)
    record = GRAPHIC_STORE.get(key)
    if not record:
        return service_fail("请先获取图形验证码")
    if time.time() > record["expire"]:
        GRAPHIC_STORE.pop(key, None)
        return service_fail("图形验证码已过期，请刷新后重试")
    if verify_code != record["code"]:
        return service_fail("图形验证码错误")

    record["passed"] = True
    return service_ok(None, "success")


@app.route("/code/sms/send", methods=["POST"])
def code_sms_send():
    data = request.get_json(silent=True) or {}
    phone = (data.get("phone") or "").strip()
    biz_type = str(data.get("bizType", BIZ_PHONE_LOGIN))

    key = graphic_key(phone, biz_type)
    record = GRAPHIC_STORE.get(key)
    if not record or not record.get("passed"):
        return service_fail("请先完成图形验证码校验")

    if not (phone.isdigit() and len(phone) >= 11):
        return service_fail("请输入正确的手机号")

    code = "".join(random.choices("0123456789", k=6))
    CODE_STORE[phone] = {"code": code, "expire": time.time() + CODE_TTL}
    GRAPHIC_STORE.pop(key, None)

    print(f"[模拟短信] 向 {phone} 发送验证码：{code}")
    return service_ok(None, "短信验证码已发送")


@app.route("/user/login/verifyCode", methods=["POST"])
def user_login_verify_code():
    data = request.get_json(silent=True) or {}
    phone = (data.get("phone") or "").strip()
    verify_code = (data.get("verifyCode") or "").strip()

    record = CODE_STORE.get(phone)
    if not record:
        return service_fail("请先获取短信验证码")
    if time.time() > record["expire"]:
        CODE_STORE.pop(phone, None)
        return service_fail("短信验证码已过期，请重新获取")
    if verify_code != record["code"]:
        return service_fail("短信验证码错误")

    CODE_STORE.pop(phone, None)
    login_info = complete_login(phone)
    print(f"[验证码登录成功] phone={phone}")
    return service_ok(login_info, "登录成功")


@app.route("/user/login/passwd", methods=["POST"])
def user_login_passwd():
    data = request.get_json(silent=True) or {}
    phone = (data.get("phone") or "").strip()
    passwd = data.get("passwd") or ""

    if not phone or not passwd:
        return service_fail("手机号和密码不能为空")

    user = load_users().get(phone)
    if not user:
        return service_fail("账号不存在")
    if user.get("passwd") != passwd:
        return service_fail("密码错误")

    login_info = complete_login(phone)
    print(f"[密码登录成功] phone={phone}")
    return service_ok(login_info, "登录成功")


@app.route("/user/me")
def user_me():
    phone = get_current_phone()
    if not phone:
        return service_fail("未登录", code=401)

    user = load_users().get(phone)
    if not user:
        return service_fail("用户不存在")

    return service_ok({
        "avatar": user.get("avatar", ""),
        "nickname": user.get("nickname", ""),
    })


@app.route("/user/logout", methods=["POST"])
def user_logout():
    session.pop("phone", None)
    return service_ok(None, "已退出登录")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
