# 守护助手 · 本地 API 文档

> 版本：v1.0  
> 基础地址：`http://{host}:5000`  
> JSON 接口：`Content-Type: application/json`

---

## 1. 通用说明

### 1.1 统一响应结构 `ServiceResponse<T>`

| 字段 | 类型 | 说明 |
|------|------|------|
| code | number | `200` 成功，`300+` 失败，`401` 未登录 |
| msg | string | 提示信息 |
| resTime | string | 响应时间，如 `2026-06-26T17:10:55` |
| result | T \| null | 业务数据 |
| tips | string | 补充说明（当前固定为空字符串） |

**成功示例：**

```json
{
  "code": 200,
  "msg": "success",
  "resTime": "2026-06-26T17:10:55",
  "result": {},
  "tips": ""
}
```

**失败示例：**

```json
{
  "code": 300,
  "msg": "图形验证码错误",
  "resTime": "2026-06-26T17:10:55",
  "result": null,
  "tips": ""
}
```

> 鸿蒙端：`response.data.code === 200` 为成功，否则 toast 展示 `msg`。

### 1.2 鉴权

登录后后续请求携带：

```
Authorization: {accessToken}
```

### 1.3 业务类型 bizType

| 值 | 含义 |
|----|------|
| 1 | 手机号登录 |
| 2 | 找回密码 |
| 3 | 注册账户 |
| 4 | 添加紧急联系人 |

### 1.4 演示账号

| 手机号 | 密码 | 昵称 | 头像 |
|--------|------|------|------|
| 120666666673 | 888itcast.CN764%... | 测试学员 | /static/cat.jpg |

---

## 2. 登录流程

```
GET /code/graphic → POST /code/graphic/check → POST /code/sms/send → POST /user/login/verifyCode
```

---

## 3. 验证码模块

### 3.1 获取图形验证码

**GET** `/code/graphic`

| 参数 | 必填 | 说明 |
|------|------|------|
| phone | 是 | 手机号 |
| bizType | 否 | 默认 `1` |
| timestamp | 否 | 防缓存，刷新图片时更新 |

响应：`image/png`，108×42，有效期 300 秒。

---

### 3.2 校验图形验证码

**POST** `/code/graphic/check`

```json
{
  "phone": "13800001234",
  "bizType": 1,
  "verifyCode": "AB3K"
}
```

成功：

```json
{
  "code": 200,
  "msg": "success",
  "result": null,
  "tips": ""
}
```

---

### 3.3 发送短信验证码

**POST** `/code/sms/send`

> 需先通过图形验证码校验

```json
{
  "phone": "13800001234",
  "bizType": 1
}
```

成功：

```json
{
  "code": 200,
  "msg": "短信验证码已发送",
  "result": null,
  "tips": ""
}
```

---

## 4. 用户模块

### 4.1 短信验证码登录

**POST** `/user/login/verifyCode`

```json
{
  "phone": "13800001234",
  "verifyCode": "905049"
}
```

成功 `result` → `LoginInfoResponse`：

```json
{
  "code": 200,
  "msg": "登录成功",
  "result": {
    "accessToken": "18430ad36a414cf4b928a080811ab8dd",
    "avatar": "",
    "nickname": "用户1234",
    "renewalToken": "0ddec108fafb4b1fab98f95a40216886"
  },
  "tips": ""
}
```

---

### 4.2 账号密码登录

**POST** `/user/login/passwd`

```json
{
  "phone": "120666666673",
  "passwd": "888itcast.CN764%..."
}
```

成功 `result` 同上，`avatar` 为 `/static/cat.jpg`。

---

### 4.3 获取我的信息

**GET** `/user/me`

鉴权：Session 或 `Authorization: {accessToken}`

成功：

```json
{
  "code": 200,
  "msg": "success",
  "result": {
    "avatar": "/static/cat.jpg",
    "nickname": "测试学员"
  },
  "tips": ""
}
```

失败（未登录）：

```json
{
  "code": 401,
  "msg": "未登录",
  "result": null,
  "tips": ""
}
```

---

### 4.4 退出登录

**POST** `/user/logout`

```json
{
  "code": 200,
  "msg": "已退出登录",
  "result": null,
  "tips": ""
}
```

---

## 5. 静态资源

**GET** `/static/cat.jpg` — 演示账号头像

---

## 6. 鸿蒙对接

| 鸿蒙 API | 后端接口 |
|----------|----------|
| postCodeGraphicCheckAPI | POST `/code/graphic/check` |
| postCodeSmsSendAPI | POST `/code/sms/send` |
| postUserLoginVerifyCodeAPI | POST `/user/login/verifyCode` |
| postUserLoginPasswdAPI | POST `/user/login/passwd` |
| getUserInfoAPI | GET `/user/me` |

---

## 7. cURL 测试

```bash
# 图形验证码
curl "http://127.0.0.1:5000/code/graphic?phone=13800001234&bizType=1&timestamp=1" -o captcha.png

# 校验图形码
curl -X POST http://127.0.0.1:5000/code/graphic/check \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800001234","bizType":1,"verifyCode":"AB3K"}'

# 发送短信
curl -X POST http://127.0.0.1:5000/code/sms/send \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800001234","bizType":1}'

# 验证码登录
curl -X POST http://127.0.0.1:5000/user/login/verifyCode \
  -H "Content-Type: application/json" \
  -d '{"phone":"13800001234","verifyCode":"905049"}'

# 密码登录
curl -X POST http://127.0.0.1:5000/user/login/passwd \
  -H "Content-Type: application/json" \
  -d '{"phone":"120666666673","passwd":"888itcast.CN764%..."}'

# 获取我的信息
curl http://127.0.0.1:5000/user/me -H "Authorization: YOUR_ACCESS_TOKEN"
```

> 本地调试时，图形码和短信码会打印在服务端控制台。
