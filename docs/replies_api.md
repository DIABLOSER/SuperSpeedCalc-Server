# 回复功能 API

## 基础信息
- **基础路径**: `/replies`
- **数据表**: `replies`
- **主要功能**: 评论回复、两级评论系统、@用户功能

## 接口列表

### 1. 获取回复列表
**GET** `/replies`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |
| post_id | int | 否 | 帖子ID筛选 |
| user | int | 否 | 用户ID筛选 |
| parent_id | int | 否 | 父回复ID筛选（用于获取子回复） |

#### 请求示例
```bash
GET /replies?page=1&per_page=20&post_id=1&parent_id=null
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取回复列表成功",
  "data": {
    "list": [
      {
        "objectId": 1,
        "content": "这是一条评论",
        "post_id": 1,
        "user": 1,
        "user_info": {
          "id": 1,
          "username": "test_user",
          "avatar": "https://example.com/avatar.jpg"
        },
        "parent_id": null,
        "children": [
          {
            "objectId": 2,
            "content": "这是对评论的回复",
            "user": 2,
            "user_info": {
              "id": 2,
              "username": "user2",
              "avatar": "https://example.com/avatar2.jpg"
            },
            "parent_id": 1,
            "createdAt": "2025-01-09T10:05:00"
          }
        ],
        "likes": 5,
        "createdAt": "2025-01-09T10:00:00",
        "updatedAt": "2025-01-09T10:00:00"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 1,
      "pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
}
```

