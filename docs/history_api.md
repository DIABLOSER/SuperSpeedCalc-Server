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
| per_page | int | 否 | 每页数量，默认20 |
| user | int | 否 | 用户ID筛选 |
| sort_by | string | 否 | 排序字段：title, score, user, createdAt |
| order | string | 否 | 排序方式：asc/desc，默认desc |

#### 请求示例
```bash
GET /history?page=1&per_page=20&user=1&sort_by=score&order=desc
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取历史记录成功",
  "data": "{\"list\": [{\"objectId\": 1, \"title\": \"数学挑战\", \"score\": 95, \"user\": 1, \"user_info\": {\"id\": 1, \"username\": \"test_user\", \"avatar\": \"https://example.com/avatar.jpg\"}, \"createdAt\": \"2025-01-09T10:00:00\", \"updatedAt\": \"2025-01-09T10:00:00\"}], \"pagination\": {\"page\": 1, \"per_page\": 20, \"total\": 1, \"pages\": 1, \"has_next\": false, \"has_prev\": false}}"
}
```

### 2. 获取单个历史记录
**GET** `/history/{id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 历史记录ID |

#### 请求示例
```bash
GET /history/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取历史记录成功",
  "data": "{\"objectId\": 1, \"title\": \"数学挑战\", \"score\": 95, \"user\": 1, \"user_info\": {\"id\": 1, \"username\": \"test_user\", \"avatar\": \"https://example.com/avatar.jpg\"}, \"createdAt\": \"2025-01-09T10:00:00\", \"updatedAt\": \"2025-01-09T10:00:00\"}"
}
```

### 3. 创建历史记录
**POST** `/history`

#### 请求体
```json
{
  "title": "数学挑战",
  "score": 95,
  "user": 1
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 记录标题 |
| score | int | 否 | 分数，默认0 |
| user | int | 是 | 用户ID |

#### 响应示例
```json
{
  "code": 201,
  "message": "历史记录创建成功",
  "data": "{\"objectId\": 1, \"title\": \"数学挑战\", \"score\": 95, \"user\": 1, \"user_info\": {\"id\": 1, \"username\": \"test_user\", \"avatar\": \"https://example.com/avatar.jpg\"}, \"createdAt\": \"2025-01-09T10:00:00\", \"updatedAt\": \"2025-01-09T10:00:00\"}"
}
```

### 4. 更新历史记录
**PUT** `/history/{id}`

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
  "data": "{\"objectId\": 1, \"title\": \"数学挑战（更新）\", \"score\": 98, \"user\": 1, \"user_info\": {\"id\": 1, \"username\": \"test_user\", \"avatar\": \"https://example.com/avatar.jpg\"}, \"createdAt\": \"2025-01-09T10:00:00\", \"updatedAt\": \"2025-01-09T11:00:00\"}"
}
```

### 5. 删除历史记录
**DELETE** `/history/{id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 历史记录ID |

#### 请求示例
```bash
DELETE /history/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "历史记录删除成功",
  "data": null
}
```

### 6. 获取用户历史记录
**GET** `/history/user/{user_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户ID |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |

#### 请求示例
```bash
GET /history/user/1?page=1&per_page=10
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取用户历史记录成功",
  "data": "{\"list\": [{\"objectId\": 1, \"title\": \"数学挑战\", \"score\": 95, \"user\": 1, \"createdAt\": \"2025-01-09T10:00:00\"}], \"pagination\": {\"page\": 1, \"per_page\": 10, \"total\": 1, \"pages\": 1, \"has_next\": false, \"has_prev\": false}}"
}
```

### 7. 获取历史记录统计
**GET** `/history/stats`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user | int | 否 | 用户ID筛选 |

#### 请求示例
```bash
GET /history/stats?user=1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取历史记录统计成功",
  "data": "{\"total_records\": 100, \"average_score\": 85.5, \"max_score\": 100, \"min_score\": 0, \"user_stats\": {\"total\": 5, \"average\": 90.0, \"max\": 98, \"min\": 85}}"
}
```

### 8. 获取排行榜数据
**GET** `/history/leaderboard`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | string | 否 | 排行榜类型：daily, weekly, monthly, yearly, all |
| limit | int | 否 | 返回数量，默认10 |

#### 请求示例
```bash
GET /history/leaderboard?type=daily&limit=20
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取排行榜成功",
  "data": "{\"leaderboard\": [{\"rank\": 1, \"user\": {\"id\": 1, \"username\": \"test_user\", \"avatar\": \"https://example.com/avatar.jpg\"}, \"score\": 100, \"title\": \"数学挑战\"}, {\"rank\": 2, \"user\": {\"id\": 2, \"username\": \"user2\", \"avatar\": \"https://example.com/avatar2.jpg\"}, \"score\": 98, \"title\": \"数学挑战\"}], \"type\": \"daily\", \"total\": 2}"
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
  "message": "标题不能为空",
  "data": null,
  "error_code": "EMPTY_TITLE",
  "details": "标题字段不能为空"
}
```
