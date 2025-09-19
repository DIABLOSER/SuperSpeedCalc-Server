# 帖子管理 API 文档

## 📋 基础信息
- **基础路径**: `/posts`
- **数据表**: `posts`
- **主要功能**: 用户帖子发布、管理、审核、搜索、点赞
- **接口总数**: 12个

## 🚀 快速开始

### 环境要求
- 开发环境: `http://localhost:8000`
- 生产环境: `http://localhost:8001`

### 通用响应格式
```json
{
  "code": 200,
  "message": "操作成功",
  "data": { ... }
}
```

## 📚 接口详细说明

### 1. 获取帖子列表
**GET** `/posts`

#### 📝 功能说明
获取帖子列表，支持分页、搜索、排序等功能。

#### 🔧 请求参数
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | int | 否 | 1 | 页码 |
| per_page | int | 否 | 20 | 每页数量 |
| user_id | string | 否 | - | 当前查看用户ID |
| keyword | string | 否 | - | 搜索关键词 |
| visible_only | bool | 否 | true | 只显示可见帖子 |
| approved_only | bool | 否 | true | 只显示已审核帖子 |
| sort_by | string | 否 | createdAt | 排序字段：createdAt, updatedAt, likeCount, replyCount |
| order | string | 否 | desc | 排序方式：asc/desc |

#### 💡 使用方法
```bash
# 基础用法
curl -X GET "http://localhost:8000/posts"

# 带分页
curl -X GET "http://localhost:8000/posts?page=1&per_page=10"

# 搜索帖子
curl -X GET "http://localhost:8000/posts?keyword=测试"

# 按点赞数排序
curl -X GET "http://localhost:8000/posts?sort_by=likeCount&order=desc"
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取帖子列表成功",
  "data": {
    "items": [
      {
        "objectId": "abc123",
        "user": "user123",
        "content": "这是帖子内容",
        "visible": true,
        "audit_state": "approved",
        "images": [],
        "likeCount": 10,
        "replyCount": 5,
        "user": {
          "objectId": "user123",
          "username": "test_user",
          "avatar": "https://example.com/avatar.jpg",
          "bio": "用户简介",
          "experience": 100,
          "boluo": 50,
          "isActive": true,
          "admin": false,
          "sex": 1,
          "birthday": "1990-01-01",
          "createdAt": "2025-01-01T00:00:00",
          "updatedAt": "2025-01-01T00:00:00"
        },
        "is_liked_by_user": false,
        "is_visible": true,
        "is_approved": true,
        "stats": {
          "likeCount": 10,
          "replyCount": 5,
          "first_level_reply_count": 3,
          "second_level_reply_count": 2
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

### 2. 获取单个帖子
**GET** `/posts/{post_id}`

#### 📝 功能说明
根据帖子ID获取单个帖子的详细信息。

#### 🔧 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| post_id | string | 是 | 帖子ID（路径参数） |
| user_id | string | 否 | 当前查看用户ID（查询参数） |

#### 💡 使用方法
```bash
# 基础用法
curl -X GET "http://localhost:8000/posts/abc123"

