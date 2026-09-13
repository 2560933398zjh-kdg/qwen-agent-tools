# 短信验证码登录（鸿蒙课程对接版）

基于 Flask 的验证码登录示例，流程与鸿蒙端一致：

```
获取图形验证码 → 校验图形验证码 → 发送短信验证码 → 手机号+短信登录 → 保存用户信息
```

## 目录结构

```
userProject/
├── app.py
├── requirements.txt
├── templates/index.html
└── users.json          # 运行后自动生成
```

## 接口文档

完整接口说明见 **[API.md](API.md)**，包含请求参数、响应示例、错误码及 cURL 测试命令。

## 接口一览

| 步骤 | 接口 | 说明 |
|------|------|------|
| 1 | `GET /code/graphic?phone=&bizType=1&timestamp=` | 返回 PNG 图形验证码 |
| 2 | `POST /code/graphic/check` | 校验图形验证码 |
| 3 | `POST /code/sms/send` | 发送短信验证码（需先通过图形校验） |
| 4 | `POST /user/login/verifyCode` | 手机号 + 短信验证码登录 |
| - | `POST /user/login/passwd` | 账号密码登录 |
| - | `GET /user/me` | 获取我的信息（需登录态） |
| - | `POST /user/logout` | 退出登录 |

**演示账号（密码登录）：**

| 手机号 | 密码 | 昵称 |
|--------|------|------|
| 120666666673 | 888itcast.CN764%... | 测试学员 |

响应格式：`{ code, msg, resTime, result, tips }`，`code === 200` 为成功。

登录成功 `result` 结构与鸿蒙 `LoginInfoResponse` 一致：

```json
{
  "accessToken": "...",
  "avatar": "",
  "nickname": "用户1234",
  "renewalToken": "..."
}
```

## 运行

```bash
pip install -r requirements.txt
python app.py
```

浏览器访问 http://127.0.0.1:5000

鸿蒙端将 `BASE_URL` 改为电脑局域网 IP，例如 `http://192.168.1.100:5000`。

## 说明

- 图形验证码、短信验证码仅打印在服务端控制台，不会出现在接口返回体中。
- 用户信息持久化到 `users.json`，Web 端登录信息存 `localStorage`。
