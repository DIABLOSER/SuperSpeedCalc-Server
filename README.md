# SuperSpeedCalc Server

基于 Flask 框架的超级速算后端服务，提供完整的用户管理、排行榜、论坛社区、图片管理、历史记录统计、应用版本发布等功能。支持多种排行榜查询（日榜、月榜、年榜、总榜）和完善的用户统计分析。

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
│   ├── forum.py         # 论坛模型
│   ├── image.py         # 图片模型
│   ├── history.py       # 历史记录模型
│   └── releases.py      # 发布版本模型（AppRelease）
├── requirements.txt      # 项目依赖
├── routes/              # API 路由
│   ├── __init__.py
│   ├── user/            # 用户相关 API（蓝图）
│   ├── charts/          # 图表相关 API（蓝图）
│   ├── forum/           # 论坛相关 API（蓝图）
│   ├── image/           # 图片相关 API（蓝图）
│   ├── history/         # 历史记录相关 API（蓝图）
│   └── releases/        # 发布版本相关 API（蓝图）
├── scripts/             # 实用脚本（数据库迁移等）
├── start.py             # 启动脚本
└── README.md           # 项目说明
```

## 数据库表结构

### MyUser 表（用户表）
- `objectId` (String, Primary Key): 用户唯一标识 
- `username` (String, Unique): 用户名
- `email` (String, Unique, Nullable): 邮箱（可为空）
- `mobile` (String, Unique, Nullable): 手机号（可为空）
- `password` (String): 密码（加密存储）
- `avatar` (String): 头像地址
- `bio` (Text): 个人简介
- `experience` (Integer): 用户经验值，默认0
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
- `url` (String): 图片访问URL（如：`/uploads/images/<filename>`）
- `fileSize` (Integer): 文件大小（字节）
- `createdAt` (DateTime): 创建时间
- `updatedAt` (DateTime): 更新时间

### History 表（历史记录表）
- `objectId` (String, Primary Key): 历史记录唯一标识
- `title` (String): 标题，最大200字符
- `score` (Integer): 分数，可以为正数或负数
- `user` (String, Foreign Key): 用户ID，关联到my_user表
- `createdAt` (DateTime): 创建时间
- `updatedAt` (DateTime): 更新时间

### AppRelease 表（发布版本表）
- `objectId` (String, Primary Key): 发布记录唯一标识
- `app_name` (String): 应用名称
- `version_name` (String): 版本号（如 1.2.3）
- `version_code` (Integer): 版本代码（整数）
- `changelog` (Text): 更新内容
- `download_url` (String): 下载链接（如：`/uploads/apk/<filename>`）
- `environment` (String): 发布环境（development/production/staging...），默认 `production`
- `status` (String): 发布状态（如 `draft`/`published`/`deprecated`），默认 `published`
- `is_update` (Boolean): 是否更新（用于客户端提示更新），默认 False
- `force_update` (Boolean): 是否强制更新，默认 False
- `createdAt` (DateTime): 创建时间
- `updatedAt` (DateTime): 更新时间

## 功能特性

### 🎯 核心功能
- **用户管理**: 支持邮箱/手机号注册登录、用户信息管理、经验值和菠萝币系统
- **图表系统**: 成绩记录、排行榜查询、用户排名统计
- **论坛社区**: 帖子发布、分类管理、点赞互动、置顶/关闭控制
- **图片管理**: 单个/批量图片上传、文件存储、静态资源访问
- **历史记录**: 用户游戏历史记录、多维度排行榜（日/月/年/总榜）、统计分析
- **发布管理**: APK版本发布管理、文件上传、版本控制、更新提示
- **数据统计**: 用户得分统计、排名查询、时间段过滤、分页查询

### 🏆 History功能亮点
- **智能排行榜**: 支持日榜、月榜、年榜、总榜
- **完整用户信息**: 所有查询都返回用户的完整信息（头像、经验等）
- **灵活分数系统**: 支持正负数计算，适应各种游戏场景
- **时间精确统计**: 基于UTC时间的精确时间段统计
- **高性能查询**: 使用SQL聚合函数，支持分页和排序

## 环境要求

- **Python**: 3.7+ (推荐使用 Python 3.8+)
- **操作系统**: Windows、macOS、Linux
- **内存**: 最低 512MB（生产环境推荐 1GB+）
- **磁盘**: 100MB+（用于数据库和上传文件存储）

## 安装和运行

### 1. 安装依赖

```bash
# 推荐使用国内镜像源加速安装
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 或者使用默认源
pip install -r requirements.txt

