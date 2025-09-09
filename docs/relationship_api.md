# 用户关系 API

## 基础信息
- **基础路径**: `/users`
- **数据表**: `user_relationships`
- **主要功能**: 用户关注/取消关注、粉丝列表、互关列表

## 接口列表

### 1. 关注用户
**POST** `/users/{user_id}/follow/{target_user_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 关注者用户ID |
| target_user_id | int | 是 | 被关注者用户ID |

#### 请求示例
```bash
POST /users/1/follow/2
```

#### 响应示例
```json
{
  "code": 201,
  "message": "关注成功",
  "data": "{\"follower\": 1, \"followed\": 2, \"created_at\": \"2025-01-09T10:00:00\"}"
}
```

### 2. 取消关注
**DELETE** `/users/{user_id}/unfollow/{target_user_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 关注者用户ID |
| target_user_id | int | 是 | 被关注者用户ID |

#### 请求示例
```bash
DELETE /users/1/unfollow/2
```

#### 响应示例
```json
{
  "code": 200,
  "message": "取消关注成功",
  "data": null
}
```

### 3. 获取粉丝列表
**GET** `/users/{user_id}/followers`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |

#### 请求示例
```bash
GET /users/1/followers?page=1&per_page=20
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取粉丝列表成功",
  "data": "{\"list\": [{\"id\": 2, \"username\": \"user2\", \"avatar\": \"https://example.com/avatar2.jpg\", \"bio\": \"用户2的简介\", \"followed_at\": \"2025-01-09T10:00:00\"}], \"pagination\": {\"page\": 1, \"per_page\": 20, \"total\": 1, \"pages\": 1, \"has_next\": false, \"has_prev\": false}}"
}
```

### 4. 获取关注列表
**GET** `/users/{user_id}/following`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |

#### 请求示例
```bash
GET /users/1/following?page=1&per_page=20
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取关注列表成功",
  "data": "{\"list\": [{\"id\": 3, \"username\": \"user3\", \"avatar\": \"https://example.com/avatar3.jpg\", \"bio\": \"用户3的简介\", \"followed_at\": \"2025-01-09T10:00:00\"}], \"pagination\": {\"page\": 1, \"per_page\": 20, \"total\": 1, \"pages\": 1, \"has_next\": false, \"has_prev\": false}}"
}
```

### 5. 获取互关列表
**GET** `/users/{user_id}/mutual`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |

#### 请求示例
```bash
GET /users/1/mutual?page=1&per_page=20
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取互关列表成功",
  "data": "{\"list\": [{\"id\": 4, \"username\": \"user4\", \"avatar\": \"https://example.com/avatar4.jpg\", \"bio\": \"用户4的简介\", \"followed_at\": \"2025-01-09T10:00:00\"}], \"pagination\": {\"page\": 1, \"per_page\": 20, \"total\": 1, \"pages\": 1, \"has_next\": false, \"has_prev\": false}}"
}
```

### 6. 检查关注状态
**GET** `/users/{user_id}/follow-status/{target_user_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户ID |
| target_user_id | int | 是 | 目标用户ID |

#### 请求示例
```bash
GET /users/1/follow-status/2
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取关注状态成功",
  "data": "{\"is_following\": true, \"is_followed_by\": false, \"is_mutual\": false}"
}
```

### 7. 获取用户关系统计
**GET** `/users/{user_id}/relationship-stats`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户ID |

#### 请求示例
```bash
GET /users/1/relationship-stats
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取用户关系统计成功",
  "data": "{\"followers_count\": 10, \"following_count\": 5, \"mutual_count\": 3}"
}
```

### 8. 批量关注用户
**POST** `/users/{user_id}/follow/batch`

#### 请求体
```json
{
  "target_user_ids": [2, 3, 4]
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| target_user_ids | array | 是 | 要关注的用户ID数组 |

#### 请求示例
```bash
curl -X POST http://localhost:5000/users/1/follow/batch \
  -H "Content-Type: application/json" \
  -d '{"target_user_ids": [2, 3, 4]}'
```

#### 响应示例
```json
{
  "code": 201,
  "message": "批量关注成功",
  "data": "{\"success_count\": 3, \"failed_count\": 0, \"results\": [{\"target_user_id\": 2, \"status\": \"success\"}, {\"target_user_id\": 3, \"status\": \"success\"}, {\"target_user_id\": 4, \"status\": \"success\"}]}"
}
```

### 9. 获取推荐关注用户
**GET** `/users/{user_id}/recommendations`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户ID |
| limit | int | 否 | 推荐数量，默认10 |

#### 请求示例
```bash
GET /users/1/recommendations?limit=10
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取推荐用户成功",
  "data": "{\"recommendations\": [{\"id\": 5, \"username\": \"user5\", \"avatar\": \"https://example.com/avatar5.jpg\", \"bio\": \"用户5的简介\", \"mutual_friends\": 2, \"reason\": \"mutual_friends\"}, {\"id\": 6, \"username\": \"user6\", \"avatar\": \"https://example.com/avatar6.jpg\", \"bio\": \"用户6的简介\", \"mutual_friends\": 1, \"reason\": \"mutual_friends\"}]}"
}
```

## 错误响应

### 常见错误码
- `USER_NOT_FOUND`: 用户不存在
- `TARGET_USER_NOT_FOUND`: 目标用户不存在
- `CANNOT_FOLLOW_SELF`: 不能关注自己
- `ALREADY_FOLLOWING`: 已经关注该用户
- `NOT_FOLLOWING`: 未关注该用户
- `FOLLOW_FAILED`: 关注失败
- `UNFOLLOW_FAILED`: 取消关注失败

### 错误响应示例
```json
{
  "code": 400,
  "message": "不能关注自己"
}
```

## 数据模型

### UserRelationship 表结构
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键ID |
| follower | int | 关注者用户ID |
| followed | int | 被关注者用户ID |
| created_at | datetime | 关注时间 |

### 关系说明
- `follower`: 关注者（主动关注的人）
- `followed`: 被关注者（被关注的人）
- 一个用户可以关注多个用户
- 一个用户可以被多个用户关注
- 支持互相关注（互关）
