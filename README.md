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
- `avatar` (String): 头像地址
- `bio` (Text): 个人简介
- `score` (Integer): 用户积分，默认0
- `experence` (Integer): 用户经验值，默认0
- `boluo` (Integer): 菠萝币数量，默认0
- `isActive` (Boolean): 是否激活
- `admin` (Boolean): 是否管理员，默认False
- `sex` (Integer): 性别（1=男，0=女），默认1
- `birthday` (Date): 生日（YYYY-MM-DD）
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

### 2. 数据库管理

#### 首次使用 - 初始化数据库
```bash
# 方式1: 使用数据库管理脚本（推荐）
python manage_db.py init

# 方式2: 使用应用启动参数
python app.py --init-db
```

#### 日常使用 - 启动应用
```bash
python app.py
```

#### 数据库管理命令
```bash
# 检查数据库状态
python manage_db.py check

# 备份数据库
python manage_db.py backup

# 重置数据库（删除所有数据）
python manage_db.py reset

# 查看帮助
python manage_db.py help
```

### 3. 应用地址

应用将在 `http://localhost:5000` 启动。

## API 接口

### 用户 API (`/api/users`)

- `GET /api/users` - 获取所有用户（支持排序与分页：sort_by, order, page, per_page）
- `GET /api/users/count` - 获取用户总数
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
- `POST /api/images/upload/multiple`