### 2. 获取单个回复
**GET** `/replies/{id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 回复ID |

#### 请求示例
```bash
GET /replies/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取回复成功",
  "data": {
    "objectId": 1,
    "content": "这是一条评论",
    "post_id": 1,
    "user": 1,
    "user_info": {
      "id": 1,
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "parent_id": null,
    "children": [
      {
        "objectId": 2,
        "content": "这是对评论的回复",
        "user": 2,
        "user_info": {
          "id": 2,
          "username": "user2",
          "avatar": "https://example.com/avatar2.jpg"
        },
        "parent_id": 1,
        "createdAt": "2025-01-09T10:05:00"
      }
    ],
    "likes": 5,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T10:00:00"
  }
}
```

### 3. 创建回复
**POST** `/replies`

#### 请求体
```json
{
  "content": "这是一条评论",
  "post_id": 1,
  "user": 1,
  "parent_id": null,
  "mentioned_users": [2, 3]
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| content | string | 是 | 回复内容 |
| post_id | int | 是 | 帖子ID |
| user | int | 是 | 回复用户ID |
| parent_id | int | 否 | 父回复ID（用于回复评论） |
| mentioned_users | array | 否 | @的用户ID数组 |

#### 响应示例
```json
{
  "code": 201,
  "message": "回复创建成功",
  "data": {
    "objectId": 1,
    "content": "这是一条评论",
    "post_id": 1,
    "user": 1,
    "user_info": {
      "id": 1,
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "parent_id": null,
    "mentioned_users": [2, 3],
    "likes": 0,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T10:00:00"
  }
}
```

### 4. 更新回复
**PUT** `/replies/{id}`

#### 请求体
```json
{
  "content": "这是更新后的评论内容"
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| content | string | 否 | 回复内容 |

#### 响应示例
```json
{
  "code": 200,
  "message": "回复更新成功",
  "data": {
    "objectId": 1,
    "content": "这是更新后的评论内容",
    "post_id": 1,
    "user": 1,
    "user_info": {
      "id": 1,
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "parent_id": null,
    "mentioned_users": [2, 3],
    "likes": 5,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T11:00:00"
  }
}
```

### 5. 删除回复
**DELETE** `/replies/{id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 回复ID |

#### 请求示例
```bash
DELETE /replies/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "回复删除成功",
  "data": null
}
```

### 6. 获取帖子回复
**GET** `/replies/post/{post_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| post_id | int | 是 | 帖子ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |
| include_children | bool | 否 | 是否包含子回复，默认true |

#### 请求示例
```bash
GET /replies/post/1?page=1&per_page=20&include_children=true
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取帖子回复成功",
  "data": {
    "list": [
      {
        "objectId": 1,
        "content": "这是一条评论",
        "post_id": 1,
        "user": 1,
        "user_info": {
          "id": 1,
          "username": "test_user",
          "avatar": "https://example.com/avatar.jpg"
        },
        "parent_id": null,
        "children": [
          {
            "objectId": 2,
            "content": "这是对评论的回复",
            "user": 2,
            "user_info": {
              "id": 2,
              "username": "user2",
              "avatar": "https://example.com/avatar2.jpg"
            },
            "parent_id": 1,
            "createdAt": "2025-01-09T10:05:00"
          }
        ],
        "likes": 5,
        "createdAt": "2025-01-09T10:00:00"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 1,
      "pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
}
```

### 7. 获取用户回复
**GET** `/replies/user/{user_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |

#### 请求示例
```bash
GET /replies/user/1?page=1&per_page=20
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取用户回复成功",
  "data": {
    "list": [
      {
        "objectId": 1,
        "content": "这是一条评论",
        "post_id": 1,
        "user": 1,
        "parent_id": null,
        "likes": 5,
        "createdAt": "2025-01-09T10:00:00"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 1,
      "pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
}
```

### 8. 获取回复的子回复
**GET** `/replies/{id}/children`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 父回复ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |

#### 请求示例
```bash
GET /replies/1/children?page=1&per_page=20
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取子回复成功",
  "data": {
    "list": [
      {
        "objectId": 2,
        "content": "这是对评论的回复",
        "post_id": 1,
        "user": 2,
        "user_info": {
          "id": 2,
          "username": "user2",
          "avatar": "https://example.com/avatar2.jpg"
        },
        "parent_id": 1,
        "likes": 2,
        "createdAt": "2025-01-09T10:05:00"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 1,
      "pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
}
```

### 9. 回复点赞
**POST** `/replies/{id}/like`

#### 请求体
```json
{
  "user_id": 3
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 点赞用户ID |

#### 响应示例
```json
{
  "code": 201,
  "message": "回复点赞成功",
  "data": {
    "reply_id": 1,
    "user_id": 3,
    "liked_at": "2025-01-09T10:00:00"
  }
}
```

### 10. 获取回复统计
**GET** `/replies/stats`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| post_id | int | 否 | 帖子ID筛选 |
| user | int | 否 | 用户ID筛选 |

#### 请求示例
```bash
GET /replies/stats?post_id=1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取回复统计成功",
  "data": {
    "total_replies": 100,
    "total_likes": 500,
    "average_likes_per_reply": 5.0,
    "post_stats": {
      "total": 10,
      "likes": 50,
      "average_likes": 5.0
    }
  }
}
```

## 错误响应

### 常见错误码
- `REPLY_NOT_FOUND`: 回复不存在
- `POST_NOT_FOUND`: 帖子不存在
- `USER_NOT_FOUND`: 用户不存在
- `MISSING_REQUIRED_FIELD`: 缺少必填字段
- `INVALID_PARENT_REPLY`: 无效的父回复
- `REPLY_CREATE_FAILED`: 回复创建失败
- `REPLY_UPDATE_FAILED`: 回复更新失败
- `REPLY_DELETE_FAILED`: 回复删除失败

### 错误响应示例
```json
{
  "code": 400,
  "message": "缺少必填字段"
}
```

## 数据模型

### Replies 表结构
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键ID |
| content | string | 回复内容 |
| post_id | int | 帖子ID |
| user | int | 回复用户ID |
| parent_id | int | 父回复ID（null表示顶级回复） |
| mentioned_users | json | @的用户ID数组 |
| likes | int | 点赞数 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

### 关系说明
- 支持两级评论：顶级回复和子回复
- 顶级回复的 `parent_id` 为 `null`
- 子回复的 `parent_id` 指向父回复的ID
- 支持@用户功能，`mentioned_users` 存储被@的用户ID数组
