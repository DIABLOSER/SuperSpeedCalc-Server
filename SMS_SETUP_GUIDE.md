# SMS 短信服务配置指南

## 概述

本项目已集成 Bmob 短信服务，支持发送短信验证码和验证短信验证码功能。

## 配置步骤

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 获取 Bmob 配置信息

1. 访问 [Bmob 控制台](https://www.bmobapp.com/)
2. 注册并登录账号
3. 创建新应用
4. 在应用设置中获取以下信息：
   - `Application ID`
   - `REST API Key`
   - `Master Key`（可选，用于更高权限操作）

### 3. 配置环境变量

创建 `.env` 文件（推荐）或直接设置环境变量：

```bash
# .env 文件内容
BMOB_APPLICATION_ID=你的Application_ID
BMOB_REST_API_KEY=你的REST_API_Key
BMOB_MASTER_KEY=你的Master_Key
```

或者直接在 `config.py` 中修改默认值：

```python
# Bmob 配置
BMOB_APPLICATION_ID = '你的Application_ID'
BMOB_REST_API_KEY = '你的REST_API_Key'
BMOB_MASTER_KEY = '你的Master_Key'
```

### 4. 启动服务器

```bash
python app.py
```

## API 接口

### 发送短信验证码

**接口地址：** `POST /sms/send`

**请求参数：**
```json
{
    "phone": "13800138000"
}
```

**响应示例：**
```json
{
    "success": true,
    "message": "短信验证码发送成功",
    "phone": "13800138000"
}
```

### 验证短信验证码

**接口地址：** `POST /sms/verify`

**请求参数：**
```json
{
    "phone": "13800138000",
    "code": "123456"
}
```

**响应示例：**
```json
{
    "success": true,
    "message": "短信验证码验证成功",
    "phone": "13800138000",
    "verified": true
}
```

## 测试

运行测试脚本：

```bash
python test_sms_api.py
```

**注意：** 测试前请确保：
1. 服务器正在运行
2. 已正确配置 Bmob 参数
3. 使用真实的手机号进行测试（避免使用测试号码）

## 错误处理

### 常见错误码

- `400`: 请求参数错误（手机号格式不正确、缺少必需参数等）
- `500`: 服务器内部错误（Bmob 配置错误、网络问题等）

### 错误响应示例

```json
{
    "success": false,
    "error": "手机号格式不正确"
}
```

## 安全注意事项

1. **保护配置信息**：不要将 Bmob 的密钥信息提交到版本控制系统
2. **使用环境变量**：推荐使用 `.env` 文件或环境变量来管理敏感配置
3. **限制发送频率**：建议在业务层面添加发送频率限制，防止滥用
4. **验证码有效期**：Bmob 默认验证码有效期为 10 分钟

## 费用说明

Bmob 短信服务按条计费，具体费用请参考 [Bmob 官方定价](https://www.bmobapp.com/pricing.html)。

## 技术支持

- [Bmob 官方文档](https://doc.bmobapp.com/data/python/index.html#_16)
- [Bmob 短信服务文档](https://doc.bmobapp.com/sms/python/index.html)
