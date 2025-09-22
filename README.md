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

# 启动服务器（选择环境）
python start_development.py    # 开发环境 - 端口 8000
python start_production.py     # 生产环境 - 端口 8001
```

### 环境说明
- **开发环境** (`start_development.py`): `http://localhost:8000` - 用于开发和测试
- **生产环境** (`start_production.py`): `http://localhost:8001` - 用于生产部署

## 📊 数据库表结构

项目包含以下数据表：

| 表名 | 说明 | 主要功能 |
|------|------|----------|
| `my_user` | 用户表 | 用户注册、登录、信息管理 |
| `charts` | 排行榜表 | 用户成绩记录、排名统计 |
| `image` | 图片表 | 图片上传、管理 |
| `history` | 历史记录表 | 用户操作历史记录 |
| `app_releases` | 应用发布表 | APK版本管理、更新控制 |
| `user_relationships` | 用户关系表 | 关注/粉丝关系管理 |
| `posts` | 帖子表 | 用户帖子发布、管理 |
| `likes` | 点赞表 | 帖子点赞功能 |
| `replies` | 回复表 | 评论回复功能（支持独立存在） |
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
├── start_production.py     # 生产环境启动脚本 (端口 8001)
├── start_development.py    # 开发环境启动脚本 (端口 8000)
├── models/               # 数据模型
├── routes/               # API路由
├── utils/                # 工具函数
│   └── response.py       # 标准化响应工具类
├── uploads/              # 文件上传目录
├── logs/                 # 日志文件
└── docs/                 # API文档
```

## 🔍 健康检查

- **测试环境**: `http://localhost:8000/health`
- **正式环境**: `http://localhost:8001/health`

## 📝 日志

- 控制台输出：实时日志
- 文件日志：`logs/app.log`

## 🧪 接口测试

### 测试状态
- ✅ **双环境支持** - 测试环境(8000) + 正式环境(8001)
- ✅ **响应格式标准化** - 所有接口使用统一的 `code + message + data` 格式
- ✅ **基础接口测试通过** - 用户列表接口返回正确格式
- ✅ **用户模型更新** - 用户名字段可为空，手机号唯一且可为空
- ✅ **500错误修复** - 所有接口跨行return语句问题已解决
- ✅ **点赞功能测试通过** - 点赞/取消点赞功能完全正常
- ✅ **评论功能测试通过** - 一级评论和二级回复功能完全正常
- ✅ **社交功能验证** - 用户关系、帖子管理、互动功能全部测试通过
- ✅ **图片上传功能** - 单个和批量图片上传功能完全正常
- ✅ **响应格式统一** - 所有接口使用统一的响应格式

### 快速测试
```bash
# 基础功能测试
curl "http://localhost:8000/users?page=1&per_page=5"
curl "http://localhost:8000/posts?page=1&per_page=5"

# 社交功能测试
# 点赞帖子
curl -X POST "http://localhost:8000/posts/{post_id}/like" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123"}'

# 取消点赞
curl -X DELETE "http://localhost:8000/posts/{post_id}/like" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123"}'

# 创建评论
curl -X POST "http://localhost:8000/replies/" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "这是一条评论",
    "post": "post123",
    "user": "user123"
  }'

# 获取帖子评论
curl "http://localhost:8000/replies/post/{post_id}"

# 图片上传功能测试
# 单个图片上传
curl -X POST "http://localhost:8000/images/upload" \
  -F "file=@image.jpg"

# 批量图片上传
curl -X POST "http://localhost:8000/images/upload/multiple" \
  -F "files=@image1.jpg" \
  -F "files=@image2.png" \
  -F "files=@image3.gif"

# 获取图片列表
curl "http://localhost:8000/images/?page=1&per_page=10"

# 获取图片统计
curl "http://localhost:8000/images/stats"

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

### 删除帖子设计理念
- **数据完整性**：删除帖子时，相关评论数据被保留
- **评论独立性**：评论可以独立存在，即使关联的帖子不存在
- **历史记录保留**：确保用户的历史评论记录不会丢失
- **数据恢复支持**：如果帖子被误删，评论数据仍然可以恢复
- **审计功能**：支持数据审计和追踪功能
- **外键约束**：replies表的post字段允许为空，支持软删除模式

## 🆘 故障排除

### 常见问题

1. **端口占用**：使用不同的启动脚本 (`start_development.py` 或 `start_production.py`)
2. **数据库错误**：检查 `instance/app_development.db` 或 `instance/app_production.db` 文件权限
3. **依赖缺失**：运行 `pip install -r requirements.txt`
4. **响应格式**：所有接口已标准化，使用 `utils/response.py` 中的工具函数
5. **接口路径**：注意接口路径没有 `/api` 前缀，直接使用 `/users`、`/charts` 等
6. **500错误**：已修复所有跨行return语句问题，确保所有接口正常返回
7. **用户名字段**：现在可以为空，注册时不需要提供用户名
8. **删除帖子**：删除帖子时评论数据会被保留，这是设计特性而非错误

### 调试模式

开发环境下自动启用调试模式，支持：
- 自动重载
- 详细错误信息
- SQL查询日志

## 🌐 双环境部署

### 环境配置
项目支持双环境部署，方便开发测试和生产使用：

| 环境 | 启动脚本 | 端口 | 用途 | 访问地址 |
|------|----------|------|------|----------|
| 开发环境 | `start_development.py` | 8000 | 开发测试 | http://localhost:8000 |
| 生产环境 | `start_production.py` | 8001 | 生产部署 | http://localhost:8001 |

### 同时运行双环境
```bash
# 终端1 - 启动开发环境
python start_development.py

# 终端2 - 启动生产环境
python start_production.py
```

### 环境切换
- **开发阶段**：使用 `start_development.py` (端口 8000)
- **生产部署**：使用 `start_production.py` (端口 8001)
- **并行测试**：可同时运行两个环境进行对比测试

### 数据库分离
两个环境使用不同的数据库文件，确保数据互不干扰：
- **开发环境**: `instance/app_development.db`
- **生产环境**: `instance/app_production.db`

### CORS 配置
- **本地开发**: 启用 CORS，支持跨域请求，便于前端开发调试
- **服务器部署**: 禁用 CORS，服务器通常有反向代理（如 Nginx）处理跨域

---

**注意**：这是开发服务器，生产环境请使用专业的WSGI服务器。
