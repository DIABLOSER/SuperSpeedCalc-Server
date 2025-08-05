# SuperSpeedCalc Server

基于 Flask 框架的后端服务，包含用户管理、图表管理和论坛功能。

## 项目结构

```
SuperSpeedCalc-Server/
├── app.py                 # Flask 应用主文件
├── config.py             # 配置文件
├── models/               # 数据库模型目录
│   ├── __init__.py      # 模型包初始化
│   ├── base.py          # 基础模型和数据库实例
│   ├── user.py          # 用户模型
│   ├── chart.py         # 图表模型
│   └── forum.py         # 论坛模型
├── requirements.txt      # 项目依赖
├── routes/              # API 路由
│   ├── __init__.py
│   ├── user_routes.py   # 用户相关 API
│   ├── charts_routes.py # 图表相关 API
│   └── forum_routes.py  # 论坛相关 API
├── test_api.py          # API 测试脚本
├── start.py             # 启动脚本
└── README.md           # 项目说明
```

## 数据库表结构

### MyUser 表（用户表）
- `objectId` (String, Primary Key): 用户唯一标识 
- `username` (String, Unique): 用户名
- `email` (String, Unique): 邮箱
- `password` (String): 密码（加密存储）
- `nickname` (String): 昵称
- `avatar` (String): 头像地址
- `bio` (Text): 个人简介
- `score` (Integer): 用户积分，默认0
- `experence` (Integer): 用户经验值，默认0
- `boluo` (Float): 菠萝币数量，默认0.0
- `isActive` (Boolean): 是否激活
- `lastLogin` (DateTime): 最后登录时间
- `createdAt` (DateTime): 创建时间
- `updatedAt` (DateTime): 更新时间

### Charts 表（排行榜表）
- `objectId` (String, Primary Key): 记录唯一标识
- `title` (String): 标题
- `achievement` (Float): 成绩值，默认0.0
- `user` (String, Foreign Key): 所属用户ID
- `createdAt` (DateTime): 创建时间
- `updatedAt` (DateTime): 更新时间

### Forum 表（社区表）
- `objectId` (String, Primary Key): 帖子唯一标识
- `content` (Text): 帖子内容
- `category` (String): 帖子分类
- `tags` (JSON): 标签列表
- `public` (Boolean): 是否公开，默认True
- `images` (JSON): 图片列表，存储图片URL数组
- `viewCount` (Integer): 浏览次数
- `likeCount` (Integer): 点赞数
- `replyCount` (Integer): 回复数
- `isPinned` (Boolean): 是否置顶
- `isClosed` (Boolean): 是否关闭
- `user` (String, Foreign Key): 作者ID
- `createdAt` (DateTime): 创建时间
- `updatedAt` (DateTime): 更新时间

### Image 表（图片表）
- `objectId` (String, Primary Key): 图片唯一标识
- `fileName` (String): 图片文件名
- `path` (String): 图片本地路径
- `url` (String): 图片访问URL
- `fileSize` (Integer): 文件大小（字节）
- `createdAt` (DateTime): 创建时间
- `updatedAt` (DateTime): 更新时间

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

## API 接口

### 用户 API (`/api/users`)

- `GET /api/users` - 获取所有用户
- `GET /api/users/<object_id>` - 获取单个用户
- `POST /api/users` - 创建用户
- `PUT /api/users/<object_id>` - 更新用户
- `DELETE /api/users/<object_id>` - 删除用户
- `POST /api/users/login` - 用户登录
- `POST /api/users/<object_id>/score` - 更新用户积分
- `POST /api/users/<object_id>/experence` - 更新用户经验值
- `POST /api/users/<object_id>/boluo` - 更新用户菠萝币

### 图表 API (`/api/charts`)

- `GET /api/charts` - 获取图表列表（支持查询参数：user）
- `GET /api/charts/<object_id>` - 获取单个图表
- `POST /api/charts` - 创建图表
- `PUT /api/charts/<object_id>` - 更新图表
- `DELETE /api/charts/<object_id>` - 删除图表
- `GET /api/charts/leaderboard` - 获取排行榜（按成绩值排序）
- `POST /api/charts/<object_id>/achievement` - 更新图表成绩值

### 论坛 API (`/api/forum`)

- `GET /api/forum` - 获取帖子列表（支持分页和查询参数：category、user、isPinned、public）
- `GET /api/forum/<object_id>` - 获取单个帖子
- `POST /api/forum` - 创建帖子
- `PUT /api/forum/<object_id>` - 更新帖子
- `DELETE /api/forum/<object_id>` - 删除帖子
- `POST /api/forum/<object_id>/like` - 给帖子点赞
- `GET /api/forum/categories` - 获取所有分类
- `GET /api/forum/popular` - 获取热门帖子
- `GET /api/forum/public` - 获取公开帖子

