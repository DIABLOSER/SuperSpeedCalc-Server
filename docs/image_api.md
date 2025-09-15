# 图片管理 API

## 基础信息
- **基础路径**: `/images`
- **数据表**: `image`
- **主要功能**: 图片上传、管理、搜索、统计

## 接口列表

### 1. 获取图片列表
**GET** `/image`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |
| sort_by | string | 否 | 排序字段：fileName, fileSize, createdAt, updatedAt |
| order | string | 否 | 排序方式：asc/desc，默认desc |

#### 请求示例
```bash
GET /image?page=1&per_page=20&sort_by=createdAt&order=desc
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取图片列表成功",
  "data": {
    "items": [
      {
        "objectId": 1,
        "fileName": "20250109_100000_abc12345.jpg",
        "fileSize": 102400,
        "path": "uploads/images/20250109_100000_abc12345.jpg",
        "url": "/uploads/images/20250109_100000_abc12345.jpg",
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

### 2. 获取单个图片信息
**GET** `/images/{object_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| object_id | string | 是 | 图片ID |

#### 请求示例
```bash
GET /images/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取图片信息成功",
  "data": {
    "objectId": 1,
    "fileName": "20250109_100000_abc12345.jpg",
    "fileSize": 102400,
    "path": "uploads/images/20250109_100000_abc12345.jpg",
    "url": "/uploads/images/20250109_100000_abc12345.jpg",
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T10:00:00"
  }
}
```

### 3. 上传单张图片
**POST** `/images/upload`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | file | 是 | 图片文件 |

#### 支持的文件格式
- PNG, JPG, JPEG, GIF, WEBP, BMP

#### 请求示例
```bash
curl -X POST -F "file=@avatar.jpg" http://localhost:8000/images/upload
```

#### 响应示例
```json
{
  "code": 201,
  "message": "图片上传成功",
  "data": {
    "objectId": 1,
    "fileName": "20250109_100000_abc12345.jpg",
    "originalName": "avatar.jpg",
    "fileSize": 102400,
    "filePath": "/uploads/images/20250109_100000_abc12345.jpg",
    "url": "http://localhost:8000/uploads/images/20250109_100000_abc12345.jpg",
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T10:00:00"
  }
}
```

### 4. 批量上传图片
**POST** `/images/upload/multiple`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| files | file[] | 是 | 图片文件数组 |

#### 请求示例
```bash
curl -X POST -F "files=@image1.jpg" -F "files=@image2.jpg" http://localhost:8000/images/upload/multiple
```

#### 响应示例
```json
{
  "code": 201,
  "message": "批量上传成功",
  "data": {
    "uploaded": [
      {
        "objectId": 1,
        "fileName": "20250109_100000_abc12345.jpg",
        "originalName": "image1.jpg",
        "fileSize": 102400,
        "url": "http://localhost:8000/uploads/images/20250109_100000_abc12345.jpg"
      },
      {
        "objectId": 2,
        "fileName": "20250109_100001_def67890.jpg",
        "originalName": "image2.jpg",
        "fileSize": 204800,
        "url": "http://localhost:8000/uploads/images/20250109_100001_def67890.jpg"
      }
    ],
    "failed": [],
    "total": 2,
    "success_count": 2
  }
}
```

### 5. 更新图片信息
**PUT** `/images/{object_id}`

#### 请求体
```json
{
  "originalName": "new_avatar.jpg"
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| originalName | string | 否 | 原始文件名 |

#### 响应示例
```json
{
  "code": 200,
  "message": "图片信息更新成功",
  "data": {
    "objectId": 1,
    "fileName": "20250109_100000_abc12345.jpg",
    "originalName": "new_avatar.jpg",
    "fileSize": 102400,
    "filePath": "/uploads/images/20250109_100000_abc12345.jpg",
    "url": "http://localhost:8000/uploads/images/20250109_100000_abc12345.jpg",
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T11:00:00"
  }
}
```

### 6. 删除图片
**DELETE** `/images/{object_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | int | 是 | 图片ID |

#### 请求示例
```bash
DELETE /images/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "图片删除成功",
  "data": null
}
```

### 7. 搜索图片
**GET** `/images/search`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| q | string | 是 | 搜索关键词 |
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认20 |

#### 请求示例
```bash
GET /images/search?q=avatar&page=1&per_page=10
```

#### 响应示例
```json
{
  "code": 200,
  "message": "搜索图片成功",
  "data": {
    "items": [
      {
        "objectId": 1,
        "fileName": "20250109_100000_abc12345.jpg",
        "originalName": "avatar.jpg",
        "fileSize": 102400,
        "url": "http://localhost:8000/uploads/images/20250109_100000_abc12345.jpg",
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
    "query": "avatar"
  }
}
```

### 8. 获取图片统计
**GET** `/images/stats`

#### 响应示例
```json
{
  "code": 200,
  "message": "获取图片统计成功",
  "data": {
    "total_images": 100,
    "total_size": 10485760,
    "average_size": 104857,
    "file_types": {
      "jpg": 50,
      "png": 30,
      "gif": 20
    }
  }
}
```

### 9. 更新图片URL
**PUT** `/images/{object_id}/url`

#### 请求体
```json
{
  "url": "https://example.com/new-image.jpg"
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| url | string | 是 | 新的图片URL |

#### 响应示例
```json
{
  "code": 200,
  "message": "图片URL更新成功",
  "data": {
    "objectId": 1,
    "fileName": "20250109_100000_abc12345.jpg",
    "originalName": "avatar.jpg",
    "fileSize": 102400,
    "filePath": "/uploads/images/20250109_100000_abc12345.jpg",
    "url": "https://example.com/new-image.jpg",
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T12:00:00"
  }
}
```

### 10. 批量删除图片
**POST** `/images/batch/delete`

#### 请求体
```json
{
  "image_ids": [1, 2, 3]
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image_ids | array | 是 | 要删除的图片ID列表 |

#### 请求示例
```bash
curl -X POST http://localhost:8000/images/batch/delete \
  -H "Content-Type: application/json" \
  -d '{"image_ids": [1, 2, 3]}'
```

#### 响应示例
```json
{
  "code": 200,
  "message": "批量删除成功",
  "data": {
    "deleted_count": 3,
    "deleted_ids": [1, 2, 3]
  }
}
```

### 11. 清空所有图片
**DELETE** `/images/clear`

#### 请求参数
无

#### 请求示例
```bash
curl -X DELETE http://localhost:8000/images/clear
```

#### 响应示例
```json
{
  "code": 200,
  "message": "清空成功",
  "data": {
    "deleted_count": 50
  }
}
```

## 错误响应

### 常见错误码
- `IMAGE_NOT_FOUND`: 图片不存在
- `INVALID_FILE_TYPE`: 不支持的文件类型
- `FILE_TOO_LARGE`: 文件过大
- `UPLOAD_FAILED`: 上传失败
- `SEARCH_QUERY_REQUIRED`: 搜索关键词不能为空
- `IMAGE_UPDATE_FAILED`: 图片更新失败
- `IMAGE_DELETE_FAILED`: 图片删除失败

### 错误响应示例
```json
{
  "code": 400,
  "message": "不支持的文件类型"
}
```
