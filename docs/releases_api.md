# 应用发布 API

## 基础信息
- **基础路径**: `/releases`
- **数据表**: `app_releases`
- **主要功能**: APK版本管理、更新控制、发布管理

## 接口列表

### 1. 获取发布记录列表
**GET** `/releases`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| per_page | int | 否 | 每页数量，默认10 |
| title | string | 否 | 应用名称筛选 |
| environment | string | 否 | 环境筛选：production, development, testing |

#### 请求示例
```bash
GET /releases?page=1&per_page=10&title=SuperSpeedCalc&environment=production
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取发布记录成功",
  "data": {
    "items": [
      {
        "objectId": 1,
        "title": "SuperSpeedCalc",
        "version_name": "1.0.0",
        "version_code": 100,
        "content": "初始版本发布",
        "download_url": "https://example.com/app-v1.0.0.apk",
        "environment": "production",
        "is_test": false,
        "is_update": true,
        "force_update": false,
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

### 2. 获取最新版本
**GET** `/releases/latest`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| environment | string | 是 | 发布环境（例如：测试、taptap、正式） |
| is_update | string | 是 | 是否更新（true/false/1/0/yes/no/on/off） |

#### 请求示例
```bash
GET /releases/latest?environment=正式&is_update=true
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取最新版本成功",
  "data": {
    "objectId": 1,
    "title": "SuperSpeedCalc",
    "version_name": "1.2.3",
    "version_code": 123,
    "content": "修复已知问题，优化用户体验",
    "download_url": "https://example.com/app-v1.2.3.apk",
    "environment": "正式",
    "is_test": false,
    "is_update": true,
    "force_update": false,
    "createdAt": "2025-01-09T12:00:00",
    "updatedAt": "2025-01-09T12:00:00"
  }
}
```

#### 错误响应示例
```json
{
  "code": 400,
  "message": "缺少必需参数：environment"
}
```

```json
{
  "code": 404,
  "message": "未找到环境为 正式 且更新状态为 true 的发布记录"
}
```

### 3. 获取单个发布记录
**GET** `/releases/{object_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| object_id | string | 是 | 发布记录ID |

#### 请求示例
```bash
GET /releases/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取发布记录成功",
  "data": {
    "objectId": 1,
    "title": "SuperSpeedCalc",
    "version_name": "1.0.0",
    "version_code": 1,
    "content": "初始版本发布",
    "download_url": "https://example.com/app-v1.0.0.apk",
    "environment": "production",
    "is_test": false,
    "is_update": true,
    "force_update": false,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T10:00:00"
  }
}
```

### 4. 创建发布记录
**POST** `/releases`

#### 请求体
```json
{
  "title": "SuperSpeedCalc",
  "version_name": "1.0.0",
  "version_code": 1,
  "content": "初始版本发布",
  "download_url": "https://example.com/app-v1.0.0.apk",
  "environment": "production",
  "is_test": false,
  "is_update": true,
  "force_update": false
}
```

**注意**: 所有字段都是可选的，可以只提供需要的字段。

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 否 | 应用名称 |
| version_name | string | 否 | 版本名称（如1.0.0），可选 |
| version_code | int | 否 | 版本代码（数字） |
| content | string | 否 | 更新日志 |
| download_url | string | 否 | 下载链接 |
| environment | string | 否 | 环境：production/development/testing |
| is_test | bool | 否 | 是否为测试版本，默认false |
| is_update | bool | 否 | 是否为更新，默认false |
| force_update | bool | 否 | 是否强制更新，默认false |

#### 响应示例
```json
{
  "code": 201,
  "message": "发布记录创建成功",
  "data": {
    "objectId": 1,
    "title": "SuperSpeedCalc",
    "version_name": "1.0.0",
    "version_code": 1,
    "content": "初始版本发布",
    "download_url": "https://example.com/app-v1.0.0.apk",
    "environment": "production",
    "is_test": false,
    "is_update": true,
    "force_update": false,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T10:00:00"
  }
}
```

### 5. 更新发布记录
**PUT** `/releases/{object_id}`

#### 请求体
```json
{
  "title": "SuperSpeedCalc",
  "version_name": "1.0.1",
  "version_code": 2,
  "content": "修复已知问题",
  "download_url": "https://example.com/app-v1.0.1.apk",
  "environment": "production",
  "is_test": false,
  "is_update": true,
  "force_update": true
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 否 | 应用名称 |
| version_name | string | 否 | 版本名称，可选 |
| version_code | int | 否 | 版本代码 |
| content | string | 否 | 更新日志 |
| download_url | string | 否 | 下载链接 |
| environment | string | 否 | 环境 |
| is_update | bool | 否 | 是否为更新 |
| force_update | bool | 否 | 是否强制更新 |

#### 响应示例
```json
{
  "code": 200,
  "message": "发布记录更新成功",
  "data": {
    "objectId": 1,
    "title": "SuperSpeedCalc",
    "version_name": "1.0.1",
    "version_code": 2,
    "content": "修复已知问题",
    "download_url": "https://example.com/app-v1.0.1.apk",
    "environment": "production",
    "is_update": true,
    "force_update": true,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T11:00:00"
  }
}
```

### 6. 删除发布记录
**DELETE** `/releases/{object_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| object_id | string | 是 | 发布记录ID |

#### 请求示例
```bash
DELETE /releases/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "发布记录删除成功",
  "data": null
}
```

### 7. 获取发布记录数量
**GET** `/releases/count`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 否 | 应用名称筛选 |
| environment | string | 否 | 环境筛选 |

#### 请求示例
```bash
GET /releases/count?title=SuperSpeedCalc&environment=production
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取发布记录数量成功",
  "data": {
    "count": 5
  }
}
```

### 8. 上传APK文件
**POST** `/releases/upload-apk`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | file | 是 | APK文件 |
| release_id | string | 否 | 发布记录ID（可选，用于绑定到指定发布记录） |

#### 请求示例
```bash
curl -X POST -F "file=@app-v1.0.1.apk" http://localhost:8000/releases/upload-apk
```

#### 响应示例
```json
{
  "code": 201,
  "message": "APK uploaded successfully",
  "data": {
    "success": true,
    "data": {
      "fileName": "1704787200000.apk",
      "path": "uploads/apk/1704787200000.apk",
      "url": "/uploads/apk/1704787200000.apk",
      "fileSize": 1024000
    },
    "message": "APK uploaded successfully"
  }
}
```

## 错误响应

### 常见错误码
- `RELEASE_NOT_FOUND`: 发布记录不存在
- `LATEST_RELEASE_NOT_FOUND`: 未找到符合条件的最新版本
- `MISSING_REQUIRED_FIELD`: 缺少必填字段
- `INVALID_VERSION_CODE`: 无效的版本代码
- `INVALID_UPDATE_PARAMETER`: 无效的更新参数格式
- `DUPLICATE_VERSION`: 版本已存在
- `INVALID_FILE_TYPE`: 不支持的文件类型
- `RELEASE_CREATE_FAILED`: 发布记录创建失败
- `RELEASE_UPDATE_FAILED`: 发布记录更新失败
- `RELEASE_DELETE_FAILED`: 发布记录删除失败

### 错误响应示例
```json
{
  "code": 400,
  "message": "version_code 必须是整数"
}
```
