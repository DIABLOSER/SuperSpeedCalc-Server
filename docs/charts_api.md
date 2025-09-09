# 排行榜 API

## 基础信息
- **基础路径**: `/charts`
- **数据表**: `charts`
- **主要功能**: 用户成绩记录、排行榜统计、成就管理

## 接口列表

### 1. 获取排行榜列表
**GET** `/charts`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20，最大100 |
| user | int | 否 | 用户ID筛选 |
| sort_by | string | 否 | 排序字段：objectId, title, achievement, user, createdAt, updatedAt |
| order | string | 否 | 排序方式：asc/desc，默认desc |

#### 请求示例
```bash
GET /charts?page=1&per_page=20&sort_by=achievement&order=desc
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取排行榜成功",
  "data": {
    "list": [
      {
        "objectId": 1,
        "title": "数学挑战",
        "achievement": 95,
        "user": 1,
        "user_info": {
          "id": 1,
          "username": "test_user",
          "avatar": "https://example.com/avatar.jpg"
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

### 2. 获取单个排行榜记录
**GET** `/charts/{id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 排行榜记录ID |

#### 请求示例
```bash
GET /charts/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取排行榜记录成功",
  "data": {
    "objectId": 1,
    "title": "数学挑战",
    "achievement": 95,
    "user": 1,
    "user_info": {
      "id": 1,
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T10:00:00"
  }
}
```

### 3. 创建排行榜记录
**POST** `/charts`

#### 请求体
```json
{
  "title": "数学挑战",
  "achievement": 95,
  "user": 1
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 挑战标题 |
| achievement | int | 否 | 成就分数，默认0 |
| user | int | 是 | 用户ID |

#### 响应示例
```json
{
  "code": 201,
  "message": "排行榜记录创建成功",
  "data": {
    "objectId": 1,
    "title": "数学挑战",
    "achievement": 95,
    "user": 1,
    "user_info": {
      "id": 1,
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T10:00:00"
  }
}
```

### 4. 更新排行榜记录
**PUT** `/charts/{id}`

#### 请求体
```json
{
  "title": "数学挑战升级版",
  "achievement": 98
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 否 | 挑战标题 |
| achievement | int | 否 | 成就分数 |

#### 响应示例
```json
{
  "code": 200,
  "message": "排行榜记录更新成功",
  "data": {
    "objectId": 1,
    "title": "数学挑战升级版",
    "achievement": 98,
    "user": 1,
    "user_info": {
      "id": 1,
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T11:00:00"
  }
}
```

### 5. 删除排行榜记录
**DELETE** `/charts/{id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 排行榜记录ID |

#### 请求示例
```bash
DELETE /charts/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "排行榜记录删除成功",
  "data": null
}
```

### 6. 获取用户排行榜记录
**GET** `/charts/user/{user_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |

#### 请求示例
```bash
GET /charts/user/1?page=1&per_page=10
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取用户排行榜记录成功",
  "data": {
    "list": [
      {
        "objectId": 1,
        "title": "数学挑战",
        "achievement": 95,
        "user": 1,
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

### 7. 获取排行榜统计
**GET** `/charts/stats`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user | int | 否 | 用户ID筛选 |

#### 请求示例
```bash
GET /charts/stats?user=1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取排行榜统计成功",
  "data": {
    "total_records": 100,
    "average_achievement": 85.5,
    "max_achievement": 100,
    "min_achievement": 0,
    "user_stats": {
      "total": 5,
      "average": 90.0,
      "max": 98,
      "min": 85
    }
  }
}
```

### 8. 更新成就分数
**PUT** `/charts/{id}/achievement`

#### 请求体
```json
{
  "achievement": 100
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| achievement | int | 是 | 新的成就分数 |

#### 响应示例
```json
{
  "code": 200,
  "message": "成就更新成功",
  "data": {
    "objectId": 1,
    "title": "数学挑战",
    "achievement": 100,
    "user": 1,
    "user_info": {
      "id": 1,
      "username": "test_user",
      "avatar": "https://example.com/avatar.jpg"
    },
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T12:00:00"
  }
}
```

## 错误响应

### 常见错误码
- `CHART_NOT_FOUND`: 排行榜记录不存在
- `USER_NOT_FOUND`: 用户不存在
- `MISSING_REQUIRED_FIELD`: 缺少必填字段
- `INVALID_ACHIEVEMENT`: 无效的成就分数
- `CHART_CREATE_FAILED`: 排行榜记录创建失败
- `CHART_UPDATE_FAILED`: 排行榜记录更新失败
- `CHART_DELETE_FAILED`: 排行榜记录删除失败

### 错误响应示例
```json
{
  "code": 400,
  "message": "用户不存在"
}
```
