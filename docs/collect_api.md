# 收藏功能 API 文档

## 概述

收藏功能允许用户收藏和取消收藏帖子，提供完整的收藏管理功能。

## 数据模型

### Collect 收藏表

| 字段名 | 类型 | 说明 | 约束 |
|--------|------|------|------|
| objectId | String(20) | 主键ID | 主键，自动生成 |
| user | String(20) | 用户ID | 外键，关联my_user表 |
| post | String(20) | 帖子ID | 外键，关联posts表 |
| createdAt | DateTime | 创建时间 | 自动设置 |
| updatedAt | DateTime | 更新时间 | 自动更新 |

**唯一约束**: `(user, post)` - 防止用户重复收藏同一帖子

## API 接口

### 1. 收藏帖子

**POST** `/collect/create`

**请求体**:
```json
{
    "user_id": "用户ID",
    "post_id": "帖子ID"
}
```

**响应示例**:
```json
{
    "success": true,
    "message": "收藏成功",
    "data": {
        "post_id": "帖子ID",
        "user_id": "用户ID", 
        "collect_id": "收藏记录ID",
        "is_collected_by_user": true
    }
}
```

**错误响应**:
- 400: 缺少必要参数
- 404: 用户或帖子不存在
- 400: 用户已经收藏过此帖子

### 2. 获取用户收藏的帖子列表

**GET** `/collect/user/{user_id}/posts`

**查询参数**:
- `page`: 页码 (默认: 1)
- `per_page`: 每页数量 (默认: 20, 最大: 100)

**响应示例**:
```json
{
    "success": true,
    "message": "获取用户收藏帖子列表成功",
    "data": {
        "user": {
            "objectId": "用户ID",
            "username": "用户名",
            "avatar": "头像URL"
        },
        "collected_posts": [
            {
                "objectId": "收藏记录ID",
                "user": "用户ID",
                "post": {
                    "objectId": "帖子ID",
                    "content": "帖子内容",
                    "visible": true,
                    "audit_state": "approved",
                    "images": ["图片URL1", "图片URL2"],
                    "likeCount": 10,
                    "replyCount": 5,
                    "createdAt": "2024-01-01T00:00:00",
                    "updatedAt": "2024-01-01T00:00:00"
                },
                "createdAt": "2024-01-01T00:00:00",
                "updatedAt": "2024-01-01T00:00:00"
            }
        ],
        "pagination": {
            "page": 1,
            "per_page": 20,
            "total": 50,
            "pages": 3,
            "has_next": true,
            "has_prev": false
        }
    }
}
```

### 3. 获取收藏指定帖子的用户列表

**GET** `/collect/post/{post_id}/users`

**查询参数**:
- `page`: 页码 (默认: 1)
- `per_page`: 每页数量 (默认: 20, 最大: 100)

**响应示例**:
```json
{
    "success": true,
    "message": "获取帖子收藏用户列表成功",
    "data": {
        "post": {
            "objectId": "帖子ID",
            "content_preview": "帖子内容预览...",
            "collect_count": 25
        },
        "collectors": [
            {
                "objectId": "收藏记录ID",
                "user": {
                    "objectId": "用户ID",
                    "username": "用户名",
                    "avatar": "头像URL",
                    "bio": "个人简介",
                    "experience": 100,
                    "boluo": 50,
                    "isActive": true,
                    "admin": false,
                    "sex": 1,
                    "birthday": "1990-01-01",
                    "createdAt": "2024-01-01T00:00:00",
                    "updatedAt": "2024-01-01T00:00:00"
                },
                "post": "帖子ID",
                "createdAt": "2024-01-01T00:00:00",
                "updatedAt": "2024-01-01T00:00:00"
            }
        ],
        "pagination": {
            "page": 1,
            "per_page": 20,
            "total": 25,
            "pages": 2,
            "has_next": true,
            "has_prev": false
        }
    }
}
```

### 4. 检查收藏状态

**GET** `/collect/status/{user_id}/{post_id}`

**响应示例**:
```json
{
    "success": true,
    "message": "获取收藏状态成功",
    "data": {
        "post_id": "帖子ID",
        "user_id": "用户ID",
        "is_collected": true,
        "collect_count": 25
    }
}
```

### 5. 获取用户收藏统计

**GET** `/collect/user/{user_id}/stats`

**响应示例**:
```json
{
    "success": true,
    "message": "获取用户收藏统计成功",
    "data": {
        "user": {
            "objectId": "用户ID",
            "username": "用户名",
            "avatar": "头像URL"
        },
        "collect_count": 50
    }
}
```

### 6. 取消收藏

**POST** `/collect/delete`

**请求体**:
```json
{
    "user_id": "用户ID",
    "post_id": "帖子ID"
}
```

**响应示例**:
```json
{
    "success": true,
    "message": "取消收藏成功",
    "data": {
        "post_id": "帖子ID",
        "user_id": "用户ID",
        "is_collected_by_user": false
    }
}
```

### 7. 通过收藏ID删除

**DELETE** `/collect/{collect_id}`

**响应示例**:
```json
{
    "success": true,
    "message": "删除收藏记录成功",
    "data": {
        "collect_id": "收藏记录ID",
        "post_id": "帖子ID",
        "user_id": "用户ID",
        "is_collected_by_user": false
    }
}
```

### 8. 清空用户所有收藏

**DELETE** `/collect/user/{user_id}/clear`

**响应示例**:
```json
{
    "success": true,
    "message": "成功清空用户收藏，删除了 50 条记录",
    "data": {
        "user_id": "用户ID",
        "deleted_count": 50
    }
}
```

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 使用示例

### JavaScript 示例

```javascript
// 收藏帖子
async function collectPost(userId, postId) {
        const response = await fetch('/collect/create', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: userId,
            post_id: postId
        })
    });
    return await response.json();
}

// 获取用户收藏列表
async function getUserCollects(userId, page = 1, perPage = 20) {
        const response = await fetch(`/collect/user/${userId}/posts?page=${page}&per_page=${perPage}`);
    return await response.json();
}

// 取消收藏
async function uncollectPost(userId, postId) {
        const response = await fetch('/collect/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: userId,
            post_id: postId
        })
    });
    return await response.json();
}
```

## 注意事项

1. 用户不能重复收藏同一个帖子
2. 收藏记录包含创建时间，按时间倒序排列
3. 删除帖子时会自动删除相关的收藏记录（级联删除）
4. 删除用户时会自动删除该用户的所有收藏记录
5. 分页查询支持最大100条每页的限制
6. 所有时间字段使用ISO格式返回
