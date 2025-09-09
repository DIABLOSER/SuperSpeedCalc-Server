# 用户管理 API

## 基础信息
- **基础路径**: `/users`
- **数据表**: `my_user`
- **主要功能**: 用户注册、登录、信息管理、密码重置

## 接口列表

### 1. 获取用户列表
**GET** `/users`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认10，最大100 |
| sort_by | string | 否 | 排序字段：username, mobile, createdAt |
| order | string | 否 | 排序方式：asc/desc，默认asc |
| keyword | string | 否 | 搜索关键词（用户名、手机号） |

#### 请求示例
```bash
GET /users?page=1&per_page=20&sort_by=createdAt&order=desc&keyword=test
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取用户列表成功",
  "data": {
    "list": [
      {
        "id": 1,
        "username": "test_user",
        "mobile": "13800138000",
        "avatar": "https://example.com/avatar.jpg",
        "bio": "用户简介",
        "experience": 100,
        "boluo": 50,
        "isActive": true,
        "admin": false,
        "sex": 1,
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

### 2. 获取单个用户
**GET** `/users/{id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 用户ID |

#### 请求示例
```bash
GET /users/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取用户信息成功",
  "data": {
    "id": 1,
    "username": "test_user",
    "mobile": "13800138000",
    "avatar": "https://example.com/avatar.jpg",
    "bio": "用户简介",
    "experience": 100,
    "boluo": 50,
    "isActive": true,
    "admin": false,
    "sex": 1,
    "createdAt": "2025-01-09T10:00:00"
  }
}
```

### 3. 创建用户
**POST** `/users`

#### 请求体
```json
{
  "username": "test_user",
  "password": "password123",
  "mobile": "13800138000",
  "avatar": "https://example.com/avatar.jpg",
  "bio": "用户简介",
  "sex": 1
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名，唯一 |
| password | string | 是 | 密码 |
| mobile | string | 是 | 手机号，唯一 |
| avatar | string | 否 | 头像URL |
| bio | string | 否 | 个人简介 |
| sex | int | 否 | 性别：1男/2女，默认1 |

#### 响应示例
```json
{
  "code": 201,
  "message": "用户创建成功",
  "data": {
    "id": 1,
    "username": "test_user",
    "mobile": "13800138000",
    "avatar": "https://example.com/avatar.jpg",
    "bio": "用户简介",
    "experience": 0,
    "boluo": 0,
    "isActive": true,
    "admin": false,
    "sex": 1,
    "createdAt": "2025-01-09T10:00:00"
  }
}
```

### 4. 更新用户信息
**PUT** `/users/{id}`

#### 请求体
```json
{
  "username": "new_username",
  "mobile": "13900139000",
  "avatar": "https://example.com/new_avatar.jpg",
  "bio": "新的个人简介",
  "sex": 2
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 否 | 用户名 |
| mobile | string | 否 | 手机号 |
| avatar | string | 否 | 头像URL |
| bio | string | 否 | 个人简介 |
| sex | int | 否 | 性别：1男/2女 |
| experience | int | 否 | 经验值 |
| boluo | int | 否 | 菠萝币 |
| isActive | bool | 否 | 是否激活 |
| admin | bool | 否 | 是否管理员 |

#### 响应示例
```json
{
  "code": 200,
  "message": "用户信息更新成功",
  "data": {
    "id": 1,
    "username": "new_username",
    "mobile": "13900139000",
    "avatar": "https://example.com/new_avatar.jpg",
    "bio": "新的个人简介",
    "experience": 100,
    "boluo": 50,
    "isActive": true,
    "admin": false,
    "sex": 2,
    "updatedAt": "2025-01-09T11:00:00"
  }
}
```

### 5. 删除用户
**DELETE** `/users/{id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 用户ID |

#### 请求示例
```bash
DELETE /users/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "用户删除成功",
  "data": null
}
```

### 6. 用户登录
**POST** `/users/login`

#### 请求体
```json
{
  "username": "test_user",
  "password": "password123"
}
```

#### 响应示例
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "user": {
      "id": 1,
      "username": "test_user",
      "mobile": "13800138000",
      "avatar": "https://example.com/avatar.jpg"
    },
    "token": "jwt_token_here"
  }
}
```

### 7. 用户注册
**POST** `/users/register`

#### 请求体
```json
{
  "username": "new_user",
  "password": "password123",
  "mobile": "13800138000"
}
```

#### 响应示例
```json
{
  "code": 201,
  "message": "注册成功",
  "data": {
    "id": 2,
    "username": "new_user",
    "mobile": "13800138000",
    "avatar": "https://example.com/avatar.jpg",
    "bio": "这个人很懒，什么都没留下",
    "experience": 0,
    "boluo": 0,
    "isActive": true,
    "admin": false,
    "sex": 1,
    "createdAt": "2025-01-09T12:00:00"
  }
}
```

### 8. 更新密码
**PUT** `/users/{id}/password`

#### 请求体
```json
{
  "old_password": "old_password123",
  "new_password": "new_password123"
}
```

#### 响应示例
```json
{
  "code": 200,
  "message": "密码更新成功",
  "data": null
}
```

### 9. 手机号密码重置
**POST** `/users/reset-password`

#### 请求体
```json
{
  "mobile": "13800138000",
  "sms_code": "123456",
  "new_password": "new_password123"
}
```

#### 响应示例
```json
{
  "code": 200,
  "message": "密码重置成功",
  "data": null
}
```

### 10. 获取用户数量
**GET** `/users/count`

#### 响应示例
```json
{
  "code": 200,
  "message": "获取用户数量成功",
  "data": {
    "count": 100
  }
}
```

## 错误响应

### 常见错误码
- `USER_NOT_FOUND`: 用户不存在
- `DUPLICATE_USERNAME`: 用户名已存在
- `DUPLICATE_EMAIL`: 邮箱已存在
- `DUPLICATE_MOBILE`: 手机号已存在
- `INVALID_PASSWORD`: 密码错误
- `INVALID_CREDENTIALS`: 登录凭据无效
- `USER_CREATE_FAILED`: 用户创建失败
- `USER_UPDATE_FAILED`: 用户更新失败
- `USER_DELETE_FAILED`: 用户删除失败

### 错误响应示例
```json
{
  "code": 400,
  "message": "用户名已存在"
}
```
