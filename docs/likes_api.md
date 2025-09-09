# 点赞功能 API

## 基础信息
- **基础路径**: `/posts`
- **数据表**: `likes`
- **主要功能**: 帖子点赞、取消点赞、点赞统计、点赞用户列表

## 接口列表

### 1. 点赞帖子
**POST** `/posts/{post_id}/like`

#### 请求体
```json
{
  "user_id": 2
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 点赞用户ID |

#### 请求示例
```bash
curl -X POST http://localhost:5000/posts/1/like \
  -H "Content-Type: application/json" \
  -d '{"user_id": 2}'
```

#### 响应示例
```json
{
  "code": 201,
  "message": "点赞成功",
  "data": "{\"post_id\": 1, \"user_id\": 2, \"liked_at\": \"2025-01-09T10:00:00\"}"
}
```

### 2. 取消点赞
**DELETE** `/posts/{post_id}/unlike`

#### 请求体
```json
{
  "user_id": 2
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 取消点赞用户ID |

#### 请求示例
```bash
curl -X DELETE http://localhost:5000/posts/1/unlike \
  -H "Content-Type: application/json" \
  -d '{"user_id": 2}'
```

#### 响应示例
```json
{
  "code": 200,
  "message": "取消点赞成功",
  "data": null
}
```

### 3. 获取帖子点赞用户列表
**GET** `/posts/{post_id}/likers`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| post_id | int | 是 | 帖子ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |
| viewer_id | int | 否 | 查看者用户ID（用于权限控制） |

#### 请求示例
```bash
GET /posts/1/likers?page=1&per_page=20&viewer_id=1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取点赞用户列表成功",
  "data": "{\"list\": [{\"id\": 2, \"username\": \"user2\", \"avatar\": \"https://example.com/avatar2.jpg\", \"bio\": \"用户2的简介\", \"liked_at\": \"2025-01-09T10:00:00\"}], \"pagination\": {\"page\": 1, \"per_page\": 20, \"total\": 1, \"pages\": 1, \"has_next\": false, \"has_prev\": false}}"
}
```

### 4. 获取用户点赞的帖子列表
**GET** `/posts/liked-by/{user_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |

#### 请求示例
```bash
GET /posts/liked-by/2?page=1&per_page=20
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取用户点赞帖子成功",
  "data": "{\"list\": [{\"objectId\": 1, \"title\": \"我的第一篇帖子\", \"content\": \"这是帖子内容\", \"user\": 1, \"user_info\": {\"id\": 1, \"username\": \"test_user\", \"avatar\": \"https://example.com/avatar.jpg\"}, \"category\": \"技术\", \"status\": \"published\", \"audit_state\": \"approved\", \"likes\": 10, \"views\": 100, \"liked_at\": \"2025-01-09T10:00:00\"}], \"pagination\": {\"page\": 1, \"per_page\": 20, \"total\": 1, \"pages\": 1, \"has_next\": false, \"has_prev\": false}}"
}
```

### 5. 检查点赞状态
**GET** `/posts/{post_id}/like-status/{user_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| post_id | int | 是 | 帖子ID |
| user_id | int | 是 | 用户ID |

#### 请求示例
```bash
GET /posts/1/like-status/2
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取点赞状态成功",
  "data": "{\"is_liked\": true, \"liked_at\": \"2025-01-09T10:00:00\"}"
}
```

### 6. 获取帖子点赞统计
**GET** `/posts/{post_id}/like-stats`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| post_id | int | 是 | 帖子ID |

#### 请求示例
```bash
GET /posts/1/like-stats
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取点赞统计成功",
  "data": "{\"total_likes\": 10, \"likes_today\": 2, \"likes_this_week\": 5, \"likes_this_month\": 8}"
}
```

### 7. 批量点赞
**POST** `/posts/like/batch`

#### 请求体
```json
{
  "user_id": 2,
  "post_ids": [1, 2, 3]
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 点赞用户ID |
| post_ids | array | 是 | 要点赞的帖子ID数组 |

#### 请求示例
```bash
curl -X POST http://localhost:5000/posts/like/batch \
  -H "Content-Type: application/json" \
  -d '{"user_id": 2, "post_ids": [1, 2, 3]}'
```

#### 响应示例
```json
{
  "code": 201,
  "message": "批量点赞成功",
  "data": "{\"success_count\": 3, \"failed_count\": 0, \"results\": [{\"post_id\": 1, \"status\": \"success\"}, {\"post_id\": 2, \"status\": \"success\"}, {\"post_id\": 3, \"status\": \"success\"}]}"
}
```

### 8. 获取热门帖子（按点赞数）
**GET** `/posts/popular`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |
| period | string | 否 | 时间周期：today/week/month/all，默认all |

#### 请求示例
```bash
GET /posts/popular?page=1&per_page=20&period=week
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取热门帖子成功",
  "data": "{\"list\": [{\"objectId\": 1, \"title\": \"我的第一篇帖子\", \"content\": \"这是帖子内容\", \"user\": 1, \"user_info\": {\"id\": 1, \"username\": \"test_user\", \"avatar\": \"https://example.com/avatar.jpg\"}, \"category\": \"技术\", \"status\": \"published\", \"audit_state\": \"approved\", \"likes\": 100, \"views\": 1000, \"createdAt\": \"2025-01-09T10:00:00\"}], \"pagination\": {\"page\": 1, \"per_page\": 20, \"total\": 1, \"pages\": 1, \"has_next\": false, \"has_prev\": false}, \"period\": \"week\"}"
}
```

### 9. 获取用户点赞统计
**GET** `/posts/user/{user_id}/like-stats`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户ID |

#### 请求示例
```bash
GET /posts/user/2/like-stats
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取用户点赞统计成功",
  "data": "{\"total_likes_given\": 50, \"total_likes_received\": 100, \"likes_today\": 5, \"likes_this_week\": 20, \"likes_this_month\": 80}"
}
```

## 错误响应

### 常见错误码
- `POST_NOT_FOUND`: 帖子不存在
- `USER_NOT_FOUND`: 用户不存在
- `ALREADY_LIKED`: 已经点赞过
- `NOT_LIKED`: 未点赞过
- `POST_NOT_VISIBLE`: 帖子不可见
- `LIKE_FAILED`: 点赞失败
- `UNLIKE_FAILED`: 取消点赞失败
- `ACCESS_DENIED`: 访问被拒绝

### 错误响应示例
```json
{
  "code": 400,
  "message": "已经点赞过",
  "data": null,
  "error_code": "ALREADY_LIKED",
  "details": "用户已经点赞过该帖子"
}
```

## 数据模型

### Likes 表结构
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键ID |
| post_id | int | 帖子ID |
| user_id | int | 点赞用户ID |
| created_at | datetime | 点赞时间 |

### 关系说明
- 一个用户可以点赞多个帖子
- 一个帖子可以被多个用户点赞
- 一个用户对同一个帖子只能点赞一次
- 支持取消点赞功能