# 如果使用虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或者 venv\Scripts\activate  # Windows
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
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
# 推荐：使用启动脚本（自动检查依赖和初始化数据库）
python start.py

# 或者直接启动应用（需要手动初始化数据库）
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

### 变更迁移
- 新增了 `mobile` 字段，并将 `email` 改为可空；已有数据库请执行：
```bash
python scripts/migrate_add_user_fields.py
```
该脚本会：
- 自动添加 `mobile` 列并创建唯一索引
- 将 `email` 改为可空（SQLite 采用表重建方式）

- 新增了 `history` 表，已有数据库请执行：
```bash
python scripts/migrate_add_history_table.py
```

- 新增了 `app_releases` 表，已有数据库请执行：
```bash
python scripts/migrate_add_releases_table.py
```

- 将 `history` 表中的 `user_id` 字段重命名为 `user`（参考charts表设计），已有数据库请执行：
```bash
python scripts/migrate_rename_user_id_to_user.py
```

- 将 `history` 表中的 `scope` 字段重命名为 `score`，已有数据库请执行：
```bash
python scripts/migrate_rename_scope_to_score.py
```

- 从 `my_user` 表中移除了 `score` 字段，已有数据库请执行：
```bash
python scripts/migrate_drop_user_score.py
```

- 将 `my_user` 表中的 `experence` 字段重命名为 `experience`，已有数据库请执行：
```bash
python scripts/migrate_rename_experence_to_experience.py
```

### 最新更新（2024年版本）
- **排行榜优化**: Charts API 排行榜现在按成绩升序排列（分数越低排名越高）
- **过滤增强**: 排行榜支持按 `title` 参数过滤特定标题的成绩记录
- **排名算法**: 更新排名计算逻辑，适配升序排序规则

### 静态文件/上传
- 图片：
  - 目录：`uploads/images/`
  - 访问：
    - 新路径：`/uploads/images/<filename>`
    - 兼容旧路径：`/static/images/<filename>`（映射到同一目录）
- APK：
  - 目录：`uploads/apk/`
  - 访问：`/uploads/apk/<filename>`

### 3. 应用地址

根据不同的启动方式：
- **推荐方式**：使用 `python start.py` 启动，应用将在 `http://localhost:5000` 运行
- **开发方式**：使用 `python app.py` 启动，应用将在 `http://localhost:8000` 运行
- **健康检查端点**：`http://localhost:5000/health` 或 `http://localhost:8000/health`

> 注意：如果5000端口被占用（如被AirPlay Receiver占用），建议使用8000端口或者在系统偏好设置->共享中关闭AirPlay接收器服务。

### 4. 测试脚本

项目提供了完整的测试脚本来验证功能：

```bash
# 测试基础History API功能
python test_history_api.py

# 测试排行榜和统计功能
python test_leaderboard_api.py

# 测试用户信息返回完整性
python test_user_info.py

# 添加测试数据
python add_history_data.py

# 查看数据统计
python check_history_data.py
```

#### 测试数据说明
- `add_history_data.py`: 为4个用户添加28条测试记录，包含不同分数段
- `check_history_data.py`: 查看当前数据库中的历史记录和排行榜
- 所有测试脚本都会自动清理测试数据，不影响生产环境

## API 接口

