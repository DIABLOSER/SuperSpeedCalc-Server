# 帖子管理 API

## 基础信息
- **基础路径**: `/posts`
- **数据表**: `posts`
- **主要功能**: 用户帖子发布、管理、审核、搜索、点赞

## 接口列表

### 1. 获取帖子列表
**GET** `/posts`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |
| user_id | string | 否 | 当前查看用户ID（用于权限控制） |
| keyword | string | 否 | 搜索关键词 |
| visible_only | bool | 否 | 只显示可见帖子，默认true |
| approved_only | bool | 否 | 只显示已审核帖子，默认true |
| sort_by | string | 否 | 排序字段：createdAt, updatedAt, likeCount, replyCount |
| order | string | 否 | 排序方式：asc/desc，默认desc |

#### 请求示例
```bash
GET /posts?page=1&per_page=20&visible_only=true&approved_only=true&user_id=1
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
          "actual_like_count": 10,
          "actual_reply_count": 5,
          "first_level_reply_count": 3,
          "second_level_reply_count": 2
        },
        "author_info": {
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
        "author_data": {
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
        "actual_like_count": 10,
        "actual_reply_count": 5,
        "first_level_reply_count": 3,
        "second_level_reply_count": 2,
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

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| post_id | string | 是 | 帖子ID |
| user_id | string | 否 | 当前查看用户ID（用于权限控制） |

#### 请求示例
```bash
GET /posts/abc123?user_id=user456
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
      "actual_like_count": 10,
      "actual_reply_count": 5,
      "first_level_reply_count": 3,
      "second_level_reply_count": 2
    },
    "author_info": {
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
    "author_data": {
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
    "actual_like_count": 10,
    "actual_reply_count": 5,
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
          "actual_like_count": 10,
          "actual_reply_count": 5,
          "first_level_reply_count": 3,
          "second_level_reply_count": 2
        },
        "actual_like_count": 10,
        "actual_reply_count": 5,
        "first_level_reply_count": 3,
        "second_level_reply_count": 2,
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
          "actual_like_count": 0,
          "actual_reply_count": 0,
          "first_level_reply_count": 0,
          "second_level_reply_count": 0
        },
        "author_info": {
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
        "author_data": {
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
        "actual_like_count": 0,
        "actual_reply_count": 0,
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

#### 请求体
```json
{
  "content": "这是帖子内容",
  "user": "user123",
  "visible": true,
  "audit_state": "pending",
  "images": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| content | string | 是 | 帖子内容 |
| user | string | 是 | 作者用户ID |
| visible | bool | 否 | 是否可见，默认true |
| audit_state | string | 否 | 审核状态：pending, approved, rejected，默认pending |
| images | array | 否 | 图片列表，默认空数组 |

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
      "actual_like_count": 0,
      "actual_reply_count": 0,
      "first_level_reply_count": 0,
      "second_level_reply_count": 0
    },
    "author_info": {
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
    "author_data": {
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
    "actual_like_count": 0,
    "actual_reply_count": 0,
    "first_level_reply_count": 0,
    "second_level_reply_count": 0,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T10:00:00"
  }
}
```

### 6. 更新帖子
**PUT** `/posts/{post_id}`

#### 请求体
```json
{
  "user_id": "user123",
  "content": "这是更新后的帖子内容",
  "visible": true,
  "images": ["https://example.com/new_image.jpg"]
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 当前用户ID（用于权限验证） |
| content | string | 否 | 帖子内容 |
| visible | bool | 否 | 是否可见 |
| images | array | 否 | 图片列表 |

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
      "actual_like_count": 5,
      "actual_reply_count": 2,
      "first_level_reply_count": 1,
      "second_level_reply_count": 1
    },
    "author_info": {
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
    "author_data": {
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
    "actual_like_count": 5,
    "actual_reply_count": 2,
    "first_level_reply_count": 1,
    "second_level_reply_count": 1,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T11:00:00"
  }
}
```

### 7. 删除帖子
**DELETE** `/posts/{post_id}`

#### 请求体
```json
{
  "user_id": "user123",
  "is_admin": false
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 当前用户ID |
| is_admin | bool | 否 | 是否为管理员操作，默认false |

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

### 8. 更新帖子审核状态
**PUT** `/posts/{post_id}/audit`

#### 请求体
```json
{
  "audit_state": "approved",
  "admin_user_id": "admin123",
  "reason": "内容符合规范"
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| audit_state | string | 是 | 审核状态：pending, approved, rejected |
| admin_user_id | string | 否 | 管理员用户ID |
| reason | string | 否 | 审核意见 |

#### 响应示例
```json
{
  "code": 200,
  "message": "Post audit state updated from pending to approved",
  "data": {
    "post_id": "abc123",
    "old_audit_state": "pending",
    "new_audit_state": "approved",
    "reason": "内容符合规范",
    "updated_by": "admin123",
    "updated_at": "2025-01-09T12:00:00"
  }
}
```

### 9. 点赞帖子
**POST** `/posts/{post_id}/like`

#### 请求体
```json
{
  "user_id": "user456"
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 点赞用户ID |

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

### 10. 取消点赞帖子
**POST** `/posts/{post_id}/unlike`

#### 请求体
```json
{
  "user_id": "user456"
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 取消点赞用户ID |

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

### 11. 获取帖子点赞用户列表
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

### 12. 获取用户点赞的帖子列表
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
          "is_liked_by_user": true,
          "is_visible": true,
          "is_approved": true,
          "stats": {
            "likeCount": 10,
            "replyCount": 5,
            "actual_like_count": 10,
            "actual_reply_count": 5,
            "first_level_reply_count": 3,
            "second_level_reply_count": 2
          },
          "author_info": {
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
          "author_data": {
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
          "actual_like_count": 10,
          "actual_reply_count": 5,
          "first_level_reply_count": 3,
          "second_level_reply_count": 2,
          "createdAt": "2025-01-09T10:00:00",
          "updatedAt": "2025-01-09T10:00:00"
        },
        "liked_at": "2025-01-09T10:30:00",
        "post": {
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
            "admin": false
          },
          "is_liked_by_user": true,
          "is_visible": true,
          "is_approved": true,
          "stats": {
            "likeCount": 10,
            "replyCount": 5,
            "actual_like_count": 10,
            "actual_reply_count": 5,
            "first_level_reply_count": 3,
            "second_level_reply_count": 2
          },
          "author_info": {
            "objectId": "user123",
            "username": "test_user",
            "avatar": "https://example.com/avatar.jpg",
            "bio": "用户简介",
            "experience": 100,
            "admin": false
          },
          "author_data": {
            "objectId": "user123",
            "username": "test_user",
            "avatar": "https://example.com/avatar.jpg",
            "bio": "用户简介",
            "experience": 100,
            "admin": false
          },
          "actual_like_count": 10,
          "actual_reply_count": 5,
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

### 13. 同步所有帖子点赞数
**POST** `/posts/admin/sync-like-counts`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| admin_user_id | string | 否 | 管理员用户ID（用于权限验证） |

#### 请求示例
```bash
POST /posts/admin/sync-like-counts?admin_user_id=admin123
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
   - 只有作者可以更新/删除自己的帖子
   - 管理员可以删除任何帖子
   - 不可见或未审核的帖子只有作者可以看到

2. **审核状态**：
   - `pending`: 待审核
   - `approved`: 已通过
   - `rejected`: 已拒绝

3. **向后兼容**：
   - 响应中包含 `author_info` 和 `author_data` 字段以保持向后兼容
   - 这些字段指向新的 `user` 字段

4. **点赞功能**：
   - 用户不能重复点赞同一帖子
   - 点赞数量会自动同步到 `likeCount` 字段
   - 提供同步工具修复数据不一致问题

5. **图片处理**：
   - 图片列表以JSON数组格式存储
   - 支持添加/删除图片
   - 提供图片列表的便捷操作方法