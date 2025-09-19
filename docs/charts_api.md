# 排行榜 API

## 基础信息
- **基础路径**: `/charts`
- **数据表**: `charts`
- **主要功能**: 用户成绩记录、排行榜统计、成就管理

## 接口列表

### 1. 获取图表列表
**GET** `/charts`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20，最大100 |
| user | string | 否 | 用户ID筛选（objectId） |
| sort_by | string | 否 | 排序字段：objectId, title, achievement, user, createdAt, updatedAt |
| order | string | 否 | 排序方式：asc/desc，默认desc |

#### 请求示例
```bash
GET /charts?page=1&per_page=20&user=user_object_id_here&sort_by=achievement&order=desc
```

#### 响应示例
```json
{
  "code": 200,
  "message": "图表数据获取成功",
  "data": {
    "items": [
      {
        "objectId": "chart_object_id_here",
        "title": "数学挑战",
        "achievement": 95.5,
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
      "per_page": 20,
      "total": 1,
      "pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
}
```

### 2. 获取单个图表
**GET** `/charts/{object_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| object_id | string | 是 | 图表ID（objectId） |

#### 请求示例
```bash
GET /charts/chart_object_id_here
```

#### 响应示例
```json
{
  "code": 200,
  "message": "图表详情获取成功",
  "data": {
    "objectId": "chart_object_id_here",
    "title": "数学挑战",
    "achievement": 95.5,
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

### 3. 创建图表
**POST** `/charts`

#### 请求体
```json
{
  "title": "数学挑战",
  "achievement": 95.5,
  "user": "user_object_id_here"
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 图表标题 |
| achievement | float | 否 | 成就分数，默认0.0 |
| user | string | 是 | 用户ID（objectId） |

#### 响应示例
```json
{
  "code": 201,
  "message": "操作成功",
  "data": {
    "objectId": "chart_object_id_here",
    "title": "数学挑战",
    "achievement": 95.5,
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

### 4. 更新图表
**PUT** `/charts/{object_id}`

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

### 5. 删除图表
**DELETE** `/charts/{object_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| object_id | string | 是 | 图表ID（objectId） |

#### 请求示例
```bash
DELETE /charts/chart_object_id_here
```

#### 响应示例
```json
{
  "code": 200,
  "message": "Chart deleted successfully"
}
```

### 6. 获取排行榜
**GET** `/charts/leaderboard`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 否 | 筛选特定标题的排行榜 |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认10，最大100 |

#### 请求示例
```bash
GET /charts/leaderboard?title=数学挑战&page=1&per_page=10
```

#### 响应示例
```json
{
  "code": 200,
  "message": "排行榜数据获取成功",
  "data": {
    "items": [
      {
        "objectId": "chart_object_id_here",
        "title": "数学挑战",
        "achievement": 95.5,
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

### 7. 根据成绩查询排名
**GET** `/charts/rank`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 图表标题 |
| achievement | float | 是 | 成绩值 |
| scope | string | 否 | 查询范围：global（全局）或title（同标题），默认global |

#### 请求示例
```bash
GET /charts/rank?title=数学挑战&achievement=95.5&scope=title
```

#### 响应示例
```json
{
  "code": 200,
  "message": "排名查询成功",
  "data": {
    "title": "数学挑战",
    "achievement": 95.5,
    "scope": "title",
    "rank": 3,
    "lower_count": 2,
    "ties_count": 1,
    "total": 10,
    "sample": {
      "objectId": "chart_object_id_here",
      "title": "数学挑战",
      "achievement": 95.5,
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
}
```

### 8. 查询用户排名
**GET** `/charts/user-rank`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user | string | 是 | 用户ID（objectId） |
| title | string | 是 | 图表标题 |

#### 请求示例
```bash
GET /charts/user-rank?user=user_object_id_here&title=数学挑战
```

#### 响应示例
```json
{
  "code": 200,
  "message": "用户排名查询成功",
  "data": {
    "user_info": {
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
    "achievement": 95.5,
    "rank": 3,
    "title": "数学挑战",
    "total_records": 10,
    "ties_count": 1,
    "record": {
      "objectId": "chart_object_id_here",
      "title": "数学挑战",
      "achievement": 95.5,
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
}
```

### 9. 更新成就分数
**POST** `/charts/{object_id}/achievement`

#### 请求体
```json
{
  "achievement": 100.5
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| achievement | float | 是 | 新的成就分数 |

#### 响应示例
```json
{
  "code": 200,
  "message": "Achievement updated successfully",
  "data": {
    "objectId": "chart_object_id_here",
    "title": "数学挑战",
    "achievement": 100.5,
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