### 分页约定
- **查询参数**：`page`（默认 1），`per_page`（默认 10 或 20，视接口而定，最大 100 或 200）。
- **返回结构**：列表接口返回如下结构（不同接口会携带额外字段，如 `message`、`period` 等）：
```json
{
  "message": "获取列表成功",
  "data": [/* 列表数据 */],
  "pagination": { "page": 1, "per_page": 20, "total": 123, "pages": 7 }
}
```

### 用户 API (`/users`)

- `GET /users` - 获取所有用户
  - 分页：`page`、`per_page`
  - 排序：`sort_by`（支持 `username`、`email`、`mobile`、`experience`、`boluo`、`isActive`、`admin`、`sex`、`birthday`、`createdAt`、`updatedAt`）、`order`（`asc`/`desc`）
  - 模糊搜索：`keyword` 或 `q`（对 `username`、`email`、`mobile` 进行不区分大小写匹配）
- `GET /users/count` - 获取用户总数
- `GET /users/<object_id>` - 获取单个用户
- `POST /users` - 创建用户（后台管理）
  - 必填：`username`、`password`
  - 二选一：`email` 或 `mobile`
  - 可选：`avatar`、`bio`、`experience`、`boluo`、`isActive`、`admin`、`sex`、`birthday`
- `POST /users/register` - 注册用户（安卓/客户端）
  - 必填：`password`
  - 二选一：`email` 或 `mobile`
  - 自动：`username`（服务端按“形容词+名词+时间戳后6位”生成，并保证唯一）
- `POST /users/login` - 用户登录
  - 方式一：`email` + `password`
  - 方式二：`mobile` + `password`
- `PUT /users/<object_id>` - 更新用户
- `DELETE /users/<object_id>` - 删除用户
- `POST /users/<object_id>/experience` - 更新用户经验值
- `POST /users/<object_id>/boluo` - 更新用户菠萝币

#### 示例
- 列表模糊搜索
```
GET /users?keyword=cat
GET /users?q=138
```

### 图表 API (`/charts`)

- `GET /charts` - 获取图表列表
  - 分页：`page`、`per_page`
  - 过滤：`user`
  - 排序：`sort_by`（`objectId`、`title`、`achievement`、`user`、`createdAt`、`updatedAt`），`order`（`asc`/`desc`）
- `GET /charts/<object_id>` - 获取单个图表
- `POST /charts` - 创建图表
- `PUT /charts/<object_id>` - 更新图表
- `DELETE /charts/<object_id>` - 删除图表
- `GET /charts/leaderboard` - 获取排行榜（按成绩值升序排序，支持分页）
  - 分页：`page`、`per_page`
  - 过滤：`title`（可选）：筛选特定标题的排行榜
- `GET /charts/rank` - 根据 `title` 与 `achievement` 查询排名
  - 必填：`title`、`achievement`
  - 可选：`scope=global|title`（默认 `global`）
  - 说明：按 `achievement` 升序，排名 = 比该分数更低的数量 + 1（同分并列）
  - 示例：`/charts/rank?title=Speed%20Run&achievement=123.45&scope=title`
- `GET /charts/user-rank` - 根据用户ID和标题查询用户成绩和排名
  - 必填：`user`（用户ID）、`title`（标题）
  - 返回：用户完整信息、成绩、排名、同分数量、总记录数
  - 说明：按 `achievement` 升序排序，分数越低排名越高
- `POST /charts/<object_id>/achievement` - 更新图表成绩值

#### Charts API 使用示例
```bash
# 获取全局排行榜（所有标题，按成绩升序）
curl "http://localhost:5000/charts/leaderboard?page=1&per_page=10"

# 获取特定标题的排行榜
curl "http://localhost:5000/charts/leaderboard?title=数学计算&page=1&per_page=5"

# 查询用户在特定标题中的排名
curl "http://localhost:5000/charts/rank?title=数学计算&achievement=85.5&scope=title"

# 查询用户在全局排行榜中的排名
curl "http://localhost:5000/charts/rank?title=数学计算&achievement=85.5&scope=global"

# 查询特定用户在指定标题下的成绩和排名
curl "http://localhost:5000/charts/user-rank?user=user123&title=数学计算"
```

