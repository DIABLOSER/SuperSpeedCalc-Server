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
  "message": "Image uploaded successfully",
  "data": {
    "objectId": "djvonwqq9q",
    "fileName": "20250921_140147_65a188e4.png",
    "path": "uploads/images/20250921_140147_65a188e4.png",
    "url": "/uploads/images/20250921_140147_65a188e4.png",
    "fileSize": 287,
    "createdAt": "2025-09-21T14:01:47",
    "updatedAt": "2025-09-21T14:01:47"
  }
}
```

### 4. 批量上传图片
**POST** `/images/upload/multiple`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| files | file[] | 是 | 图片文件数组 |

#### 支持的文件格式
- PNG, JPG, JPEG, GIF, WEBP, BMP

#### 请求示例
```bash
curl -X POST -F "files=@image1.jpg" -F "files=@image2.jpg" -F "files=@image3.png" http://localhost:8000/images/upload/multiple
```

#### 成功响应示例
```json
{
  "code": 201,
  "message": "All 3 files uploaded successfully",
  "data": {
    "images": [
      {
        "objectId": "djvonwqq9q",
        "fileName": "20250921_140148_75767fe4.png",
        "path": "uploads/images/20250921_140148_75767fe4.png",
        "url": "/uploads/images/20250921_140148_75767fe4.png",
        "fileSize": 287,
        "createdAt": "2025-09-21T14:01:48",
        "updatedAt": "2025-09-21T14:01:48"
      },
      {
        "objectId": "1mdeap865c",
        "fileName": "20250921_140148_fb84b3a2.png",
        "path": "uploads/images/20250921_140148_fb84b3a2.png",
        "url": "/uploads/images/20250921_140148_fb84b3a2.png",
        "fileSize": 287,
        "createdAt": "2025-09-21T14:01:48",
        "updatedAt": "2025-09-21T14:01:48"
      }
    ],
    "uploaded_count": 3,
    "total_files": 3
  }
}
```

#### 部分失败响应示例
```json
{
  "code": 201,
  "message": "Uploaded 2 files successfully, 1 files failed",
  "data": {
    "images": [
      {
        "objectId": "abc123",
        "fileName": "20250921_140148_75767fe4.png",
        "path": "uploads/images/20250921_140148_75767fe4.png",
        "url": "/uploads/images/20250921_140148_75767fe4.png",
        "fileSize": 287,
        "createdAt": "2025-09-21T14:01:48",
        "updatedAt": "2025-09-21T14:01:48"
      }
    ],
    "uploaded_count": 2,
    "total_files": 3,
    "errors": [
      "File 3 (test.txt): File type not allowed"
    ]
  }
}
```

#### 响应字段说明
| 字段 | 类型 | 说明 |
|------|------|------|
| images | array | 成功上传的图片列表 |
| uploaded_count | int | 成功上传的文件数量 |
| total_files | int | 总文件数量 |
| errors | array | 失败文件的错误信息（可选） |

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

## 测试状态

### 最新测试结果
- **测试时间**: 2025-09-21
- **测试环境**: 开发环境 (localhost:8000)
- **测试状态**: ✅ 全部通过

### 已验证功能
- ✅ 单个图片上传 (`POST /images/upload`)
- ✅ 批量图片上传 (`POST /images/upload/multiple`)
- ✅ 文件格式验证 (PNG, JPG, JPEG, GIF, WEBP, BMP)
- ✅ 错误处理机制
- ✅ 空文件处理
- ✅ 无效文件类型处理
- ✅ 响应格式统一性
- ✅ 数据库记录创建
- ✅ 文件存储功能
- ✅ 图片列表查询 (`GET /images/`)
- ✅ 图片统计信息 (`GET /images/stats`)

### 测试数据统计
- **测试图片数量**: 7张 (1个单张 + 6个批量)
- **文件大小范围**: 287-289 bytes (测试图片)
- **上传成功率**: 100% (有效文件)
- **当前图片总数**: 65张
- **响应时间**: < 200ms

### 接口响应格式
所有接口均使用统一响应格式：
```json
{
  "code": 状态码,
  "message": "响应消息",
  "data": 响应数据
}
```

### 批量上传特殊说明
- 支持同时上传多个文件
- 部分文件失败时仍返回成功状态码 (201)
- 错误信息包含在 `data.errors` 字段中
- 成功上传的文件信息包含在 `data.images` 字段中