# 带用户ID（用于判断是否已点赞）
curl -X GET "http://localhost:8000/posts/abc123?user_id=user456"
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取帖子详情成功",
  "data": {
    "objectId": "abc123",
    "user": "user123",
    "content": "这是帖子内容",
    "visible": true,
    "audit_state": "approved",
    "images": [],
    "likeCount": 10,
    "replyCount": 5,
    "user": {
      "objectId": "user123",
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg",
      "bio": "用户简介",
      "experience": 100,
      "boluo": 50,
      "isActive": true,
      "admin": false,
      "sex": 1,
      "birthday": "1990-01-01",
      "createdAt": "2025-01-01T00:00:00",
      "updatedAt": "2025-01-01T00:00:00"
    },
    "is_liked_by_user": false,
    "is_visible": true,
    "is_approved": true,
    "stats": {
      "likeCount": 10,
      "replyCount": 5,
      "first_level_reply_count": 3,
      "second_level_reply_count": 2
    },
    "first_level_reply_count": 3,
    "second_level_reply_count": 2,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T10:00:00"
  }
}
```

### 3. 获取用户帖子列表
**GET** `/posts/user/{user_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 用户ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |
| viewer_id | string | 否 | 当前查看用户ID（用于权限控制） |

#### 请求示例
```bash
GET /posts/user/user123?page=1&per_page=20&viewer_id=user456
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取用户帖子列表成功",
  "data": {
    "user": {
      "objectId": "user123",
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "posts": [
      {
        "objectId": "abc123",
        "user": "user123",
        "content": "这是帖子内容",
        "visible": true,
        "audit_state": "approved",
        "images": [],
        "likeCount": 10,
        "replyCount": 5,
        "is_liked_by_user": false,
        "is_visible": true,
        "is_approved": true,
        "stats": {
          "likeCount": 10,
          "replyCount": 5,
          "first_level_reply_count": 3,
          "second_level_reply_count": 2
        },
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

### 4. 获取审核状态帖子列表
**GET** `/posts/audit/{audit_state}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| audit_state | string | 是 | 审核状态：pending, approved, rejected |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |

#### 请求示例
```bash
GET /posts/audit/pending?page=1&per_page=20
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取审核状态帖子列表成功",
  "data": {
    "audit_state": "pending",
    "audit_state_name": "待审核",
    "posts": [
      {
        "objectId": "abc123",
        "user": "user123",
        "content": "这是待审核的帖子内容",
        "visible": true,
        "audit_state": "pending",
        "images": [],
        "likeCount": 0,
        "replyCount": 0,
        "user": {
          "objectId": "user123",
          "username": "test_user",
          "avatar": "https://example.com/avatar.jpg",
          "bio": "用户简介",
          "experience": 100,
          "boluo": 50,
          "isActive": true,
          "admin": false,
          "sex": 1,
          "birthday": "1990-01-01",
          "createdAt": "2025-01-01T00:00:00",
          "updatedAt": "2025-01-01T00:00:00"
        },
        "is_liked_by_user": false,
        "is_visible": true,
        "is_approved": false,
        "stats": {
          "likeCount": 0,
          "replyCount": 0,
          "first_level_reply_count": 0,
          "second_level_reply_count": 0
        },
        "first_level_reply_count": 0,
        "second_level_reply_count": 0,
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

### 5. 创建帖子
**POST** `/posts`

#### 📝 功能说明
创建新的帖子，支持文本内容和图片。

#### 🔧 请求参数
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| content | string | 是 | - | 帖子内容 |
| user | string | 是 | - | 作者用户ID |
| visible | bool | 否 | true | 是否可见 |
| audit_state | string | 否 | pending | 审核状态：pending, approved, rejected |
| images | array | 否 | [] | 图片列表 |

#### 💡 使用方法
```bash
# 基础创建
curl -X POST "http://localhost:8000/posts" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "这是帖子内容",
    "user": "user123"
  }'

# 带图片创建
curl -X POST "http://localhost:8000/posts" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "这是带图片的帖子",
    "user": "user123",
    "images": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]
  }'
```

#### 响应示例
```json
{
  "code": 201,
  "message": "帖子创建成功",
  "data": {
    "objectId": "abc123",
    "user": "user123",
    "content": "这是帖子内容",
    "visible": true,
    "audit_state": "pending",
    "images": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
    "likeCount": 0,
    "replyCount": 0,
    "user": {
      "objectId": "user123",
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg",
      "bio": "用户简介",
      "experience": 100,
      "boluo": 50,
      "isActive": true,
      "admin": false,
      "sex": 1,
      "birthday": "1990-01-01",
      "createdAt": "2025-01-01T00:00:00",
      "updatedAt": "2025-01-01T00:00:00"
    },
    "is_liked_by_user": false,
    "is_visible": true,
    "is_approved": false,
    "stats": {
      "likeCount": 0,
      "replyCount": 0,
      "first_level_reply_count": 0,
      "second_level_reply_count": 0
    },
    "first_level_reply_count": 0,
    "second_level_reply_count": 0,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T10:00:00"
  }
}
```

### 6. 更新帖子（包括审核状态）
**PUT** `/posts/{post_id}`

#### 📝 功能说明
更新帖子内容或审核状态，支持同时更新多个字段。

#### 🔧 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| post_id | string | 是 | 帖子ID（路径参数） |
| user_id | string | 否 | 当前用户ID |
| content | string | 否 | 帖子内容 |
| visible | bool | 否 | 是否可见 |
| images | array | 否 | 图片列表 |
| audit_state | string | 否 | 审核状态：pending, approved, rejected |
| reason | string | 否 | 审核意见（当更新审核状态时） |

#### 💡 使用方法
```bash
# 更新帖子内容
curl -X PUT "http://localhost:8000/posts/abc123" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "这是更新后的帖子内容",
    "visible": true
  }'