#### 用户排名查询响应格式
```json
{
  "success": true,
  "data": {
    "user_info": {
      "objectId": "user123",
      "username": "玩家张三",
      "avatar": "avatar.jpg",
      "bio": "我是游戏爱好者",
      "experience": 1500,
      "boluo": 200,
      "isActive": true,
      "admin": false,
      "sex": 1,
      "birthday": "1995-06-15",
      "createdAt": "2024-01-01T00:00:00",
      "updatedAt": "2024-01-15T12:30:00"
    },
    "achievement": 85.5,
    "rank": 3,
    "title": "数学计算",
    "total_records": 50,
    "ties_count": 2,
    "record": {
      "objectId": "chart456",
      "title": "数学计算",
      "achievement": 85.5,
      "user": { /* 同上user_info */ },
      "createdAt": "2024-01-10T14:20:00",
      "updatedAt": "2024-01-10T14:20:00"
    }
  }
}
```

### 论坛 API (`/forum`)

- `GET /forum` - 获取帖子列表
  - 分页：`page`、`per_page`
  - 过滤：`category`、`user`、`isPinned`（`true|false`）、`public`（`true|false`）
  - 排序：置顶优先（`isPinned` 降序），其后按 `createdAt` 降序
- `GET /forum/<object_id>` - 获取单个帖子
- `GET /forum/categories` - 获取所有帖子分类（支持分页）
  - 分页：`page`、`per_page`
- `GET /forum/popular` - 获取热门帖子（支持分页）
  - 分页：`page`、`per_page`
  - 排序：`sort_by=viewCount|likeCount`
- `GET /forum/public` - 获取公开帖子（支持分页）
  - 分页：`page`、`per_page`
- `POST /forum` - 创建帖子
- `PUT /forum/<object_id>` - 更新帖子
- `POST /forum/<object_id>/like` - 点赞
- `DELETE /forum/<object_id>` - 删除帖子

### 图片 API (`/images`)

- `GET /images` - 获取图片列表
  - 分页：`page`、`per_page`
  - 排序：`sort_by`（支持 `fileName`、`fileSize`、`createdAt`、`updatedAt`）、`order`（`asc`/`desc`）
- `GET /images/<object_id>` - 获取单个图片
- `GET /images/stats` - 获取图片统计信息（总数量、总大小）
- `GET /images/search` - 按文件名搜索
  - 参数：`q`
  - 分页：`page`、`per_page`
- `POST /images` - 创建图片记录（JSON方式）
- `PUT /images/<object_id>` - 更新图片信息
- `DELETE /images/<object_id>` - 删除图片
- `POST /images/upload` - 上传单个图片文件（multipart/form-data，字段名：`file`）
- `POST /images/upload/multiple` - 批量上传图片文件（multipart/form档），字段名：`files`

### 发布版本 API (`/releases`)

- `GET /releases` - 获取发布记录列表
  - 分页：`page`、`per_page`
  - 过滤：`app_name`、`environment`、`status`
  - 排序：按创建时间倒序
- `GET /releases/count` - 获取发布记录数量（支持同样的过滤）
- `GET /releases/<object_id>` - 获取单个发布记录
- `POST /releases` - 创建发布记录
  - 必填：`app_name`、`version_name`、`version_code`
  - 可选：`changelog`、`download_url`、`environment`（默认 `production`）、`status`（默认 `published`）、`is_update`、`force_update`
- `PUT /releases/<object_id>` - 更新发布记录
- `DELETE /releases/<object_id>` - 删除发布记录
- `POST /releases/upload-apk` - 上传 APK 文件（multipart/form-data）
  - 字段：`file`（必填，.apk）、`release_id`（可选；若提供，将自动回写该记录的 `download_url`）

