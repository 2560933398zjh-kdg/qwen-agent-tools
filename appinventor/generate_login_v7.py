# -*- coding: utf-8 -*-
"""
生成 LoginPage.aia - v7 (最终版)
基于对比分析结果修复：
1. BKY 用 XML 格式（不是 JSON！）
2. YaVersion = 219
3. SCM 顶层需要 authURL, YaVersion, Source, Properties
4. project.properties 使用 color.primary 等字段
"""
import zipfile, os, json, uuid as _uuid

BASE = os.path.dirname(os.path.abspath(__file__))

# ==============================================================
# project.properties (模仿弹球游戏格式)
# ==============================================================
PROPS = """#
#Fri Jun 19 11:00:00 CST 2026
source=../src
name=LoginPage
defaultfilescope=App
main=appinventor.ai_user.LoginPage.Screen1
color.accent=&HFFFF4081
sizing=Responsive
assets=../assets
theme=AppTheme.Light
showlistsasjson=True
useslocation=False
aname=LoginPage
actionbar=True
color.primary=&HFF3F51B5
build=../build
versionname=1.0
versioncode=1
color.primary.dark=&HFF303F9F
"""

# ==============================================================
# Screen1.scm (模仿弹球游戏格式 - 顶层有 authURL, YaVersion, Source, Properties)
# ==============================================================
def uid():
    return str(_uuid.uuid4().int % (10**18) * (-1 if _uuid.uuid4().int % 2 else 1))

SCM_JSON = {
    "authURL": ["ai2.17coding.net"],
    "YaVersion": "219",
    "Source": "Form",
    "Properties": {
        "$Name": "Screen1",
        "$Type": "Form",
        "$Version": "30",
        "Uuid": "0",
        "Title": "User Login",
        "AppName": "LoginPage",
        "ActionBar": "True",
        "$Components": [
            {
                "$Name": "Label_Title", "$Type": "Label", "$Version": "5",
                "Uuid": "-7044951163314671203",
                "Text": "Welcome! Please Login"
            },
            {
                "$Name": "TextBox_Username", "$Type": "TextBox", "$Version": "6",
                "Uuid": "-1234567890123456789",
                "Hint": "Enter Username"
            },
            {
                "$Name": "TextBox_Password", "$Type": "TextBox", "$Version": "6",
                "Uuid": "-2345678901234567890",
                "Hint": "Enter Password",
                "PasswordVisible": "True"
            },
            {
                "$Name": "Button_Login", "$Type": "Button", "$Version": "7",
                "Uuid": "-3456789012345678901",
                "Text": "Log In"
            },
            {
                "$Name": "Label_Error", "$Type": "Label", "$Version": "5",
                "Uuid": "-4567890123456789012",
                "Text": ""
            },
            {
                "$Name": "Label_NoAccount", "$Type": "Label", "$Version": "5",
                "Uuid": "-5678901234567890123",
                "Text": "Don't have an account?"
            },
            {
                "$Name": "Button_GoRegister", "$Type": "Button", "$Version": "7",
                "Uuid": "-6789012345678901234",
                "Text": "Register Now"
            },
            {
                "$Name": "TinyDB_Users", "$Type": "TinyDB", "$Version": "3",
                "Uuid": "-7890123456789012345"
            },
            {
                "$Name": "Notifier_Login", "$Type": "Notifier", "$Version": "6",
                "Uuid": "-8901234567890123456"
            }
        ]
    }
}

SCM_CONTENT = "#|\n$JSON\n" + json.dumps(SCM_JSON, ensure_ascii=False, separators=(',', ':')) + "\n|#"

# ==============================================================
# 生成随机 block ID (模仿弹球游戏的格式)
# ==============================================================
import random, string as _string

def bid():
    """生成类似 t075,TS?19+lb)S#ag/m 的随机 ID"""
    chars = _string.ascii_letters + _string.digits + "+-.:;=?@^_`|~!#$%&*()[]{}"
    return ''.join(random.choice(chars) for _ in range(20))


