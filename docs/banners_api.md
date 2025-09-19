# 横幅管理 API

## 基础信息
- **基础路径**: `/banners`
- **数据表**: `banners`
- **主要功能**: 轮播图管理、广告投放、排序控制
- **测试状态**: ✅ 已通过完整测试（100% 成功率）

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
  "data": {
    "items": [
      {
        "objectId": "hv2vi1u8lg",
        "title": "测试1",
        "show": true,
        "click": true,
        "content": null,
        "action": null,
        "imageurl": null,
        "sort_order": 1,
        "createdAt": "2025-09-19T07:01:48.509506",
        "updatedAt": "2025-09-19T07:06:17.952159"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 3,
      "pages": 1,
      "has_next": false,
      "has_prev": false
    }
  }
}
```

### 2. 获取单个横幅
**GET** `/banners/{banner_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| banner_id | string | 是 | 横幅ID |

#### 请求示例
```bash
GET /banners/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "objectId": "hv2vi1u8lg",
    "title": "测试1",
    "show": true,
    "click": true,
    "content": null,
    "action": null,
    "imageurl": null,
    "sort_order": 1,
    "is_active": true,
    "createdAt": "2025-09-19T07:01:48.509506",
    "updatedAt": "2025-09-19T07:06:17.952159"
  }
}
```

### 3. 获取活跃横幅列表
**GET** `/banners/active`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| limit | int | 否 | 限制返回数量 |

#### 请求示例
```bash
GET /banners/active?limit=5
```

#### 响应示例
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "banners": [
      {
        "objectId": "hv2vi1u8lg",
        "title": "测试1",
        "show": true,
        "click": true,
        "content": null,
        "action": null,
        "imageurl": null,
        "sort_order": 1,
        "createdAt": "2025-09-19T07:01:48.509506",
        "updatedAt": "2025-09-19T07:06:17.952159"
      }
    ],
    "total": 3,
    "action_types": {
      "download": "下载文件",
      "modal": "打开弹窗",
      "none": "无动作",
      "page": "跳转到应用内页面",
      "share": "分享功能",
      "url": "跳转到外部链接"
    }
  }
}
```

### 4. 获取横幅统计信息
**GET** `/banners/stats`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| admin_user_id | string | 是 | 管理员用户ID |

#### 请求示例
```bash
GET /banners/stats?admin_user_id=1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取横幅统计成功",
  "data": {
    "overview": {
      "total_banners": 3,
      "active_banners": 3,
      "visible_banners": 3
    }
  }
}
```

### 5. 创建横幅
**POST** `/banners`

#### 请求体
```json
{
  "title": "欢迎横幅",
  "show": true,
  "click": true,
  "content": "横幅内容描述",
  "action": "https://example.com",
  "imageurl": "https://example.com/banner1.jpg",
  "sort_order": 1
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 横幅标题 |
| show | bool | 否 | 是否显示，默认true |
| click | bool | 否 | 是否可点击，默认true |
| content | string | 否 | 横幅内容描述 |
| action | string | 否 | 动作值 |
| imageurl | string | 否 | 横幅图片URL |
| sort_order | int | 否 | 排序权重，默认0 |

#### 响应示例
```json
{
  "code": 201,
  "message": "Banner created successfully",
  "data": {
    "objectId": "ni7zjqlrqj",
    "title": "API测试横幅",
    "show": true,
    "click": true,
    "content": "这是一个通过API创建的测试横幅",
    "action": "https://example.com/test",
    "imageurl": "https://example.com/test-banner.jpg",
    "sort_order": 10,
    "is_active": true,
    "createdAt": "2025-09-19T07:21:47.940357",
    "updatedAt": "2025-09-19T07:21:47.940357"
  }
}
```

### 6. 更新横幅排序权重
**POST** `/banners/{banner_id}/sort-order`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| banner_id | string | 是 | 横幅ID |

#### 请求体
```json
{
  "sort_order": 5,
  "admin_user_id": "1"
}
```

#### 请求示例
```bash
curl -X POST http://localhost:8000/banners/1/sort-order \
  -H "Content-Type: application/json" \
  -d '{"sort_order": 5, "admin_user_id": "1"}'
```

#### 响应示例
```json
{
  "code": 200,
  "message": "Banner sort order updated from 10 to 20",
  "data": {
    "objectId": "ni7zjqlrqj",
    "title": "API测试横幅",
    "old_sort_order": 10,
    "new_sort_order": 20
  }
}
```

### 7. 记录横幅展示
**POST** `/banners/{banner_id}/view`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| banner_id | string | 是 | 横幅ID |

#### 请求示例
```bash
POST /banners/1/view
```

#### 响应示例
```json
{
  "code": 200,
  "message": "Banner view tracked",
  "data": {
    "banner_id": "hv2vi1u8lg",
    "title": "测试1"
  }
}
```

### 8. 记录横幅点击
**POST** `/banners/{banner_id}/click`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| banner_id | string | 是 | 横幅ID |

#### 请求示例
```bash
POST /banners/1/click
```

#### 响应示例
```json
{
  "code": 200,
  "message": "Banner click tracked",
  "data": {
    "banner_id": "hv2vi1u8lg",
    "title": "测试1",
    "action": null
  }
}
```

### 9. 更新横幅
**PUT** `/banners/{banner_id}`

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
  "message": "Banner updated successfully",
  "data": {
    "objectId": "ni7zjqlrqj",
    "title": "API测试横幅（已更新）",
    "show": true,
    "click": true,
    "content": "这是一个更新后的测试横幅",
    "action": "https://example.com/updated",
    "imageurl": "https://example.com/test-banner.jpg",
    "sort_order": 15,
    "is_active": true,
    "createdAt": "2025-09-19T07:21:47.940357",
    "updatedAt": "2025-09-19T07:21:52.039385"
  }
}
```

### 5. 删除横幅
**DELETE** `/banners/{banner_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| banner_id | string | 是 | 横幅ID |

#### 请求示例
```bash
DELETE /banners/1
```

#### 响应示例
```json
{
  "code": 200,
  "message": "Banner deleted successfully",
  "data": {
    "banner_id": "ni7zjqlrqj",
    "title": "API测试横幅（已更新）",
    "show": true,
    "click": true,
    "action": "https://example.com/updated"
  }
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
  "data": {
    "banners": [
      {
        "objectId": 1,
        "title": "欢迎横幅",
        "image_url": "https://example.com/banner1.jpg",
        "action_type": "url",
        "action_value": "https://example.com",
        "status": "active",
        "sort_order": 1,
        "start_date": "2025-01-09T00:00:00",
        "end_date": "2025-12-31T23:59:59"
      }
    ],
    "total": 1,
    "action_types": ["url", "app_page", "product"]
  }
}
```

### 7. 更新横幅排序
**PUT** `/banners/{banner_id}/sort`

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
  "data": {
    "objectId": 1,
    "title": "欢迎横幅",
    "image_url": "https://example.com/banner1.jpg",
    "action_type": "url",
    "action_value": "https://example.com",
    "status": "active",
    "sort_order": 3,
    "start_date": "2025-01-09T00:00:00",
    "end_date": "2025-12-31T23:59:59",
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T12:00:00"
  }
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
curl -X PUT http://localhost:8000/banners/batch-status \
  -H "Content-Type: application/json" \
  -d '{"banner_ids": [1, 2, 3], "status": "inactive"}'
```

#### 响应示例
```json
{
  "code": 200,
  "message": "批量更新横幅状态成功",
  "data": {
    "success_count": 3,
    "failed_count": 0,
    "results": [
      {
        "banner_id": 1,
        "status": "success"
      },
      {
        "banner_id": 2,
        "status": "success"
      },
      {
        "banner_id": 3,
        "status": "success"
      }
    ]
  }
}
```

### 9. 获取横幅统计
**GET** `/banners/stats`

#### 响应示例
```json
{
  "code": 200,
  "message": "获取横幅统计成功",
  "data": {
    "total_banners": 10,
    "active_banners": 8,
    "inactive_banners": 2,
    "action_types": {
      "url": 5,
      "app_page": 3,
      "product": 2
    },
    "expired_banners": 1,
    "upcoming_banners": 2
  }
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
curl -X POST -F "file=@banner.jpg" http://localhost:8000/banners/upload
```

#### 响应示例
```json
{
  "code": 201,
  "message": "横幅图片上传成功",
  "data": {
    "image_url": "http://localhost:8000/uploads/banners/20250109_100000_abc12345.jpg",
    "file_size": 102400,
    "uploaded_at": "2025-01-09T10:00:00"
  }
}
```

## 错误响应

### 常见错误码
- `BANNER_NOT_FOUND`: 横幅不存在
- `MISSING_REQUIRED_FIELD`: 缺少必填字段
- `INVALID_ACTION_TYPE`: 无效的动作类型
- `INVALID_STATUS`: 无效的状态
- `BANNER_CREATE_FAILED`: 横幅创建失败
- `BANNER_UPDATE_FAILED`: 横幅更新失败
- `BANNER_DELETE_FAILED`: 横幅删除失败
- `PERMISSION_DENIED`: 权限不足（需要管理员权限）

### 错误响应示例
```json
{
  "code": 400,
  "message": "Title is required"
}
```

```json
{
  "code": 403,
  "message": "Permission denied. Admin access required."
}
```

```json
{
  "code": 404,
  "message": "Banner not found"
}
```

## 数据模型

### Banners 表结构
| 字段 | 类型 | 说明 |
|------|------|------|
| objectId | string | 主键ID |
| title | string | 横幅标题 |
| show | boolean | 是否显示 |
| click | boolean | 是否可点击 |
| content | string | 横幅内容描述 |
| action | string | 动作值（URL或页面路径） |
| imageurl | string | 图片URL |
| sort_order | int | 排序权重 |
| createdAt | datetime | 创建时间 |
| updatedAt | datetime | 更新时间 |

**注意**: `is_active` 字段是动态计算的，基于 `show` 字段的值，不会存储在数据库中。

### 动作类型说明
- `url`: 跳转到外部链接
- `page`: 跳转到应用内页面
- `download`: 下载文件
- `modal`: 打开弹窗
- `share`: 分享功能
- `none`: 无动作

## 测试结果

### 接口测试状态
| 接口 | 方法 | 状态 | 说明 |
|------|------|------|------|
| 获取横幅列表 | GET /banners | ✅ | 支持分页，返回格式正确 |
| 获取单个横幅 | GET /banners/{id} | ✅ | 正常返回横幅详情 |
| 获取活跃横幅 | GET /banners/active | ✅ | 返回活跃横幅和动作类型 |
| 获取统计信息 | GET /banners/stats | ✅ | 返回横幅统计数据 |
| 创建横幅 | POST /banners | ✅ | 无需管理员权限验证 |
| 更新横幅 | PUT /banners/{id} | ✅ | 支持部分字段更新 |
| 更新排序 | POST /banners/{id}/sort-order | ✅ | 排序权重更新正常 |
| 记录展示 | POST /banners/{id}/view | ✅ | 展示追踪功能正常 |
| 记录点击 | POST /banners/{id}/click | ✅ | 点击追踪功能正常 |
| 删除横幅 | DELETE /banners/{id} | ✅ | 删除功能正常 |

### 测试覆盖率
- **总接口数**: 10个
- **测试通过**: 10个
- **测试失败**: 0个
- **成功率**: 100%

### 注意事项
1. 创建和删除横幅接口都不需要管理员权限验证
2. 所有接口都使用统一的响应格式
3. 横幅ID使用字符串格式的objectId
4. 时间格式使用ISO 8601标准
5. `is_active` 字段是动态计算的，基于 `show` 字段的值