#### 发布版本示例
```bash
# 创建发布记录
curl -X POST "http://localhost:5000/releases/" \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "SuperSpeedCalc",
    "version_name": "1.0.0",
    "version_code": 100,
    "changelog": "初始化发布",
    "is_update": true,
    "force_update": false
  }'

# 上传 APK 并绑定到发布记录（release_id 为创建返回的 objectId）
curl -X POST "http://localhost:5000/releases/upload-apk?release_id=<objectId>" \
  -F "file=@/path/to/app-release.apk"

# 仅上传 APK，不绑定记录（可得到文件 URL，之后手动写入）
curl -X POST "http://localhost:5000/releases/upload-apk" \
  -F "file=@/path/to/app-release.apk"
```

### 历史记录 API (`/history`)

#### 基础操作
- `GET /history` - 获取历史记录列表
  - 分页：`page`、`per_page`
  - 过滤：`user`（按用户ID过滤）
  - 排序：按创建时间倒序
  - 返回：包含完整的用户信息（用户名、头像、经验等）
- `GET /history/count` - 获取历史记录总数
  - 可选：`user`（按用户ID统计）
- `GET /history/<object_id>` - 获取单个历史记录
  - 返回：包含完整的用户信息
- `POST /history` - 创建历史记录
  - 必填：`title`、`score`、`user`
  - 说明：`score` 必须为整数，可以为正数或负数
- `PUT /history/<object_id>` - 更新历史记录
  - 可选：`title`、`score`、`user`
- `DELETE /history/<object_id>` - 删除历史记录

#### 排行榜功能
- `GET /history/leaderboard` - 获取用户得分排行榜（基于历史记录分数总和）
  - 分页：`page`、`per_page`
  - 时间段：`period`（`all`=总榜，`daily`=日榜，`monthly`=月榜，`yearly`=年榜）
  - 返回：用户排名、总分、历史记录数量，包含完整的用户信息
  - 算法：基于历史记录 `score` 字段的总和进行排序，支持正负数计算

#### 用户统计
- `GET /history/stats` - 获取用户历史分数统计信息
  - 必填：`user`
  - 返回：今日、本月、今年、总计的分数、记录数量与对应榜单排名（`rank`），包含完整的用户信息。
  - 说明：当某周期用户无任何记录时，该周期的 `rank` 返回 `null`。
  - 时间计算：基于UTC时间，日榜从当天00:00:00开始，月榜从当月1号开始，年榜从当年1月1日开始

#### 使用示例
```bash
# 创建历史记录
curl -X POST "http://localhost:5000/history/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "超级速度计算挑战",
    "score": 1500,
    "user": "user123"
  }'

# 获取总排行榜
curl "http://localhost:5000/history/leaderboard?period=all"

# 获取日榜
curl "http://localhost:5000/history/leaderboard?period=daily"

# 获取用户统计
curl "http://localhost:5000/history/stats?user=user123"

# 获取用户历史记录
curl "http://localhost:5000/history/?user=user123"
```

## History功能使用指南

### 🚀 快速开始

1. **创建历史记录**
   ```bash
   curl -X POST "http://localhost:5000/history/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "游戏挑战",
       "score": 1000,
       "user": "user123"
     }'
   ```

2. **查看排行榜**
   ```bash
   # 总排行榜
   curl "http://localhost:5000/history/leaderboard?period=all"
   
   # 日榜
   curl "http://localhost:5000/history/leaderboard?period=daily"
   
   # 月榜
   curl "http://localhost:5000/history/leaderboard?period=monthly"
   
   # 年榜
   curl "http://localhost:5000/history/leaderboard?period=yearly"
   ```

3. **获取用户统计**
   ```bash
   curl "http://localhost:5000/history/stats?user=user123"
   ```

### 📊 数据格式说明

#### 历史记录结构
```json
{
  "objectId": "abc123def",
  "title": "游戏挑战",
  "score": 1000,
  "user": {
    "objectId": "user123",
    "username": "玩家1",
    "avatar": "avatar.jpg",
    "experience": 100,
    "boluo": 50,
    "isActive": true,
    "admin": false,
    "sex": 1,
    "birthday": "1990-01-01",
    "createdAt": "2024-01-01T00:00:00",
    "updatedAt": "2024-01-01T00:00:00"
  },
  "createdAt": "2024-01-01T12:00:00",
  "updatedAt": "2024-01-01T12:00:00"
}
```