# ==============================================================
# 构建 Blocks XML (模仿弹球游戏的 XML 格式)
# ==============================================================
def build_blocks_xml():
    """
    登录/注册逻辑:
    1. Button_Login.Click ->
       if TextBox_Username.Text == "" OR TextBox_Password.Text == "" 
       then Notifier_Login.ShowMessageDialog("请填写所有字段", "提示", "确定")
       else 
         if TinyDB_Users.Value(TextBox_Username.Text) == TextBox_Password.Text
         then Notifier_Login.ShowMessageDialog("登录成功！欢迎！", "提示", "确定")
         else Notifier_Login.ShowMessageDialog("用户名或密码错误！", "提示", "确定")
    
    2. Button_GoRegister.Click ->
       TinyDB_Users.StoreValue(TextBox_Username.Text, TextBox_Password.Text)
       -> Notifier_Login.ShowMessageDialog("注册成功！请登录", "提示", "确定")
    """
    blocks = []
    
    # ========== Login Event ==========
    ev1_id = bid()     # Button_Login.Click
    if1_id = bid()     # controls_if (empty check)
    or1_id = bid()     # logic_operation OR
    eq_u_id = bid()    # logic_compare EQ (username == "")
    get_u_id = bid()   # component_get TextBox_Username.Text
    empty1_id = bid()  # text ""
    eq_p_id = bid()    # logic_compare EQ (password == "")
    get_p_id = bid()   # component_get TextBox_Password.Text
    empty2_id = bid()  # text ""
    show1_id = bid()   # Notifier.ShowMessageDialog "请填写"
    msg1_id = bid()    # text "请填写所有字段"
    title1_id = bid()  # text "提示"
    btn1_id = bid()    # text "确定"
    
    if2_id = bid()     # controls_if (cred check) - in ELSE
    eq_c_id = bid()    # logic_compare EQ (db == pass)
    get_db_id = bid()  # component_get TinyDB.Value(tag)
    get_utag_id = bid() # component_get TextBox_Username.Text (for tag)
    empty_tag_id = bid() # text "" (valueIfTagNotThere)
    get_p2_id = bid()  # component_get TextBox_Password.Text (for compare)
    show2_id = bid()   # Notifier.ShowMessageDialog "登录成功"
    msg2_id = bid()    # text "登录成功！欢迎！"
    title2_id = bid()  # text "提示"
    btn2_id = bid()    # text "确定"
    show3_id = bid()   # Notifier.ShowMessageDialog "密码错误"
    msg3_id = bid()    # text "用户名或密码错误！"
    title3_id = bid()  # text "提示"
    btn3_id = bid()    # text "确定"
    
    # ========== Register Event ==========
    ev2_id = bid()     # Button_GoRegister.Click
    store_id = bid()   # TinyDB.StoreValue
    get_utag2_id = bid() # component_get TextBox_Username.Text (tag)
    get_p3_id = bid()  # component_get TextBox_Password.Text (value)
    show4_id = bid()   # Notifier.ShowMessageDialog "注册成功"
    msg4_id = bid()    # text "注册成功！请登录"
    title4_id = bid()  # text "提示"
    btn4_id = bid()    # text "确定"
    
    xml_parts = []
    xml_parts.append('<?xml version="1.0" encoding="UTF-8" standalone="no"?>')
    xml_parts.append(f'<xml xmlns="http://www.w3.org/1999/xhtml">')
    
    # ---- Login Event Block ----
    xml_parts.append(
        f'<block type="component_event" id="{ev1_id}" x="-267" y="-352">'
        f'<mutation component_type="Button" is_generic="false" instance_name="Button_Login" event_name="Click"></mutation>'
        f'<field name="COMPONENT_SELECTOR">Button_Login</field>'
        f'<statement name="DO">'
        # ---- Outer IF (empty check) ----
        f'<block type="controls_if" id="{if1_id}">'
        f'<mutation else="1"></mutation>'
        f'<value name="IF0">'
        # ---- OR logic ----
        f'<block type="logic_operation" id="{or1_id}">'
        f'<field name="OP">OR</field>'
        f'<value name="A">'
        # ---- EQ username=="" ----
        f'<block type="logic_compare" id="{eq_u_id}">'
        f'<field name="OP">EQ</field>'
        f'<value name="A">'
        f'<block type="component_set_get" id="{get_u_id}">'
        f'<mutation component_type="TextBox" set_or_get="get" property_name="Text" is_generic="false" instance_name="TextBox_Username"></mutation>'
        f'<field name="COMPONENT_SELECTOR">TextBox_Username</field>'
        f'<field name="PROP">Text</field>'
        f'</block>'
        f'</value>'
        f'<value name="B">'
        f'<block type="text" id="{empty1_id}">'
        f'<field name="TEXT"></field>'
        f'</block>'
        f'</value>'
        f'</block>'
        f'</value>'
        f'<value name="B">'
        # ---- EQ password=="" ----
        f'<block type="logic_compare" id="{eq_p_id}">'
        f'<field name="OP">EQ</field>'
        f'<value name="A">'
        f'<block type="component_set_get" id="{get_p_id}">'
        f'<mutation component_type="TextBox" set_or_get="get" property_name="Text" is_generic="false" instance_name="TextBox_Password"></mutation>'
        f'<field name="COMPONENT_SELECTOR">TextBox_Password</field>'
        f'<field name="PROP">Text</field>'
        f'</block>'
        f'</value>'
        f'<value name="B">'
        f'<block type="text" id="{empty2_id}">'
        f'<field name="TEXT"></field>'
        f'</block>'
        f'</value>'
        f'</block>'
        f'</value>'
        f'</block>'
        f'</value>'
        # ---- THEN: show "请填写" ----
        f'<statement name="DO0">'
        f'<block type="component_method" id="{show1_id}">'
        f'<mutation component_type="Notifier" method_name="ShowMessageDialog" is_generic="false" instance_name="Notifier_Login"></mutation>'
        f'<field name="COMPONENT_SELECTOR">Notifier_Login</field>'
        f'<value name="ARG0">'
        f'<block type="text" id="{msg1_id}">'
        f'<field name="TEXT">请填写所有字段！</field>'
        f'</block>'
        f'</value>'
        f'<value name="ARG1">'
        f'<block type="text" id="{title1_id}">'
        f'<field name="TEXT">提示</field>'
        f'</block>'
        f'</value>'
        f'<value name="ARG2">'
        f'<block type="text" id="{btn1_id}">'
        f'<field name="TEXT">确定</field>'
        f'</block>'
        f'</value>'
        f'</block>'
        f'</statement>'
        # ---- ELSE: inner IF (cred check) ----
        f'<statement name="ELSE">'
        f'<block type="controls_if" id="{if2_id}">'
        f'<mutation else="1"></mutation>'
        f'<value name="IF0">'
        f'<block type="logic_compare" id="{eq_c_id}">'
        f'<field name="OP">EQ</field>'
        f'<value name="A">'
        f'<block type="component_set_get" id="{get_db_id}">'
        f'<mutation component_type="TinyDB" set_or_get="get" property_name="Value" is_generic="false" instance_name="TinyDB_Users"></mutation>'
        f'<field name="COMPONENT_SELECTOR">TinyDB_Users</field>'
        f'<field name="PROP">Value</field>'
        f'<value name="TAG">'
        f'<block type="component_set_get" id="{get_utag_id}">'
        f'<mutation component_type="TextBox" set_or_get="get" property_name="Text" is_generic="false" instance_name="TextBox_Username"></mutation>'
        f'<field name="COMPONENT_SELECTOR">TextBox_Username</field>'
        f'<field name="PROP">Text</field>'
        f'</block>'
        f'</value>'
        f'<value name="VALUEIFTAGNOTTHERE">'
        f'<block type="text" id="{empty_tag_id}">'
        f'<field name="TEXT"></field>'
        f'</block>'
        f'</value>'
        f'</block>'
        f'</value>'
        f'<value name="B">'
        f'<block type="component_set_get" id="{get_p2_id}">'
        f'<mutation component_type="TextBox" set_or_get="get" property_name="Text" is_generic="false" instance_name="TextBox_Password"></mutation>'
        f'<field name="COMPONENT_SELECTOR">TextBox_Password</field>'
        f'<field name="PROP">Text</field>'
        f'</block>'
        f'</value>'
        f'</block>'
        f'</value>'
        # ---- THEN: login success ----
        f'<statement name="DO0">'
        f'<block type="component_method" id="{show2_id}">'
        f'<mutation component_type="Notifier" method_name="ShowMessageDialog" is_generic="false" instance_name="Notifier_Login"></mutation>'
        f'<field name="COMPONENT_SELECTOR">Notifier_Login</field>'
        f'<value name="ARG0">'
        f'<block type="text" id="{msg2_id}">'
        f'<field name="TEXT">登录成功！欢迎！</field>'
        f'</block>'
        f'</value>'
        f'<value name="ARG1">'
        f'<block type="text" id="{title2_id}">'
        f'<field name="TEXT">提示</field>'
        f'</block>'
        f'</value>'
        f'<value name="ARG2">'
        f'<block type="text" id="{btn2_id}">'
        f'<field name="TEXT">确定</field>'
        f'</block>'
        f'</value>'
        f'</block>'
        f'</statement>'
        # ---- ELSE: login fail ----
        f'<statement name="ELSE">'
        f'<block type="component_method" id="{show3_id}">'
        f'<mutation component_type="Notifier" method_name="ShowMessageDialog" is_generic="false" instance_name="Notifier_Login"></mutation>'
        f'<field name="COMPONENT_SELECTOR">Notifier_Login</field>'
        f'<value name="ARG0">'
        f'<block type="text" id="{msg3_id}">'
        f'<field name="TEXT">用户名或密码错误！</field>'
        f'</block>'
        f'</value>'
        f'<value name="ARG1">'
        f'<block type="text" id="{title3_id}">'
        f'<field name="TEXT">提示</field>'
        f'</block>'
        f'</value>'
        f'<value name="ARG2">'
        f'<block type="text" id="{btn3_id}">'
        f'<field name="TEXT">确定</field>'
        f'</block>'
        f'</value>'
        f'</block>'
        f'</statement>'
        f'</block>'
        f'</statement>'
        f'</block>'
        f'</statement>'
        f'</block>'
    )
    
    # ---- Register Event Block ----
    xml_parts.append(
        f'<block type="component_event" id="{ev2_id}" x="-295" y="100">'
        f'<mutation component_type="Button" is_generic="false" instance_name="Button_GoRegister" event_name="Click"></mutation>'
        f'<field name="COMPONENT_SELECTOR">Button_GoRegister</field>'
        f'<statement name="DO">'
        f'<block type="component_method" id="{store_id}">'
        f'<mutation component_type="TinyDB" method_name="StoreValue" is_generic="false" instance_name="TinyDB_Users"></mutation>'
        f'<field name="COMPONENT_SELECTOR">TinyDB_Users</field>'
        f'<value name="ARG0">'
        f'<block type="component_set_get" id="{get_utag2_id}">'
        f'<mutation component_type="TextBox" set_or_get="get" property_name="Text" is_generic="false" instance_name="TextBox_Username"></mutation>'
        f'<field name="COMPONENT_SELECTOR">TextBox_Username</field>'
        f'<field name="PROP">Text</field>'
        f'</block>'
        f'</value>'
        f'<value name="ARG1">'
        f'<block type="component_set_get" id="{get_p3_id}">'
        f'<mutation component_type="TextBox" set_or_get="get" property_name="Text" is_generic="false" instance_name="TextBox_Password"></mutation>'
        f'<field name="COMPONENT_SELECTOR">TextBox_Password</field>'
        f'<field name="PROP">Text</field>'
        f'</block>'
        f'</value>'
        f'<next>'
        f'<block type="component_method" id="{show4_id}">'
        f'<mutation component_type="Notifier" method_name="ShowMessageDialog" is_generic="false" instance_name="Notifier_Login"></mutation>'
        f'<field name="COMPONENT_SELECTOR">Notifier_Login</field>'
        f'<value name="ARG0">'
        f'<block type="text" id="{msg4_id}">'
        f'<field name="TEXT">注册成功！请登录</field>'
        f'</block>'
        f'</value>'
        f'<value name="ARG1">'
        f'<block type="text" id="{title4_id}">'
        f'<field name="TEXT">提示</field>'
        f'</block>'
        f'</value>'
        f'<value name="ARG2">'
        f'<block type="text" id="{btn4_id}">'
        f'<field name="TEXT">确定</field>'
        f'</block>'
        f'</value>'
        f'</block>'
        f'</next>'
        f'</block>'
        f'</statement>'
        f'</block>'
    )
    
    xml_parts.append(f'<yacodeblocks ya-version="219" language-version="34"></yacodeblocks>')
    xml_parts.append('</xml>')
    
    return ''.join(xml_parts)


