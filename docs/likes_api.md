# Likes API 文档

## 📋 概述

Likes API 提供了完整的点赞功能，包括点赞、取消点赞、查询点赞状态等功能。该模块已从 posts 模块中独立出来，提供更好的模块化架构。

## 🚀 基础信息

- **基础路径**: `/likes`
- **内容类型**: `application/json`
- **认证**: 无需认证（可根据需要添加）

### 通用响应格式
```json
{
  "code": 200,
  "message": "操作成功",
  "data": { ... }
}
```

#### 响应字段说明
| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | HTTP状态码，200表示成功，400表示客户端错误，500表示服务器错误 |
| message | string | 操作结果消息，成功或失败的具体描述 |
| data | object | 响应数据，成功时包含具体数据，失败时可能为空 |

## 📚 API 接口

### 1. 点赞帖子

**POST** `/likes/`

创建新的点赞记录。

#### 请求参数

```json
{
    "post_id": "string",  // 必填：帖子ID
    "user_id": "string"   // 必填：用户ID
}
```

#### 响应示例

```json
{
    "success": true,
    "message": "点赞成功",
    "data": {
        "post_id": "post_123",
        "likeCount": 15,
        "user_id": "user_456",
        "like_id": "like_789",
        "is_liked_by_user": true
    }
}
```

#### 错误响应

```json
{
    "code": 400,
    "message": "用户已经点赞过此帖子"
}
```

### 2. 取消点赞帖子

**DELETE** `/likes/`

删除点赞记录。

#### 请求参数

```json
{
    "post_id": "string",  // 必填：帖子ID
    "user_id": "string"   // 必填：用户ID
}
```

#### 响应示例

```json
{
    "code": 200,
    "message": "取消点赞成功",
    "data": {
        "post_id": "post_123",
        "likeCount": 14,
        "user_id": "user_456",
        "is_liked_by_user": false
    }
}
```

### 3. 切换点赞状态

**POST** `/likes/toggle`

智能切换点赞状态（如果已点赞则取消，如果未点赞则点赞）。

#### 请求参数

```json
{
    "post_id": "string",  // 必填：帖子ID
    "user_id": "string"   // 必填：用户ID
}
```

#### 响应示例

```json
{
    "code": 200,
    "message": "点赞成功",
    "data": {
        "post_id": "post_123",
        "likeCount": 15,
        "user_id": "user_456",
        "is_liked_by_user": true,
        "action": "点赞"
    }
}
```

### 4. 获取帖子点赞用户列表

**GET** `/likes/post/{post_id}/likers`

获取指定帖子的所有点赞用户。

#### 路径参数

- `post_id`: 帖子ID

#### 查询参数

- `page`: 页码（默认：1）
- `per_page`: 每页数量（默认：20，最大：100）

#### 响应示例

```json
{
    "code": 200,
    "message": "获取帖子点赞列表成功",
    "data": {
        "post": {
            "objectId": "post_123",
            "content_preview": "这是一篇关于...",
            "likeCount": 15
        },
        "likers": [
            {
                "objectId": "like_789",
                "post": "post_123",
                "user": "user_456",
                "createdAt": "2024-01-15T10:30:00Z",
                "user_data": {
                    "objectId": "user_456",
                    "username": "张三",
                    "avatar": "avatar_url",
                    "bio": "用户简介"
                }
            }
        ],
        "pagination": {
            "page": 1,
            "per_page": 20,
            "total": 15,
            "pages": 1,
            "has_next": false,
            "has_prev": false
        }
    }
}
```

### 5. 获取用户点赞的帖子列表

**GET** `/likes/user/{user_id}/liked`

获取指定用户点赞的所有帖子。

#### 路径参数

- `user_id`: 用户ID

#### 查询参数

- `page`: 页码（默认：1）
- `per_page`: 每页数量（默认：20，最大：100）

#### 响应示例

```json
{
    "code": 200,
    "message": "获取用户点赞帖子列表成功",
    "data": {
        "user": {
            "objectId": "user_456",
            "username": "张三",
            "avatar": "avatar_url"
        },
        "liked_posts": [
            {
                "objectId": "like_789",
                "post": "post_123",
                "user": "user_456",
                "createdAt": "2024-01-15T10:30:00Z",
                "post_data": {
                    "objectId": "post_123",
                    "content": "完整的帖子内容...",
                    "visible": true,
                    "audit_state": "approved",
                    "likeCount": 15,
                    "replyCount": 3,
                    "images": ["image1.jpg", "image2.jpg"],
                    "createdAt": "2024-01-15T09:00:00Z",
                    "user": {
                        "objectId": "user_789",
                        "username": "李四",
                        "avatar": "avatar_url"
                    }
                }
            }
        ],
        "pagination": {
            "page": 1,
            "per_page": 20,
            "total": 5,
            "pages": 1,
            "has_next": false,
            "has_prev": false
        }
    }
}
```

### 6. 检查点赞状态

**GET** `/likes/status/{post_id}/{user_id}`

检查指定用户是否点赞了指定帖子。

#### 路径参数

- `post_id`: 帖子ID
- `user_id`: 用户ID

#### 响应示例

```json
{
    "code": 200,
    "message": "获取点赞状态成功",
    "data": {
        "post_id": "post_123",
        "user_id": "user_456",
        "is_liked": true,
        "like_count": 15
    }
}
```

### 7. 同步所有帖子点赞数（管理员功能）

**POST** `/likes/admin/sync-like-counts`

同步所有帖子的点赞数，确保数据一致性。

#### 请求参数

```json
{
    "admin_user_id": "string"  // 可选：管理员用户ID
}
```

#### 响应示例

```json
{
    "code": 200,
    "message": "同步完成，更新了 3 个帖子的点赞数",
    "data": {
        "total_posts": 100,
        "updated_posts": 3,
        "admin_user": "admin_123"
    }
}
```


## 🔄 架构变更说明

### 从 posts 模块迁移到独立模块

**之前的API路径**:
- `POST /posts/{post_id}/like` → `POST /likes/`
- `DELETE /posts/{post_id}/like` → `DELETE /likes/`
- `GET /posts/{post_id}/likers` → `GET /likes/post/{post_id}/likers`
- `GET /posts/user/{user_id}/liked` → `GET /likes/user/{user_id}/liked`

**新增功能**:
- `POST /likes/toggle` - 智能切换点赞状态
- `GET /likes/status/{post_id}/{user_id}` - 检查点赞状态

### 优势

1. **模块独立性**: likes 功能完全独立，不影响 posts 模块
2. **功能完整性**: 提供完整的 CRUD 操作
3. **易于维护**: 修改 likes 功能不会影响其他模块
4. **扩展性好**: 可以独立扩展 likes 功能
5. **代码组织**: 相关功能聚合在同一个模块中

## ⚠️ 注意事项

1. **数据一致性**: 点赞操作会自动同步更新帖子的 `likeCount` 字段
2. **唯一约束**: 同一用户不能重复点赞同一帖子
3. **分页限制**: 每页最多返回 100 条记录
4. **错误处理**: 所有接口都有完整的错误处理和响应
5. **事务安全**: 所有数据库操作都在事务中执行，确保数据一致性

## 🔗 相关文档

- [Posts API 文档](./posts_api.md)
- [Replies API 文档](./replies_api.md)