#### 排行榜结构
```json
{
  "message": "获取all排行榜成功",
  "data": [
    {
      "rank": 1,
      "total_score": 5000,
      "history_count": 5,
      "user": {
        "objectId": "user123",
        "username": "玩家1",
        "avatar": "avatar.jpg",
        "experience": 100,
        "boluo": 50
      }
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 10,
    "pages": 1,
    "has_next": false,
    "has_prev": false
  },
  "period": "all"
}
```

#### 用户统计结构
```json
{
  "message": "获取用户历史分数统计成功",
  "data": {
    "user": {
      "objectId": "user123",
      "username": "玩家1",
      "avatar": "avatar.jpg"
    },
    "stats": {
      "today": { "total_score": 1000, "count": 2, "rank": 3 },
      "month": { "total_score": 3000, "count": 8, "rank": 5 },
      "year": { "total_score": 5000, "count": 15, "rank": 7 },
      "total": { "total_score": 5000, "count": 15, "rank": 9 }
    }
  }
}
```

### 🔧 高级功能

#### 分页查询
```bash
# 获取第2页，每页10条记录
curl "http://localhost:5000/history/?page=2&per_page=10"

# 获取排行榜第1页，每页5条记录
curl "http://localhost:5000/history/leaderboard?period=all&page=1&per_page=5"
```

#### 用户过滤
```bash
# 获取特定用户的历史记录
curl "http://localhost:5000/history/?user=user123"

# 获取特定用户的历史记录数量
curl "http://localhost:5000/history/count?user=user123"
```

### 🎮 应用场景

- **游戏排行榜**: 实时显示玩家排名和分数
- **成就系统**: 记录玩家的游戏成就和进步
- **数据分析**: 分析玩家的游戏习惯和表现
- **社交功能**: 展示玩家的游戏历史和成就
- **竞赛系统**: 支持各种时间段的竞赛排名

### 📈 性能优化

- **SQL聚合查询**: 使用数据库层面的GROUP BY和SUM进行高效统计
- **分页机制**: 支持灵活的分页查询，避免大量数据传输
- **索引优化**: 为外键字段和查询频繁字段建立合理索引
- **缓存友好**: API设计考虑缓存策略，支持条件查询减少数据量
- **排序优化**: 排行榜查询使用数据库原生排序，性能优异
- **并发处理**: Flask多线程支持，适合中等并发场景

## 项目总结

### 🎯 项目特点
- **模块化设计**: 蓝图模块化架构，清晰的目录结构和代码组织
- **RESTful API**: 标准的REST API设计，完整的CRUD操作
- **智能用户系统**: 自动生成用户名、双重登录方式（邮箱/手机号）
- **完整功能覆盖**: 用户管理、排行榜、社区、文件上传、版本发布一应俱全
- **灵活排行榜系统**: 支持升序排序、多标题过滤、精确排名计算
- **多维度统计**: 日/月/年/总榜多时间维度，实时统计分析
- **数据完整性**: 外键关联、级联删除、数据校验等数据库最佳实践
- **高性能查询**: SQL聚合查询、分页支持、索引优化
- **扩展性强**: 支持数据库迁移、环境配置、一键部署

### 🚀 技术栈
- **后端框架**: Flask 2.3.3 + Flask-SQLAlchemy 3.0.5
- **跨域支持**: Flask-CORS 4.0.0
- **数据库**: SQLite（默认），支持 MySQL（使用 PyMySQL）
- **密码加密**: Werkzeug 安全模块
- **API设计**: RESTful风格，蓝图模块化架构
- **数据格式**: JSON，完整的分页和错误处理
- **文件处理**: 支持图片（PNG/JPG）和APK文件上传存储
- **配置管理**: 支持环境变量配置和多环境部署