# ==============================================================
# 打包
# ==============================================================
def make_aia(filename, bky_xml):
    path = os.path.join(BASE, filename)
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('youngandroidproject/project.properties', PROPS)
        zf.writestr('src/appinventor/ai_user/LoginPage/Screen1.scm', SCM_CONTENT)
        zf.writestr('src/appinventor/ai_user/LoginPage/Screen1.bky', bky_xml)
    size = os.path.getsize(path)
    print(f"  [OK] {filename} ({size} bytes)")
    return path

if __name__ == "__main__":
    print("生成 LoginPage.aia (v7 - XML BKY 格式 + 完整登录逻辑)")
    bky = build_blocks_xml()
    make_aia("LoginPage.aia", bky)
    print()
    print("=" * 60)
    print("登录逻辑:")
    print("  [登录] 点击 Log In -> 检查用户名/密码是否为空")
    print("    -> 空: 弹出 '请填写所有字段！'")
    print("    -> 非空: 检查 TinyDB 中存储的密码是否匹配")
    print("      -> 匹配: 弹出 '登录成功！欢迎！'")
    print("      -> 不匹配: 弹出 '用户名或密码错误！'")
    print("  [注册] 点击 Register Now ->")
    print("    存入 TinyDB -> 弹出 '注册成功！请登录'")
    print("=" * 60)
