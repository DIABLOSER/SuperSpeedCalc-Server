# 帖子管理 API

## 基础信息
- **基础路径**: `/posts`
- **数据表**: `posts`
- **主要功能**: 用户帖子发布、管理、审核、搜索

## 接口列表

### 1. 获取帖子列表
**GET** `/posts`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |
| user_id | string | 否 | 用户ID筛选 |
| keyword | string | 否 | 搜索关键词 |
| visible_only | bool | 否 | 只显示可见帖子，默认true |
| approved_only | bool | 否 | 只显示已审核帖子，默认true |
| sort_by | string | 否 | 排序字段：createdAt, updatedAt, likeCount, replyCount |
| order | string | 否 | 排序方式：asc/desc，默认desc |

#### 请求示例
```bash
GET /posts?page=1&per_page=20&visible_only=true&approved_only=true
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取帖子列表成功",
  "data": {
    "items": [
      {
        "objectId": 1,
        "content": "这是帖子内容",
        "user": "1",
        "user_info": {
          "objectId": "1",
          "username": "test_user",
          "avatar": "https://example.com/avatar.jpg"
        },
        "visible": true,
        "audit_state": "approved",
        "likeCount": 10,
        "replyCount": 5,
        "is_liked_by_user": false,
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
GET /posts/1?user_id=2
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取帖子成功",
  "data": {
    "objectId": 1,
    "title": "我的第一篇帖子",
    "content": "这是帖子内容",
    "user": 1,
    "user_info": {
      "id": 1,
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "category": "技术",
    "status": "published",
    "audit_state": "approved",
    "likes": 10,
    "views": 100,
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
GET /posts/user/1?page=1&per_page=20&viewer_id=2
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取用户帖子列表成功",
  "data": {
    "user": {
      "objectId": "1",
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "posts": [
      {
        "objectId": 1,
        "content": "这是帖子内容",
        "user": "1",
        "visible": true,
        "audit_state": "approved",
        "likeCount": 10,
        "replyCount": 5,
        "is_liked_by_user": false,
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
        "objectId": 1,
        "content": "这是待审核的帖子内容",
        "user": "1",
        "user_info": {
          "objectId": "1",
          "username": "test_user",
          "avatar": "https://example.com/avatar.jpg"
        },
        "visible": true,
        "audit_state": "pending",
        "likeCount": 0,
        "replyCount": 0,
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
  "user": "1",
  "visible": true,
  "audit_state": "pending",
  "images": []
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
    "objectId": 1,
    "title": "我的第一篇帖子",
    "content": "这是帖子内容",
    "user": 1,
    "user_info": {
      "id": 1,
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "category": "技术",
    "status": "published",
    "audit_state": "pending",
    "likes": 0,
    "views": 0,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T10:00:00"
  }
}
```

### 4. 更新帖子
**PUT** `/posts/{id}`

#### 请求体
```json
{
  "title": "我的第一篇帖子（更新）",
  "content": "这是更新后的帖子内容",
  "category": "技术分享",
  "status": "published"
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 否 | 帖子标题 |
| content | string | 否 | 帖子内容 |
| category | string | 否 | 分类 |
| status | string | 否 | 状态 |

#### 响应示例
```json
{
  "code": 200,
  "message": "帖子更新成功",
  "data": {
    "objectId": 1,
    "title": "我的第一篇帖子（更新）",
    "content": "这是更新后的帖子内容",
    "user": 1,
    "user_info": {
      "id": 1,
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "category": "技术分享",
    "status": "published",
    "audit_state": "pending",
    "likes": 10,
    "views": 100,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T11:00:00"
  }
}
```

### 5. 删除帖子
**DELETE** `/posts/{id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 帖子ID |

#### 请求示例
```bash
DELETE /posts/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "帖子删除成功",
  "data": null
}
```

### 6. 获取用户帖子
**GET** `/posts/user/{user_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |
| status | string | 否 | 状态筛选 |

#### 请求示例
```bash
GET /posts/user/1?page=1&per_page=10&status=published
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取用户帖子成功",
  "data": {
    "list": [
      {
        "objectId": 1,
        "title": "我的第一篇帖子",
        "content": "这是帖子内容",
        "user": 1,
        "category": "技术",
        "status": "published",
        "audit_state": "approved",
        "likes": 10,
        "views": 100,
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

### 7. 获取审核状态帖子
**GET** `/posts/audit/{audit_state}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| audit_state | string | 是 | 审核状态：pending/approved/rejected |
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
  "message": "获取审核帖子成功",
  "data": {
    "list": [
      {
        "objectId": 1,
        "title": "我的第一篇帖子",
        "content": "这是帖子内容",
        "user": 1,
        "user_info": {
          "id": 1,
          "username": "test_user",
          "avatar": "https://example.com/avatar.jpg"
        },
        "category": "技术",
        "status": "published",
        "audit_state": "pending",
        "likes": 0,
        "views": 0,
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

### 8. 审核帖子
**PUT** `/posts/{id}/audit`

#### 请求体
```json
{
  "audit_state": "approved",
  "audit_comment": "内容符合规范"
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| audit_state | string | 是 | 审核状态：approved/rejected |
| audit_comment | string | 否 | 审核意见 |

#### 响应示例
```json
{
  "code": 200,
  "message": "帖子审核成功",
  "data": {
    "objectId": 1,
    "title": "我的第一篇帖子",
    "content": "这是帖子内容",
    "user": 1,
    "user_info": {
      "id": 1,
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "category": "技术",
    "status": "published",
    "audit_state": "approved",
    "audit_comment": "内容符合规范",
    "likes": 10,
    "views": 100,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T12:00:00"
  }
}
```

### 9. 搜索帖子
**GET** `/posts/search`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| q | string | 是 | 搜索关键词 |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |
| category | string | 否 | 分类筛选 |

#### 请求示例
```bash
GET /posts/search?q=技术&page=1&per_page=10&category=技术
```

#### 响应示例
```json
{
  "code": 200,
  "message": "搜索帖子成功",
  "data": {
    "list": [
      {
        "objectId": 1,
        "title": "我的第一篇帖子",
        "content": "这是帖子内容",
        "user": 1,
        "user_info": {
          "id": 1,
          "username": "test_user",
          "avatar": "https://example.com/avatar.jpg"
        },
        "category": "技术",
        "status": "published",
        "audit_state": "approved",
        "likes": 10,
        "views": 100,
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
    },
    "query": "技术"
  }
}
```

### 10. 获取帖子统计
**GET** `/posts/stats`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user | int | 否 | 用户ID筛选 |

#### 请求示例
```bash
GET /posts/stats?user=1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取帖子统计成功",
  "data": {
    "total_posts": 100,
    "published_posts": 80,
    "draft_posts": 15,
    "archived_posts": 5,
    "pending_audit": 10,
    "approved_posts": 70,
    "rejected_posts": 5,
    "user_stats": {
      "total": 5,
      "published": 4,
      "draft": 1,
      "pending_audit": 1,
      "approved": 3,
      "rejected": 0
    }
  }
}
```

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

### 错误响应示例
```json
{
  "code": 400,
  "message": "缺少必填字段"
}
```
