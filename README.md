# SuperSpeedCalc Server

基于 Flask 框架的全功能后端服务，提供完整的社交化应用功能。

> ✅ **API响应格式已完全标准化** - 所有接口统一使用 `code + message + data` 格式

## 🚀 快速开始

### 环境要求
- Python 3.8+
- SQLite 数据库

### 安装运行
```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务器
python start.py
```

服务器将在 `http://localhost:8000` 启动

## 📊 数据库表结构

项目包含以下数据表：

| 表名 | 说明 | 主要功能 |
|------|------|----------|
| `my_user` | 用户表 | 用户注册、登录、信息管理 |
| `charts` | 排行榜表 | 用户成绩记录、排名统计 |
| `forum` | 论坛表 | 论坛帖子发布、管理 |
| `image` | 图片表 | 图片上传、管理 |
| `history` | 历史记录表 | 用户操作历史记录 |
| `app_releases` | 应用发布表 | APK版本管理、更新控制 |
| `user_relationships` | 用户关系表 | 关注/粉丝关系管理 |
| `posts` | 帖子表 | 用户帖子发布、管理 |
| `likes` | 点赞表 | 帖子点赞功能 |
| `replies` | 回复表 | 评论回复功能 |
| `banners` | 横幅表 | 轮播图、广告管理 |

## 🔧 API 响应格式

✅ **所有API接口已完全标准化**，使用简化的响应格式：

> **标准化完成**：所有接口现在都严格按照 `code + message + data` 格式返回响应，确保前后端交互的一致性。

### 成功响应
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "key": "value"
  }
}
```

### 分页响应
```json
{
  "code": 200,
  "message": "获取数据成功",
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total": 100,
      "pages": 10
    }
  }
}
```

### 错误响应
```json
{
  "code": 400,
  "message": "错误描述"
}
```

### 响应格式说明
- **code**: HTTP状态码（200成功，400客户端错误，500服务器错误）
- **message**: 中文提示信息
- **data**: 实际数据（JSON对象），仅成功响应包含此字段
- 错误响应只包含 `code` 和 `message` 字段，简化了错误处理

## 📚 API 接口文档

详细的API接口文档请查看以下文件：

- [用户管理 API](docs/user_api.md)
- [排行榜 API](docs/charts_api.md)
- [论坛 API](docs/forum_api.md)
- [图片管理 API](docs/image_api.md)
- [历史记录 API](docs/history_api.md)
- [应用发布 API](docs/releases_api.md)
- [用户关系 API](docs/relationship_api.md)
- [帖子管理 API](docs/posts_api.md)
- [点赞功能 API](docs/likes_api.md)
- [回复功能 API](docs/replies_api.md)
- [横幅管理 API](docs/banners_api.md)
- [短信服务 API](docs/sms_api.md)

## 🛠️ 项目结构

```
SuperSpeedCalc-Server/
├── app.py                 # Flask应用主文件
├── config.py             # 配置文件
├── start.py              # 启动脚本
├── models/               # 数据模型
├── routes/               # API路由
├── utils/                # 工具函数
│   └── response.py       # 标准化响应工具类
├── uploads/              # 文件上传目录
├── logs/                 # 日志文件
└── docs/                 # API文档
```

## 🔍 健康检查

访问 `http://localhost:8000/health` 检查服务状态

## 📝 日志

- 控制台输出：实时日志
- 文件日志：`logs/app.log`

## 🧪 接口测试

### 测试状态
- ✅ **服务器正常运行** - 端口 8000
- ✅ **响应格式标准化** - 所有接口使用统一的 `code + message + data` 格式
- ✅ **基础接口测试通过** - 用户列表接口返回正确格式
- ✅ **用户模型更新** - 用户名字段可为空，手机号唯一且可为空
- ✅ **500错误修复** - 所有接口跨行return语句问题已解决

### 快速测试
```bash
# 测试用户列表接口
curl "http://localhost:8000/users?page=1&per_page=5"

# 测试横幅创建接口
curl -X POST "http://localhost:8000/banners" \
  -H "Content-Type: application/json" \
  -d '{"title": "测试横幅", "show": true, "click": true}'

# 预期响应格式
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "items": [...],
    "pagination": {...}
  }
}
```

### 用户模型变更
- **用户名字段**：现在可以为空，不再要求唯一性
- **手机号字段**：保持唯一性，可以为空
- **数据库迁移**：已自动完成用户名字段的数据库结构更新

## 🆘 故障排除

### 常见问题

1. **端口占用**：修改 `start.py` 中的端口号
2. **数据库错误**：检查 `instance/app.db` 文件权限
3. **依赖缺失**：运行 `pip install -r requirements.txt`
4. **响应格式**：所有接口已标准化，使用 `utils/response.py` 中的工具函数
5. **接口路径**：注意接口路径没有 `/api` 前缀，直接使用 `/users`、`/charts` 等
6. **500错误**：已修复所有跨行return语句问题，确保所有接口正常返回
7. **用户名字段**：现在可以为空，注册时不需要提供用户名

### 调试模式

开发环境下自动启用调试模式，支持：
- 自动重载
- 详细错误信息
- SQL查询日志

---

**注意**：这是开发服务器，生产环境请使用专业的WSGI服务器。
