# 横幅管理 API

## 基础信息
- **基础路径**: `/banners`
- **数据表**: `banners`
- **主要功能**: 轮播图管理、广告投放、排序控制

## 接口列表

### 1. 获取横幅列表
**GET** `/banners`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |
| status | string | 否 | 状态筛选：active/inactive |
| action_type | string | 否 | 动作类型筛选 |

#### 请求示例
```bash
GET /banners?page=1&per_page=20&status=active
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取横幅列表成功",
  "data": "{\"list\": [{\"objectId\": 1, \"title\": \"欢迎横幅\", \"image_url\": \"https://example.com/banner1.jpg\", \"action_type\": \"url\", \"action_value\": \"https://example.com\", \"status\": \"active\", \"sort_order\": 1, \"start_date\": \"2025-01-09T00:00:00\", \"end_date\": \"2025-12-31T23:59:59\", \"createdAt\": \"2025-01-09T10:00:00\", \"updatedAt\": \"2025-01-09T10:00:00\"}], \"pagination\": {\"page\": 1, \"per_page\": 20, \"total\": 1, \"pages\": 1, \"has_next\": false, \"has_prev\": false}}"
}
```

### 2. 获取单个横幅
**GET** `/banners/{id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 横幅ID |

#### 请求示例
```bash
GET /banners/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取横幅成功",
  "data": "{\"objectId\": 1, \"title\": \"欢迎横幅\", \"image_url\": \"https://example.com/banner1.jpg\", \"action_type\": \"url\", \"action_value\": \"https://example.com\", \"status\": \"active\", \"sort_order\": 1, \"start_date\": \"2025-01-09T00:00:00\", \"end_date\": \"2025-12-31T23:59:59\", \"createdAt\": \"2025-01-09T10:00:00\", \"updatedAt\": \"2025-01-09T10:00:00\"}"
}
```

### 3. 创建横幅
**POST** `/banners`

#### 请求体
```json
{
  "title": "欢迎横幅",
  "image_url": "https://example.com/banner1.jpg",
  "action_type": "url",
  "action_value": "https://example.com",
  "status": "active",
  "sort_order": 1,
  "start_date": "2025-01-09T00:00:00",
  "end_date": "2025-12-31T23:59:59"
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 横幅标题 |
| image_url | string | 是 | 图片URL |
| action_type | string | 是 | 动作类型：url/app_page/product |
| action_value | string | 是 | 动作值（URL、页面ID或产品ID） |
| status | string | 否 | 状态：active/inactive，默认active |
| sort_order | int | 否 | 排序顺序，默认0 |
| start_date | datetime | 否 | 开始时间 |
| end_date | datetime | 否 | 结束时间 |

#### 响应示例
```json
{
  "code": 201,
  "message": "横幅创建成功",
  "data": "{\"objectId\": 1, \"title\": \"欢迎横幅\", \"image_url\": \"https://example.com/banner1.jpg\", \"action_type\": \"url\", \"action_value\": \"https://example.com\", \"status\": \"active\", \"sort_order\": 1, \"start_date\": \"2025-01-09T00:00:00\", \"end_date\": \"2025-12-31T23:59:59\", \"createdAt\": \"2025-01-09T10:00:00\", \"updatedAt\": \"2025-01-09T10:00:00\"}"
}
```

### 4. 更新横幅
**PUT** `/banners/{id}`

#### 请求体
```json
{
  "title": "欢迎横幅（更新）",
  "image_url": "https://example.com/banner1_updated.jpg",
  "action_type": "app_page",
  "action_value": "home",
  "status": "active",
  "sort_order": 2
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 否 | 横幅标题 |
| image_url | string | 否 | 图片URL |
| action_type | string | 否 | 动作类型 |
| action_value | string | 否 | 动作值 |
| status | string | 否 | 状态 |
| sort_order | int | 否 | 排序顺序 |
| start_date | datetime | 否 | 开始时间 |
| end_date | datetime | 否 | 结束时间 |

#### 响应示例
```json
{
  "code": 200,
  "message": "横幅更新成功",
  "data": "{\"objectId\": 1, \"title\": \"欢迎横幅（更新）\", \"image_url\": \"https://example.com/banner1_updated.jpg\", \"action_type\": \"app_page\", \"action_value\": \"home\", \"status\": \"active\", \"sort_order\": 2, \"start_date\": \"2025-01-09T00:00:00\", \"end_date\": \"2025-12-31T23:59:59\", \"createdAt\": \"2025-01-09T10:00:00\", \"updatedAt\": \"2025-01-09T11:00:00\"}"
}
```

### 5. 删除横幅
**DELETE** `/banners/{id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 横幅ID |

#### 请求示例
```bash
DELETE /banners/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "横幅删除成功",
  "data": null
}
```

### 6. 获取活跃横幅
**GET** `/banners/active`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| limit | int | 否 | 返回数量，默认10 |

#### 请求示例
```bash
GET /banners/active?limit=5
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取活跃横幅成功",
  "data": "{\"banners\": [{\"objectId\": 1, \"title\": \"欢迎横幅\", \"image_url\": \"https://example.com/banner1.jpg\", \"action_type\": \"url\", \"action_value\": \"https://example.com\", \"status\": \"active\", \"sort_order\": 1, \"start_date\": \"2025-01-09T00:00:00\", \"end_date\": \"2025-12-31T23:59:59\"}], \"total\": 1, \"action_types\": [\"url\", \"app_page\", \"product\"]}"
}
```

### 7. 更新横幅排序
**PUT** `/banners/{id}/sort`

#### 请求体
```json
{
  "sort_order": 3
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sort_order | int | 是 | 新的排序顺序 |

#### 响应示例
```json
{
  "code": 200,
  "message": "横幅排序更新成功",
  "data": "{\"objectId\": 1, \"title\": \"欢迎横幅\", \"image_url\": \"https://example.com/banner1.jpg\", \"action_type\": \"url\", \"action_value\": \"https://example.com\", \"status\": \"active\", \"sort_order\": 3, \"start_date\": \"2025-01-09T00:00:00\", \"end_date\": \"2025-12-31T23:59:59\", \"createdAt\": \"2025-01-09T10:00:00\", \"updatedAt\": \"2025-01-09T12:00:00\"}"
}
```

### 8. 批量更新横幅状态
**PUT** `/banners/batch-status`

#### 请求体
```json
{
  "banner_ids": [1, 2, 3],
  "status": "inactive"
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| banner_ids | array | 是 | 横幅ID数组 |
| status | string | 是 | 新状态：active/inactive |

#### 请求示例
```bash
curl -X PUT http://localhost:5000/banners/batch-status \
  -H "Content-Type: application/json" \
  -d '{"banner_ids": [1, 2, 3], "status": "inactive"}'
```

#### 响应示例
```json
{
  "code": 200,
  "message": "批量更新横幅状态成功",
  "data": "{\"success_count\": 3, \"failed_count\": 0, \"results\": [{\"banner_id\": 1, \"status\": \"success\"}, {\"banner_id\": 2, \"status\": \"success\"}, {\"banner_id\": 3, \"status\": \"success\"}]}"
}
```

### 9. 获取横幅统计
**GET** `/banners/stats`

#### 响应示例
```json
{
  "code": 200,
  "message": "获取横幅统计成功",
  "data": "{\"total_banners\": 10, \"active_banners\": 8, \"inactive_banners\": 2, \"action_types\": {\"url\": 5, \"app_page\": 3, \"product\": 2}, \"expired_banners\": 1, \"upcoming_banners\": 2}"
}
```

### 10. 上传横幅图片
**POST** `/banners/upload`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | file | 是 | 图片文件 |

#### 支持的文件格式
- PNG, JPG, JPEG, GIF, WEBP, BMP

#### 请求示例
```bash
curl -X POST -F "file=@banner.jpg" http://localhost:5000/banners/upload
```

#### 响应示例
```json
{
  "code": 201,
  "message": "横幅图片上传成功",
  "data": "{\"image_url\": \"http://localhost:5000/uploads/banners/20250109_100000_abc12345.jpg\", \"file_size\": 102400, \"uploaded_at\": \"2025-01-09T10:00:00\"}"
}
```

## 错误响应

### 常见错误码
- `BANNER_NOT_FOUND`: 横幅不存在
- `MISSING_REQUIRED_FIELD`: 缺少必填字段
- `INVALID_ACTION_TYPE`: 无效的动作类型
- `INVALID_STATUS`: 无效的状态
- `INVALID_DATE_RANGE`: 无效的日期范围
- `BANNER_CREATE_FAILED`: 横幅创建失败
- `BANNER_UPDATE_FAILED`: 横幅更新失败
- `BANNER_DELETE_FAILED`: 横幅删除失败

### 错误响应示例
```json
{
  "code": 400,
  "message": "无效的动作类型",
  "data": null,
  "error_code": "INVALID_ACTION_TYPE",
  "details": "支持的动作类型：url, app_page, product"
}
```

## 数据模型

### Banners 表结构
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键ID |
| title | string | 横幅标题 |
| image_url | string | 图片URL |
| action_type | string | 动作类型：url/app_page/product |
| action_value | string | 动作值 |
| status | string | 状态：active/inactive |
| sort_order | int | 排序顺序 |
| start_date | datetime | 开始时间 |
| end_date | datetime | 结束时间 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

### 动作类型说明
- `url`: 跳转到外部链接
- `app_page`: 跳转到应用内页面
- `product`: 跳转到产品详情页