# 更新审核状态
curl -X PUT "http://localhost:8000/posts/abc123" \
  -H "Content-Type: application/json" \
  -d '{
    "audit_state": "approved",
    "reason": "内容符合规范"
  }'

# 同时更新内容和审核状态
curl -X PUT "http://localhost:8000/posts/abc123" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "更新后的内容",
    "audit_state": "approved",
    "reason": "内容已修改并符合规范"
  }'
```

#### 响应示例
```json
{
  "code": 200,
  "message": "Post updated successfully",
  "data": {
    "objectId": "abc123",
    "user": "user123",
    "content": "这是更新后的帖子内容",
    "visible": true,
    "audit_state": "pending",
    "images": ["https://example.com/new_image.jpg"],
    "likeCount": 5,
    "replyCount": 2,
    "user": {
      "objectId": "user123",
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg",
      "bio": "用户简介",
      "experience": 100,
      "boluo": 50,
      "isActive": true,
      "admin": false,
      "sex": 1,
      "birthday": "1990-01-01",
      "createdAt": "2025-01-01T00:00:00",
      "updatedAt": "2025-01-01T00:00:00"
    },
    "is_liked_by_user": true,
    "is_visible": true,
    "is_approved": false,
    "stats": {
      "likeCount": 5,
      "replyCount": 2,
      "first_level_reply_count": 1,
      "second_level_reply_count": 1
    },
    "first_level_reply_count": 1,
    "second_level_reply_count": 1,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T11:00:00"
  }
}
```

### 7. 删除帖子
**DELETE** `/posts/{post_id}`

#### 📝 功能说明
删除指定的帖子，任何人都可以删除任何帖子（已移除权限限制）。

#### 🔧 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| post_id | string | 是 | 帖子ID（路径参数） |
| user_id | string | 否 | 当前用户ID（请求体） |
| is_admin | bool | 否 | 是否为管理员操作，默认false（请求体） |

#### 💡 使用方法
```bash
# 删除帖子
curl -X DELETE "http://localhost:8000/posts/abc123" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123"
  }'

# 管理员删除帖子
curl -X DELETE "http://localhost:8000/posts/abc123" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "admin123",
    "is_admin": true
  }'
```

#### 响应示例
```json
{
  "code": 201,
  "message": "Post deleted successfully",
  "data": {
    "post_id": "abc123",
    "author_id": "user123",
    "content_preview": "这是更新后的帖子内容",
    "delete_reason": "Deleted by author",
    "deleted_by": "user123"
  }
}
```

### 8. 点赞帖子
**POST** `/posts/{post_id}/like`

#### 📝 功能说明
为指定帖子点赞，用户不能重复点赞同一帖子。

#### 🔧 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| post_id | string | 是 | 帖子ID（路径参数） |
| user_id | string | 是 | 点赞用户ID（请求体） |

#### 💡 使用方法
```bash
# 点赞帖子
curl -X POST "http://localhost:8000/posts/abc123/like" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user456"
  }'
```

#### 响应示例
```json
{
  "code": 200,
  "message": "Post liked successfully",
  "data": {
    "post_id": "abc123",
    "likeCount": 11,
    "user_id": "user456",
    "like_id": "like789",
    "is_liked_by_user": true
  }
}
```

#### 错误响应
```json
{
  "code": 400,
  "message": "User has already liked this post"
}
```

```json
{
  "code": 404,
  "message": "User not found"
}
```

### 9. 取消点赞帖子
**DELETE** `/posts/{post_id}/like`

#### 📝 功能说明
取消对指定帖子的点赞。用户只能取消自己之前的点赞。

#### 🔧 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| post_id | string | 是 | 帖子ID（路径参数） |
| user_id | string | 是 | 取消点赞用户ID（请求体） |

#### 💡 使用方法
```bash
# 取消点赞帖子
curl -X DELETE "http://localhost:8000/posts/abc123/like" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user456"
  }'