### 📊 数据模型
- **用户模型 (MyUser)**: 完整的用户信息管理，支持经验值、菠萝币、权限控制
- **图表模型 (Charts)**: 成绩记录和排行榜系统
- **论坛模型 (Forum)**: 社区帖子管理，支持分类、标签、互动统计
- **图片模型 (Image)**: 文件上传管理，自动生成访问URL
- **历史记录模型 (History)**: 用户游戏历史，支持多维度统计分析
- **发布模型 (AppRelease)**: 应用版本发布管理，支持更新控制

### 🔧 开发工具
- **测试脚本**: 完整的API测试覆盖（`test_*.py`）
- **数据迁移**: 多个迁移脚本支持数据库结构平滑升级（`scripts/migrate_*.py`）
- **数据库管理**: 专用的数据库管理工具（`manage_db.py`）
- **启动脚本**: 智能启动脚本，自动检查依赖和初始化（`start.py`）
- **数据填充**: 测试数据生成和统计工具（`add_history_data.py`、`check_history_data.py`）
- **文档完善**: 详细的API文档和使用指南，包含完整的curl示例

### 🎮 应用场景
- **游戏平台**: 用户管理、排行榜、成就系统
- **社交应用**: 论坛、图片分享、用户互动
- **数据分析**: 用户行为分析、统计报表
- **竞赛系统**: 多维度排行榜、实时统计

### 📈 项目优势
- **生产就绪**: 完整的错误处理、健康检查端点、配置管理
- **性能优化**: SQL聚合查询、分页机制、索引设计
- **安全特性**: 密码哈希存储、数据校验、SQL注入防护
- **易于部署**: 支持Docker部署、环境变量配置、一键启动
- **维护友好**: 详细的日志输出、清晰的代码结构、完善的文档
- **可扩展性**: 模块化设计支持轻松添加新功能和API端点

---

## 🎉 项目总结

SuperSpeedCalc Server 是一个功能完整、架构清晰的后端服务项目。通过 Flask + SQLAlchemy 构建，提供了用户管理、排行榜、社区论坛、文件上传、历史记录统计等核心功能。项目采用蓝图模块化设计，支持多种数据库，具有良好的扩展性和维护性。

### 🌟 核心亮点
- **完整的用户体系**：支持邮箱/手机号注册登录，自动生成用户名，经验值和积分系统
- **强大的统计功能**：多维度排行榜（日/月/年/总榜），实时用户统计分析
- **全面的内容管理**：论坛社区、图片上传、版本发布一应俱全
- **开发友好**：完整的测试脚本、数据迁移工具、详细的API文档

### 📞 技术支持
如果您在使用过程中遇到问题，请参考：
1. **API文档**：详细的接口说明和示例
2. **测试脚本**：`test_*.py` 文件提供完整的功能验证
3. **数据库管理**：`manage_db.py` 提供数据库操作工具
4. **启动脚本**：`start.py` 提供智能启动和依赖检查

### 🚀 生产环境部署建议

#### 基本部署配置
```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 设置环境变量
export FLASK_ENV=production
export SECRET_KEY=your_secret_key_here

# 3. 初始化数据库
python manage_db.py init

# 4. 启动服务
python start.py
```

#### 性能优化建议
- **Web服务器**: 生产环境建议使用 Gunicorn + Nginx
- **数据库**: 大数据量场景建议使用 MySQL 替代 SQLite
- **静态文件**: 配置 Nginx 直接服务静态文件，减轻应用服务器负担
- **缓存策略**: 可集成 Redis 进行排行榜和热门内容缓存
- **监控日志**: 集成日志系统，监控API性能和错误

#### 安全配置
- 生产环境需注释掉 `app.py` 第18行的 `CORS(app)` 
- 配置合适的CORS策略和安全头
- 使用HTTPS协议保护数据传输
- 定期更新依赖包版本

项目持续更新维护中，欢迎使用！ 🚀