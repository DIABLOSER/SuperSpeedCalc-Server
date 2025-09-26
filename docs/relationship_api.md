# 用户关系管理 API

## 基础信息
- **基础路径**: `/users`
- **数据表**: `user_relationships`
- **主要功能**: 用户关注/取消关注、粉丝管理、互相关注查询

## 接口列表

### 1. 关注用户
**POST** `/users/{user_id}/follow/{target_user_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 关注者用户ID |
| target_user_id | string | 是 | 被关注者用户ID |

#### 请求示例
```bash
POST /users/user123/follow/user456
```

#### 响应示例
```json
{
  "code": 200,
  "message": "user123 is now following user456",
  "data": {
    "follower": {
      "objectId": "user123",
      "username": "user123"
    },
    "followed": {
      "objectId": "user456",
      "username": "user456"
    },
    "relationship_id": "rel_789",
    "createdAt": "2025-01-09T10:00:00"
  }
}
```

### 2. 取消关注用户
**DELETE** `/users/{user_id}/follow/{target_user_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 关注者用户ID |
| target_user_id | string | 是 | 被关注者用户ID |

#### 请求示例
```bash
DELETE /users/user123/follow/user456
```

#### 响应示例
```json
{
  "code": 200,
  "message": "user123 has unfollowed user456",
  "data": {
    "follower": {
      "objectId": "user123",
      "username": "user123"
    },
    "unfollowed": {
      "objectId": "user456",
      "username": "user456"
    }
  }
}
```

### 3. 获取用户粉丝列表
**GET** `/users/{user_id}/followers`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 用户ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |

#### 请求示例
```bash
GET /users/user123/followers?page=1&per_page=20
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取粉丝列表成功",
  "data": {
    "user": {
      "objectId": "user123",
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "followers": [
      {
        "objectId": "follower1",
        "username": "follower_user1",
        "avatar": "https://example.com/avatar1.jpg",
        "bio": "用户简介"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 1,
      "pages": 1
    }
  }
}
```

### 4. 获取用户关注列表
**GET** `/users/{user_id}/following`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 用户ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |

#### 请求示例
```bash
GET /users/user123/following?page=1&per_page=20
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取关注列表成功",
  "data": {
    "user": {
      "objectId": "user123",
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "following": [
      {
        "objectId": "following1",
        "username": "following_user1",
        "avatar": "https://example.com/avatar1.jpg",
        "bio": "用户简介"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 1,
      "pages": 1
    }
  }
}
```

### 5. 获取互相关注列表
**GET** `/users/{user_id}/mutual`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 用户ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |

#### 请求示例
```bash
GET /users/user123/mutual?page=1&per_page=20
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取互相关注列表成功",
  "data": {
    "user": {
      "objectId": "user123",
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "mutual_followers": [
      {
        "objectId": "mutual1",
        "username": "mutual_user1",
        "avatar": "https://example.com/avatar1.jpg",
        "bio": "用户简介",
        "experience": 100
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 1,
      "pages": 1
    },
    "stats": {
      "mutual_count": 1,
      "followers_count": 5,
      "following_count": 3
    }
  }
}
```

### 6. 检查关注关系
**GET** `/users/{user_id}/follow/{target_user_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 用户ID |
| target_user_id | string | 是 | 目标用户ID |

#### 请求示例
```bash
GET /users/user123/follow/user456
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取关注关系成功",
  "data": {
    "user": {
      "objectId": "user123",
      "username": "user123"
    },
    "target_user": {
      "objectId": "user456",
      "username": "user456"
    },
    "relationship": {
      "is_following": true,
      "is_followed_by": false,
      "mutual": false
    }
  }
}
```

## 数据表结构

### User Relationships 表字段
| 字段名 | 类型 | 说明 |
|--------|------|------|
| objectId | string | 主键ID |
| follower | string | 关注者用户ID |
| following | string | 被关注者用户ID |
| createdAt | datetime | 关注时间 |
| updatedAt | datetime | 更新时间 |

## 错误响应

### 常见错误码
- `404`: 用户不存在
- `400`: 已经关注该用户
- `400`: 未关注该用户
- `400`: 不能关注自己
- `400`: 不能取消关注自己

### 错误响应示例
```json
{
  "code": 404,
  "message": "Not found"
}
```

```json
{
  "code": 400,
  "message": "Cannot follow yourself"
}
```

```json
{
  "code": 400,
  "message": "Already following this user"
}
```

```json
{
  "code": 400,
  "message": "Not following this user"
}
```

## 注意事项

1. **关注限制**：
   - 用户不能关注自己
   - 不能重复关注同一用户

2. **关系查询**：
   - 支持分页查询粉丝和关注列表
   - 提供互相关注查询功能

3. **数据一致性**：
   - 关注和取消关注操作是原子性的
   - 删除用户时会自动清理相关关系
