# 论坛 API

## 基础信息
- **基础路径**: `/forum`
- **数据表**: `forum`
- **主要功能**: 论坛帖子发布、管理、分类、置顶

## 接口列表

### 1. 获取论坛帖子列表
**GET** `/forum`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |
| category | string | 否 | 分类筛选 |
| user | int | 否 | 用户ID筛选 |
| isPinned | bool | 否 | 是否置顶 |
| public | bool | 否 | 是否公开 |

#### 请求示例
```bash
GET /forum?page=1&per_page=20&category=技术讨论&isPinned=true
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取论坛帖子成功",
  "data": {
    "list": [
      {
        "objectId": 1,
        "title": "技术讨论",
        "content": "这是一个技术讨论帖子",
        "category": "技术讨论",
        "user": 1,
        "user_info": {
          "id": 1,
          "username": "test_user",
          "avatar": "https://example.com/avatar.jpg"
        },
        "isPinned": true,
        "public": true,
        "likes": 10,
        "replies": 5,
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

### 2. 获取单个论坛帖子
**GET** `/forum/{id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 帖子ID |

#### 请求示例
```bash
GET /forum/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取论坛帖子成功",
  "data": {
    "objectId": 1,
    "title": "技术讨论",
    "content": "这是一个技术讨论帖子",
    "category": "技术讨论",
    "user": 1,
    "user_info": {
      "id": 1,
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "isPinned": true,
    "public": true,
    "likes": 10,
    "replies": 5,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T10:00:00"
  }
}
```

### 3. 创建论坛帖子
**POST** `/forum`

#### 请求体
```json
{
  "title": "技术讨论",
  "content": "这是一个技术讨论帖子",
  "category": "技术讨论",
  "user": 1,
  "isPinned": false,
  "public": true
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 否 | 帖子标题 |
| content | string | 是 | 帖子内容 |
| category | string | 否 | 分类 |
| user | int | 是 | 作者用户ID |
| isPinned | bool | 否 | 是否置顶，默认false |
| public | bool | 否 | 是否公开，默认true |

#### 响应示例
```json
{
  "code": 201,
  "message": "论坛帖子创建成功",
  "data": {
    "objectId": 1,
    "title": "技术讨论",
    "content": "这是一个技术讨论帖子",
    "category": "技术讨论",
    "user": 1,
    "user_info": {
      "id": 1,
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "isPinned": false,
    "public": true,
    "likes": 0,
    "replies": 0,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T10:00:00"
  }
}
```

### 4. 更新论坛帖子
**PUT** `/forum/{id}`

#### 请求体
```json
{
  "title": "技术讨论（更新）",
  "content": "这是更新后的技术讨论帖子",
  "category": "技术讨论",
  "isPinned": true,
  "public": true
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 否 | 帖子标题 |
| content | string | 否 | 帖子内容 |
| category | string | 否 | 分类 |
| isPinned | bool | 否 | 是否置顶 |
| public | bool | 否 | 是否公开 |

#### 响应示例
```json
{
  "code": 200,
  "message": "论坛帖子更新成功",
  "data": {
    "objectId": 1,
    "title": "技术讨论（更新）",
    "content": "这是更新后的技术讨论帖子",
    "category": "技术讨论",
    "user": 1,
    "user_info": {
      "id": 1,
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "isPinned": true,
    "public": true,
    "likes": 10,
    "replies": 5,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T11:00:00"
  }
}
```

### 5. 删除论坛帖子
**DELETE** `/forum/{id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 帖子ID |

#### 请求示例
```bash
DELETE /forum/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "论坛帖子删除成功",
  "data": null
}
```

### 6. 获取用户论坛帖子
**GET** `/forum/user/{user_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |

#### 请求示例
```bash
GET /forum/user/1?page=1&per_page=10
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取用户论坛帖子成功",
  "data": {
    "list": [
      {
        "objectId": 1,
        "title": "技术讨论",
        "content": "这是一个技术讨论帖子",
        "category": "技术讨论",
        "user": 1,
        "isPinned": true,
        "public": true,
        "likes": 10,
        "replies": 5,
        "createdAt": "2025-01-09T10:00:00"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total": 1,
      "pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
}
```

### 7. 点赞论坛帖子
**POST** `/forum/{id}/like`

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

#### 响应示例
```json
{
  "code": 200,
  "message": "帖子点赞成功",
  "data": {
    "objectId": 1,
    "title": "技术讨论",
    "content": "这是一个技术讨论帖子",
    "category": "技术讨论",
    "user": 1,
    "user_info": {
      "id": 1,
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "isPinned": true,
    "public": true,
    "likes": 11,
    "replies": 5,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T12:00:00"
  }
}
```

### 8. 获取论坛统计
**GET** `/forum/stats`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user | int | 否 | 用户ID筛选 |

#### 请求示例
```bash
GET /forum/stats?user=1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取论坛统计成功",
  "data": {
    "total_posts": 100,
    "total_likes": 500,
    "total_replies": 200,
    "user_stats": {
      "posts": 5,
      "likes": 25,
      "replies": 10
    }
  }
}
```

## 错误响应

### 常见错误码
- `FORUM_POST_NOT_FOUND`: 论坛帖子不存在
- `AUTHOR_NOT_FOUND`: 作者不存在
- `MISSING_REQUIRED_FIELD`: 缺少必填字段
- `FORUM_POST_CREATE_FAILED`: 论坛帖子创建失败
- `FORUM_POST_UPDATE_FAILED`: 论坛帖子更新失败
- `FORUM_POST_DELETE_FAILED`: 论坛帖子删除失败
- `ALREADY_LIKED`: 已经点赞过

### 错误响应示例
```json
{
  "code": 400,
  "message": "作者不存在"
}
```