```

#### 响应示例
```json
{
  "code": 200,
  "message": "Post unliked successfully",
  "data": {
    "post_id": "abc123",
    "likeCount": 10,
    "user_id": "user456",
    "is_liked_by_user": false
  }
}
```

#### 错误响应
```json
{
  "code": 400,
  "message": "User has not liked this post"
}
```

### 10. 获取帖子点赞用户列表
**GET** `/posts/{post_id}/likers`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| post_id | string | 是 | 帖子ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |
| viewer_id | string | 否 | 当前查看用户ID（用于权限控制） |

#### 请求示例
```bash
GET /posts/abc123/likers?page=1&per_page=20&viewer_id=user456
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取帖子点赞列表成功",
  "data": {
    "post": {
      "objectId": "abc123",
      "content_preview": "这是帖子内容",
      "likeCount": 10
    },
    "likers": [
      {
        "like_id": "like789",
        "user_data": {
          "objectId": "user456",
          "username": "liker_user",
          "avatar": "https://example.com/avatar2.jpg",
          "bio": "点赞用户简介",
          "experience": 50,
          "boluo": 25,
          "isActive": true,
          "admin": false,
          "sex": 0,
          "birthday": "1995-05-15",
          "createdAt": "2025-01-02T00:00:00",
          "updatedAt": "2025-01-02T00:00:00"
        },
        "liked_at": "2025-01-09T10:30:00",
        "user": {
          "objectId": "user456",
          "username": "liker_user",
          "avatar": "https://example.com/avatar2.jpg"
        }
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

### 11. 获取用户点赞的帖子列表
**GET** `/posts/user/{user_id}/liked`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 用户ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |
| viewer_id | string | 否 | 当前查看用户ID（用于权限控制） |

#### 请求示例
```bash
GET /posts/user/user456/liked?page=1&per_page=20&viewer_id=user789
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取用户点赞帖子列表成功",
  "data": {
    "user": {
      "objectId": "user456",
      "username": "liker_user",
      "avatar": "https://example.com/avatar2.jpg"
    },
    "liked_posts": [
      {
        "like_id": "like789",
        "post_data": {
          "objectId": "abc123",
          "content": "这是帖子内容",
          "visible": true,
          "audit_state": "approved",
          "images": [],
          "likeCount": 10,
          "replyCount": 5,
          "user": {
            "objectId": "user123",
            "username": "test_user",
            "avatar": "https://example.com/avatar.jpg",
            "bio": "用户简介",
            "experience": 100,
            "boluo": 50,
            "isActive": true,
            "admin": false,
            "sex": 1,
            "birthday": "1990-01-01",
            "createdAt": "2025-01-01T00:00:00",
            "updatedAt": "2025-01-01T00:00:00"
          },
          "is_liked_by_user": true,
          "is_visible": true,
          "is_approved": true,
          "stats": {
            "likeCount": 10,
            "replyCount": 5,
            "first_level_reply_count": 3,
            "second_level_reply_count": 2
          },
          "first_level_reply_count": 3,
          "second_level_reply_count": 2,
          "createdAt": "2025-01-09T10:00:00",
          "updatedAt": "2025-01-09T10:00:00"
        },
        "liked_at": "2025-01-09T10:30:00",
        "post": {
          "objectId": "abc123",
          "content": "这是帖子内容",
          "visible": true,
          "audit_state": "approved",
          "images": [],
          "likeCount": 10,
          "replyCount": 5,
          "user": {
            "objectId": "user123",
            "username": "test_user",
            "avatar": "https://example.com/avatar.jpg",
            "bio": "用户简介",
            "experience": 100,
            "admin": false
          },
          "is_liked_by_user": true,
          "is_visible": true,
          "is_approved": true,
          "stats": {
            "likeCount": 10,
            "replyCount": 5,
            "first_level_reply_count": 3,
            "second_level_reply_count": 2
          },
          "first_level_reply_count": 3,
          "second_level_reply_count": 2,
          "createdAt": "2025-01-09T10:00:00",
          "updatedAt": "2025-01-09T10:00:00"
        }
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

### 12. 同步所有帖子点赞数
**POST** `/posts/admin/sync-like-counts`

#### 📝 功能说明
同步所有帖子的点赞数，修复数据不一致问题。这是一个管理员工具。

#### 🔧 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| admin_user_id | string | 否 | 管理员用户ID（用于权限验证） |

#### 💡 使用方法
```bash
# 同步所有帖子点赞数
curl -X POST "http://localhost:8000/posts/admin/sync-like-counts" \
  -H "Content-Type: application/json" \
  -d '{
    "admin_user_id": "admin123"
  }'
```

#### 响应示例
```json
{
  "code": 200,
  "message": "Synchronized like counts for 5 posts",
  "data": {
    "total_posts": 100,
    "updated_posts": 5,
    "admin_user": "admin123"
  }
}
```

## 数据表结构

### Posts 表字段
| 字段名 | 类型 | 说明 |
|--------|------|------|
| objectId | string | 主键ID |
| user | string | 发帖用户ID（外键） |
| content | text | 帖子内容 |
| visible | bool | 是否公开可见 |
| audit_state | string | 审核状态：pending/approved/rejected |
| images | text | 图片列表（JSON格式） |
| likeCount | int | 点赞数量 |
| replyCount | int | 评论数量 |
| createdAt | datetime | 创建时间 |
| updatedAt | datetime | 更新时间 |

## 错误响应

### 常见错误码
- `POST_NOT_FOUND`: 帖子不存在
- `USER_NOT_FOUND`: 用户不存在
- `MISSING_REQUIRED_FIELD`: 缺少必填字段
- `INVALID_AUDIT_STATE`: 无效的审核状态
- `ACCESS_DENIED`: 访问被拒绝
- `POST_CREATE_FAILED`: 帖子创建失败
- `POST_UPDATE_FAILED`: 帖子更新失败
- `POST_DELETE_FAILED`: 帖子删除失败
- `PERMISSION_DENIED`: 权限不足

### 错误响应示例
```json
{
  "code": 400,
  "message": "User ID and content are required"
}
```

```json
{
  "code": 403,
  "message": "Permission denied. Only the author can update this post."
}
```

```json
{
  "code": 404,
  "message": "User not found"
}
```

## 注意事项

1. **权限控制**：
   - 任何人都可以查看、更新、删除所有帖子（已移除权限限制）
   - 任何人都可以点赞/取消点赞所有帖子
   - 任何人都可以查看所有帖子的点赞列表

2. **审核状态**：
   - `pending`: 待审核
   - `approved`: 已通过
   - `rejected`: 已拒绝
   - 审核状态更新已合并到帖子更新接口中

3. **路由合并**：
   - 帖子更新和审核状态更新使用同一个路由 `PUT /posts/{post_id}`
   - 取消点赞使用 `DELETE /posts/{post_id}/like` 而不是 `POST /posts/{post_id}/unlike`
   - 同步点赞数使用JSON请求体而不是URL参数

4. **字段统一**：
   - 每个信息只保留一个字段，避免重复
   - 用户信息统一使用 `user` 字段

5. **点赞功能**：
   - 用户不能重复点赞同一帖子
   - 点赞数量会自动同步到 `likeCount` 字段
   - 提供同步工具修复数据不一致问题

6. **图片处理**：
   - 图片列表以JSON数组格式存储
   - 支持添加/删除图片
   - 提供图片列表的便捷操作方法

## 🚀 快速参考

### 常用接口速查
| 功能 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 获取帖子列表 | GET | `/posts` | 支持分页、搜索、排序 |
| 获取单个帖子 | GET | `/posts/{post_id}` | 获取帖子详情 |
| 创建帖子 | POST | `/posts` | 创建新帖子 |
| 更新帖子 | PUT | `/posts/{post_id}` | 更新内容或审核状态 |
| 删除帖子 | DELETE | `/posts/{post_id}` | 删除帖子 |
| 点赞帖子 | POST | `/posts/{post_id}/like` | 点赞 |
| 取消点赞 | DELETE | `/posts/{post_id}/like` | 取消点赞 |
| 获取点赞列表 | GET | `/posts/{post_id}/likers` | 查看谁点赞了 |
| 获取用户帖子 | GET | `/posts/user/{user_id}` | 用户的所有帖子 |
| 获取用户点赞 | GET | `/posts/user/{user_id}/liked` | 用户点赞的帖子 |
| 按状态筛选 | GET | `/posts/audit/{audit_state}` | 按审核状态筛选 |
| 同步点赞数 | POST | `/posts/admin/sync-like-counts` | 管理员工具 |

### 状态码说明
| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

### 审核状态说明
| 状态 | 说明 |
|------|------|
| pending | 待审核 |
| approved | 已通过 |
| rejected | 已拒绝 |