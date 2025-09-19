# 历史记录 API

## 基础信息
- **基础路径**: `/history`
- **数据表**: `history`
- **主要功能**: 用户操作历史记录、成绩统计、排行榜数据

## 接口列表

### 1. 获取历史记录列表
**GET** `/history`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认10 |
| user | string | 否 | 用户ID筛选（objectId） |

#### 请求示例
```bash
GET /history?page=1&per_page=10&user=user_object_id_here
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取历史记录列表成功",
  "data": {
    "items": [
      {
        "objectId": "history_object_id_here",
        "title": "数学挑战",
        "score": 95,
        "user": {
          "objectId": "user_object_id_here",
          "username": "快乐小熊123456",
          "avatar": "https://example.com/avatar.jpg",
          "bio": "这个人很懒，什么都没留下",
          "experience": 100,
          "boluo": 50,
          "isActive": true,
          "admin": false,
          "sex": 1,
          "birthday": "1990-01-01",
          "createdAt": "2025-01-09T10:00:00",
          "updatedAt": "2025-01-09T10:00:00"
        },
        "createdAt": "2025-01-09T10:00:00",
        "updatedAt": "2025-01-09T10:00:00"
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

### 2. 获取单个历史记录
**GET** `/history/{object_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| object_id | string | 是 | 历史记录ID（objectId） |

#### 请求示例
```bash
GET /history/history_object_id_here
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取历史记录成功",
  "data": {
    "objectId": "history_object_id_here",
    "title": "数学挑战",
    "score": 95,
    "user": {
      "objectId": "user_object_id_here",
      "username": "快乐小熊123456",
      "avatar": "https://example.com/avatar.jpg",
      "bio": "这个人很懒，什么都没留下",
      "experience": 100,
      "boluo": 50,
      "isActive": true,
      "admin": false,
      "sex": 1,
      "birthday": "1990-01-01",
      "createdAt": "2025-01-09T10:00:00",
      "updatedAt": "2025-01-09T10:00:00"
    },
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T10:00:00"
  }
}
```

### 3. 创建历史记录
**POST** `/history`

#### 请求体
```json
{
  "title": "数学挑战",
  "score": 95,
  "user": "user_object_id_here"
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 记录标题 |
| score | int | 是 | 分数（必填） |
| user | string | 是 | 用户ID（objectId） |

#### 响应示例
```json
{
  "code": 201,
  "message": "历史记录创建成功",
  "data": {
    "objectId": "history_object_id_here",
    "title": "数学挑战",
    "score": 95,
    "user": "user_object_id_here",
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T10:00:00"
  }
}
```

### 4. 更新历史记录
**PUT** `/history/{object_id}`

#### 请求体
```json
{
  "title": "数学挑战（更新）",
  "score": 98
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 否 | 记录标题 |
| score | int | 否 | 分数 |

#### 响应示例
```json
{
  "code": 200,
  "message": "历史记录更新成功",
  "data": {
    "objectId": 1,
    "title": "数学挑战（更新）",
    "score": 98,
    "user": {
      "objectId": "1",
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T11:00:00"
  }
}
```

### 5. 删除历史记录
**DELETE** `/history/{object_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| object_id | string | 是 | 历史记录ID（objectId） |

#### 请求示例
```bash
DELETE /history/history_object_id_here
```

#### 响应示例
```json
{
  "code": 200,
  "message": "历史记录删除成功"
}
```

### 6. 获取历史记录总数
**GET** `/history/count`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user | string | 否 | 用户ID筛选（objectId） |

#### 请求示例
```bash
GET /history/count?user=user_object_id_here
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取历史记录总数成功",
  "data": {
    "count": 100
  }
}
```

### 7. 获取用户score统计信息
**GET** `/history/stats`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user | string | 是 | 用户ID（objectId） |

#### 请求示例
```bash
GET /history/stats?user=user_object_id_here
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取用户score统计成功",
  "data": {
    "user": {
      "objectId": "user_object_id_here",
      "username": "快乐小熊123456",
      "avatar": "https://example.com/avatar.jpg",
      "bio": "这个人很懒，什么都没留下",
      "score": 0,
      "experience": 100,
      "boluo": 50,
      "isActive": true,
      "admin": false,
      "sex": 1,
      "birthday": "1990-01-01",
      "createdAt": "2025-01-09T10:00:00",
      "updatedAt": "2025-01-09T10:00:00"
    },
    "stats": {
      "today": {
        "total_score": 95,
        "count": 1,
        "rank": 1
      },
      "month": {
        "total_score": 285,
        "count": 3,
        "rank": 2
      },
      "year": {
        "total_score": 1200,
        "count": 12,
        "rank": 5
      },
      "total": {
        "total_score": 2500,
        "count": 25,
        "rank": 8
      }
    }
  }
}
```

### 8. 获取用户score得分排行榜
**GET** `/history/leaderboard`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认10 |
| period | string | 否 | 时间段：all, daily, monthly, yearly，默认all |

#### 请求示例
```bash
GET /history/leaderboard?page=1&per_page=10&period=daily
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取daily排行榜成功",
  "data": {
    "items": [
      {
        "rank": 1,
        "user": {
          "objectId": "user_object_id_here",
          "username": "快乐小熊123456",
          "avatar": "https://example.com/avatar.jpg",
          "bio": "这个人很懒，什么都没留下",
          "score": 0,
          "experience": 100,
          "boluo": 50,
          "isActive": true,
          "admin": false,
          "sex": 1,
          "birthday": "1990-01-01",
          "createdAt": "2025-01-09T10:00:00",
          "updatedAt": "2025-01-09T10:00:00"
        },
        "total_score": 100,
        "history_count": 1
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

## 错误响应

### 常见错误码
- `HISTORY_NOT_FOUND`: 历史记录不存在
- `USER_NOT_FOUND`: 用户不存在
- `MISSING_REQUIRED_FIELD`: 缺少必填字段
- `INVALID_SCORE`: 无效的分数
- `EMPTY_TITLE`: 标题不能为空
- `EMPTY_USER_ID`: 用户ID不能为空
- `HISTORY_CREATE_FAILED`: 历史记录创建失败
- `HISTORY_UPDATE_FAILED`: 历史记录更新失败
- `HISTORY_DELETE_FAILED`: 历史记录删除失败

### 错误响应示例
```json
{
  "code": 400,
  "message": "标题不能为空"
}
```
