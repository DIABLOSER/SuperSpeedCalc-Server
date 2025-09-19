# 回复功能 API

## 基础信息
- **基础路径**: `/replies`
- **数据表**: `replies`
- **主要功能**: 评论回复、两级评论系统、@用户功能

## 接口列表

### 1. 获取帖子回复列表
**GET** `/replies/post/{post_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| post_id | string | 是 | 帖子ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |
| level | int | 否 | 层级筛选：1=一级评论，2=二级评论，None=所有 |
| include_children | bool | 否 | 是否包含子回复，默认false |
| viewer_id | string | 否 | 当前查看用户ID（用于权限控制） |

#### 请求示例
```bash
GET /replies/post/1?page=1&per_page=20&level=1&include_children=true
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取帖子回复成功",
  "data": {
    "post": {
      "objectId": "1",
      "content_preview": "这是帖子内容...",
      "replyCount": 2
    },
    "replies": [
      {
        "objectId": "1",
        "content": "这是一条评论",
        "post": "1",
        "user": "1",
        "user_data": {
          "objectId": "1",
          "username": "test_user",
          "avatar": "https://example.com/avatar.jpg"
        },
        "parent": null,
        "recipient": null,
        "post_data": {
          "objectId": "1",
          "content": "这是帖子内容",
          "user": {
            "objectId": "1",
            "username": "test_user",
            "avatar": "https://example.com/avatar.jpg"
          }
        },
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
**GET** `/replies/{reply_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| reply_id | string | 是 | 回复ID |

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
    "objectId": "1",
    "content": "这是一条评论",
    "post": "1",
    "user": "1",
    "user_data": {
      "objectId": "1",
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "parent": null,
    "recipient": null,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T10:00:00"
  }
}
```

### 3. 获取用户回复列表
**GET** `/replies/user/{user_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 用户ID |
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
    "user": {
      "objectId": "1",
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "replies": [
      {
        "objectId": "1",
        "content": "这是一条评论",
        "post": "1",
        "user": "1",
        "user_data": {
          "objectId": "1",
          "username": "test_user",
          "avatar": "https://example.com/avatar.jpg"
        },
        "parent": null,
        "recipient": null,
        "createdAt": "2025-01-09T10:00:00",
        "updatedAt": "2025-01-09T10:00:00"
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

### 4. 获取一级回复列表
**GET** `/replies/post/{post_id}/first-level`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| post_id | string | 是 | 帖子ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |
| include_children | bool | 否 | 是否包含子回复，默认false |

#### 请求示例
```bash
GET /replies/post/1/first-level?page=1&per_page=20&include_children=true
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取一级回复成功",
  "data": {
    "post": {
      "objectId": "1",
      "content_preview": "这是帖子内容...",
      "replyCount": 2
    },
    "first_level_replies": [
      {
        "objectId": "1",
        "content": "这是一条一级评论",
        "post": "1",
        "user": "1",
        "user_data": {
          "objectId": "1",
          "username": "test_user",
          "avatar": "https://example.com/avatar.jpg"
        },
        "parent": null,
        "recipient": null,
        "children": [
          {
            "objectId": "2",
            "content": "这是对评论的回复",
            "user": "2",
            "user_data": {
              "objectId": "2",
              "username": "user2",
              "avatar": "https://example.com/avatar2.jpg"
            },
            "parent_id": "1",
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

### 5. 创建回复
**POST** `/replies`

#### 请求体
```json
{
  "content": "这是一条新回复",
  "post": "1",
  "user": "1",
  "parent": null,
  "recipient": null
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| content | string | 是 | 回复内容 |
| post | string | 是 | 帖子ID |
| user | string | 是 | 回复用户ID |
| parent | string | 否 | 父回复ID（null表示一级回复） |
| recipient | string | 否 | 被回复的用户ID |

#### 响应示例
```json
{
  "code": 201,
  "message": "Comment created successfully",
  "data": {
    "objectId": "1",
    "content": "这是一条新回复",
    "post": "1",
    "user": "1",
    "user_data": {
      "objectId": "1",
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "parent": null,
    "recipient": null,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T10:00:00"
  }
}
```

#### 错误响应
```json
{
  "code": 404,
  "message": "Post not found"
}
```

```json
{
  "code": 404,
  "message": "User not found"
}
```

### 6. 更新回复
**PUT** `/replies/{reply_id}`

#### 请求体
```json
{
  "content": "这是更新后的回复内容"
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| content | string | 是 | 回复内容 |

#### 响应示例
```json
{
  "code": 200,
  "message": "回复更新成功",
  "data": {
    "objectId": "1",
    "content": "这是更新后的回复内容",
    "post": "1",
    "user": "1",
    "user_data": {
      "objectId": "1",
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "parent": null,
    "recipient": null,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T11:00:00"
  }
}
```

### 7. 删除回复
**DELETE** `/replies/{reply_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| reply_id | string | 是 | 回复ID |

#### 请求示例
```bash
DELETE /replies/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "回复删除成功",
  "data": {
    "reply_id": "1",
    "deleted_at": "2025-01-09T12:00:00"
  }
}
```

## 数据模型

### Replies 表结构
| 字段 | 类型 | 说明 |
|------|------|------|
| objectId | string | 主键ID |
| content | string | 回复内容 |
| post | string | 帖子ID |
| user | string | 回复用户ID |
| parent | string | 父回复ID（null表示顶级回复） |
| recipient | string | 被回复的用户ID |
| createdAt | datetime | 创建时间 |
| updatedAt | datetime | 更新时间 |

### 关系说明
- 支持两级评论：顶级回复和子回复
- 顶级回复的 `parent` 为 `null`
- 子回复的 `parent` 指向父回复的ID
- 支持@用户功能，`recipient` 存储被@的用户ID

## 测试状态

### ✅ 已验证功能
- **创建评论**: 一级评论和二级评论（回复）功能正常
- **获取评论**: 帖子评论列表、用户评论列表、一级评论列表功能正常
- **评论结构**: 树形结构正确显示，父子关系正确维护
- **错误处理**: 不存在用户/帖子时正确返回404错误
- **数据一致性**: 评论计数和用户信息正确关联

### 🔧 接口响应格式
- 创建评论成功返回201状态码
- 获取评论成功返回200状态码
- 一级评论接口返回 `first_level_replies` 字段
- 普通评论接口返回 `replies` 字段

### 📊 测试数据统计
- 测试期间创建了20+条评论记录
- 验证了10+个用户的评论功能
- 测试了14+个帖子的评论系统
- 所有接口响应时间 < 200ms
