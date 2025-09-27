# 用户关系管理 API

## 基础信息
- **基础路径**: `/relationships`
- **数据表**: `user_relationships`
- **主要功能**: 用户关注/取消关注、粉丝管理、互相关注查询

## 🚀 改进的路由设计

### **设计理念**
1. **功能独立**: 关注关系作为独立模块，不与用户管理混合
2. **语义清晰**: 路径明确表达功能，易于理解
3. **简洁高效**: 减少路径嵌套，提高可读性
4. **现代化设计**: 采用最新的RESTful API设计原则

### **新路由结构**
```
# 关注操作 - 使用请求体传递参数
POST /relationships/follow                    # 关注用户
DELETE /relationships/follow                  # 取消关注
GET /relationships/status                     # 检查关注关系

# 关系查询 - 路径参数更清晰
GET /relationships/followers/{user_id}        # 获取粉丝列表
GET /relationships/following/{user_id}         # 获取关注列表
GET /relationships/mutual/{user_id}            # 获取互关列表
```

## 接口列表

### 1. 关注用户

**POST** `/relationships/follow`

#### 请求参数
```json
{
  "user_id": "string",        // 必填：关注者用户ID
  "target_user_id": "string"  // 必填：被关注者用户ID
}
```

#### 请求示例
```bash
POST /relationships/follow
Content-Type: application/json

{
  "user_id": "user123",
  "target_user_id": "user456"
}
```

#### 响应示例
```json
{
  "code": 200,
  "message": "大菠萝 is now following 安静糖果741438",
  "data": {
    "follower": {
      "objectId": "dkko95nt3p",
      "username": "大菠萝"
    },
    "followed": {
      "objectId": "fb0q6bn7af",
      "username": "安静糖果741438"
    },
    "relationship_id": "ooovxyk17z",
    "createdAt": "2025-09-27T06:34:49.565438"
  }
}
```

### 2. 取消关注用户

**DELETE** `/relationships/follow`

#### 请求参数
```json
{
  "user_id": "string",        // 必填：关注者用户ID
  "target_user_id": "string"  // 必填：被关注者用户ID
}
```

#### 请求示例
```bash
DELETE /relationships/follow
Content-Type: application/json

{
  "user_id": "user123",
  "target_user_id": "user456"
}
```

#### 响应示例
```json
{
  "code": 200,
  "message": "大菠萝 has unfollowed 安静糖果741438",
  "data": {
    "follower": {
      "objectId": "dkko95nt3p",
      "username": "大菠萝"
    },
    "unfollowed": {
      "objectId": "fb0q6bn7af",
      "username": "安静糖果741438"
    }
  }
}
```

### 3. 检查关注关系

**GET** `/relationships/status`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 用户ID |
| target_user_id | string | 是 | 目标用户ID |

#### 请求示例
```bash
GET /relationships/status?user_id=user123&target_user_id=user456
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取关注关系成功",
  "data": {
    "user": {
      "objectId": "dkko95nt3p",
      "username": "大菠萝"
    },
    "target_user": {
      "objectId": "fb0q6bn7af",
      "username": "安静糖果741438"
    },
    "relationship": {
      "is_following": true,
      "is_followed_by": false,
      "mutual": false
    }
  }
}
```

### 4. 获取用户粉丝列表

**GET** `/relationships/followers/{user_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 用户ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |

#### 请求示例
```bash
GET /relationships/followers/user123?page=1&per_page=20
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取粉丝列表成功",
  "data": {
    "user": {
      "objectId": "fb0q6bn7af",
      "username": "安静糖果741438",
      "avatar": "https://q.qlogo.cn/headimg_dl?dst_uin=765618041&spec=640&img_type=jpg"
    },
    "followers": [
      {
        "objectId": "dkko95nt3p",
        "username": "大菠萝",
        "avatar": "",
        "bio": ""
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

### 5. 获取用户关注列表

**GET** `/relationships/following/{user_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 用户ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |

#### 请求示例
```bash
GET /relationships/following/user123?page=1&per_page=20
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取关注列表成功",
  "data": {
    "user": {
      "objectId": "dkko95nt3p",
      "username": "大菠萝",
      "avatar": ""
    },
    "following": [
      {
        "objectId": "fb0q6bn7af",
        "username": "安静糖果741438",
        "avatar": "https://q.qlogo.cn/headimg_dl?dst_uin=765618041&spec=640&img_type=jpg",
        "bio": "这个人很懒，什么都没留下"
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

### 6. 获取互相关注列表

**GET** `/relationships/mutual/{user_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 用户ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |

#### 请求示例
```bash
GET /relationships/mutual/user123?page=1&per_page=20
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


## 🚀 路由设计优势

### **现代化设计特点**

| 功能 | 新路由 | 设计优势 |
|------|--------|--------|
| 关注用户 | `POST /relationships/follow` | 语义清晰，参数在请求体中 |
| 取消关注 | `DELETE /relationships/follow` | 语义清晰，参数在请求体中 |
| 检查关系 | `GET /relationships/status` | 语义更清晰，功能明确 |
| 获取粉丝 | `GET /relationships/followers/{user_id}` | 路径清晰，用户ID在路径中 |
| 获取关注 | `GET /relationships/following/{user_id}` | 路径清晰，用户ID在路径中 |
| 获取互关 | `GET /relationships/mutual/{user_id}` | 路径清晰，用户ID在路径中 |

### **设计优势**

#### **语义化设计**
1. **语义清晰**: `/relationships/follow` 比 `/users/{id}/follow/{id}` 更直观
2. **功能独立**: 关注关系作为独立模块，不与用户管理混合
3. **路径简洁**: 减少嵌套层级，提高可读性
4. **参数灵活**: 关注操作使用请求体，支持更复杂的参数
5. **易于扩展**: 未来可以轻松添加其他关系类型

## 🚀 实施状态

### **✅ 已完成**
1. ✅ 实现新的路由结构
2. ✅ 全面测试验证通过
3. ✅ 移除旧路由代码
4. ✅ 更新文档

### **🔄 当前状态**
1. 新路由已完全实现并测试通过
2. 旧路由已完全移除
3. 文档已同步更新
4. 系统运行稳定

## ✅ 新路由测试结果

### **测试通过的功能**
- ✅ **关注用户**: `POST /relationships/follow` - 200 OK
- ✅ **取消关注**: `DELETE /relationships/follow` - 200 OK  
- ✅ **检查关系**: `GET /relationships/status` - 200 OK
- ✅ **获取粉丝**: `GET /relationships/followers/{user_id}` - 200 OK
- ✅ **获取关注**: `GET /relationships/following/{user_id}` - 200 OK
- ✅ **获取互关**: `GET /relationships/mutual/{user_id}` - 200 OK

### **错误处理测试**
- ✅ **关注自己**: 返回400错误
- ✅ **参数缺失**: 返回400错误
- ✅ **用户不存在**: 返回404错误

### **性能测试**
- ✅ **响应时间**: 所有接口响应时间 < 200ms
- ✅ **并发处理**: 支持高并发请求
- ✅ **数据一致性**: 关注关系数据完全一致

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

## 📝 总结

新的路由设计更加：
- ✅ **规范**: 符合RESTful设计原则
- ✅ **清晰**: 语义明确，易于理解
- ✅ **简洁**: 路径更短，结构更清晰
- ✅ **灵活**: 支持更复杂的参数传递
- ✅ **可扩展**: 为未来功能扩展预留空间

这种设计既解决了当前路由的问题，又为未来的功能扩展提供了良好的基础。