### 图片 API (`/api/images`)

- `GET /api/images` - 获取图片列表（支持分页）
- `GET /api/images/<object_id>` - 获取单个图片
- `POST /api/images` - 创建图片记录（JSON方式）
- `PUT /api/images/<object_id>` - 更新图片信息
- `DELETE /api/images/<object_id>` - 删除图片
- `POST /api/images/upload` - 上传单个图片文件
- `POST /api/images/upload/multiple` - 批量上传图片文件
- `GET /api/images/stats` - 获取图片统计信息
- `GET /api/images/search` - 搜索图片（按文件名）
- `POST /api/images/<object_id>/url` - 更新图片URL
- `POST /api/images/batch/delete` - 批量删除图片
- `DELETE /api/images/clear` - 清空所有图片

## 示例请求

### 创建用户

```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "nickname": "测试用户",
    "avatar": "https://example.com/avatar.jpg",
    "bio": "这是一个测试用户",
    "score": 100,
    "experence": 50,
    "boluo": 10.5
  }'
```

### 更新用户积分

```bash
curl -X POST http://localhost:5000/api/users/<user_id>/score \
  -H "Content-Type: application/json" \
  -d '{
    "score_change": 50
  }'
```

### 更新用户经验值

```bash
curl -X POST http://localhost:5000/api/users/<user_id>/experence \
  -H "Content-Type: application/json" \
  -d '{
    "exp_change": 25
  }'
```

### 更新用户菠萝币

```bash
curl -X POST http://localhost:5000/api/users/<user_id>/boluo \
  -H "Content-Type: application/json" \
  -d '{
    "boluo_change": 5.5
  }'
```

### 创建图表

```bash
curl -X POST http://localhost:5000/api/charts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "用户游戏记录",
    "achievement": 100.5,
    "user": "用户的objectId"
  }'
```

### 更新图表成绩值

```bash
curl -X POST http://localhost:5000/api/charts/<chart_id>/achievement \
  -H "Content-Type: application/json" \
  -d '{
    "achievement_change": 25.5
  }'
```

### 获取排行榜

```bash
curl -X GET http://localhost:5000/api/charts/leaderboard?limit=10
```

### 创建论坛帖子

```bash
curl -X POST http://localhost:5000/api/forum \
  -H "Content-Type: application/json" \
  -d '{
    "content": "这是我的第一个帖子",
    "category": "公告",
    "tags": ["欢迎", "新手", "公告"],
    "public": true,
    "images": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
    "user": "用户的objectId"
  }'
```

### 获取公开帖子

```bash
curl -X GET http://localhost:5000/api/forum/public?limit=10
```

### 创建图片记录

```bash
curl -X POST http://localhost:5000/api/images \
  -H "Content-Type: application/json" \
  -d '{
    "fileName": "example.jpg",
    "path": "/uploads/images/example.jpg",
    "url": "https://example.com/images/example.jpg",
    "fileSize": 256000
  }'
```

### 上传单个图片文件

```bash
curl -X POST http://localhost:5000/api/images/upload \
  -F "file=@/path/to/your/image.jpg"
```

### 批量上传图片文件

```bash
curl -X POST http://localhost:5000/api/images/upload/multiple \
  -F "files=@/path/to/image1.jpg" \
  -F "files=@/path/to/image2.jpg" \
  -F "files=@/path/to/image3.jpg"
```

### 获取图片统计信息

```bash
curl -X GET http://localhost:5000/api/images/stats
```

### 搜索图片

```bash
curl -X GET "http://localhost:5000/api/images/search?q=test&page=1&per_page=10"
```

### 批量删除图片

```bash
curl -X POST http://localhost:5000/api/images/batch/delete \
  -H "Content-Type: application/json" \
  -d '{
    "image_ids": ["image_id_1", "image_id_2", "image_id_3"]
  }'
```

### 更新图片URL

```bash
curl -X POST http://localhost:5000/api/images/<image_id>/url \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/new-path/image.jpg"
  }'
```

## 健康检查

访问 `http://localhost:5000/health` 可以检查服务状态。

## 注意事项

1. 默认使用 SQLite 数据库，生产环境建议切换到 MySQL 或 PostgreSQL
2. 密码使用 werkzeug 进行哈希加密存储，字段名为 password
3. 支持 CORS 跨域请求
4. 所有 API 响应都包含 `success` 字段表示操作是否成功
5. 新增了用户积分、经验值和菠萝币系统
6. 用户字段支持完整的游戏化元素（积分、经验、虚拟货币）
7. 模型采用模块化设计，每个数据表独立为一个文件，便于维护和扩展
8. Charts表简化为排行榜功能，专注于标题和成绩值管理 