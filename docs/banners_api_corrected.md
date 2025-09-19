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
  "message": "获取活跃横幅成功",
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
        "is_active": true,
        "createdAt": "2025-09-19T07:01:48.509506",
        "updatedAt": "2025-09-19T07:06:17.952159"
      }
    ],
    "total": 1
  }
}
```

### 4. 获取横幅统计
**GET** `/banners/stats`

#### 请求示例
```bash
GET /banners/stats
```

#### 响应示例
```json
{
  "code": 200,
  "message": "获取横幅统计成功",
  "data": {
    "total_banners": 10,
    "active_banners": 5,
    "inactive_banners": 5,
    "total_views": 1000,
    "total_clicks": 100
  }
}
```

### 5. 创建横幅
**POST** `/banners`

#### 请求体
```json
{
  "title": "新横幅",
  "show": true,
  "click": true,
  "content": "横幅内容",
  "action": "url",
  "imageurl": "https://example.com/banner.jpg",
  "sort_order": 1
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 横幅标题 |
| show | bool | 否 | 是否显示，默认true |
| click | bool | 否 | 是否可点击，默认true |
| content | string | 否 | 横幅内容 |
| action | string | 否 | 动作类型：url, page, download, modal, share, none |
| imageurl | string | 否 | 图片URL |
| sort_order | int | 否 | 排序顺序，默认0 |

#### 响应示例
```json
{
  "code": 201,
  "message": "横幅创建成功",
  "data": {
    "objectId": "new_banner_id",
    "title": "新横幅",
    "show": true,
    "click": true,
    "content": "横幅内容",
    "action": "url",
    "imageurl": "https://example.com/banner.jpg",
    "sort_order": 1,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T10:00:00"
  }
}
```

### 6. 更新横幅
**PUT** `/banners/{banner_id}`

#### 请求体
```json
{
  "title": "更新后的横幅标题",
  "show": false,
  "content": "更新后的内容"
}
```

#### 请求参数说明
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 否 | 横幅标题 |
| show | bool | 否 | 是否显示 |
| click | bool | 否 | 是否可点击 |
| content | string | 否 | 横幅内容 |
| action | string | 否 | 动作类型 |
| imageurl | string | 否 | 图片URL |
| sort_order | int | 否 | 排序顺序 |

#### 响应示例
```json
{
  "code": 200,
  "message": "横幅更新成功",
  "data": {
    "objectId": "banner_id",
    "title": "更新后的横幅标题",
    "show": false,
    "click": true,
    "content": "更新后的内容",
    "action": "url",
    "imageurl": "https://example.com/banner.jpg",
    "sort_order": 1,
    "createdAt": "2025-01-09T10:00:00",
    "updatedAt": "2025-01-09T11:00:00"
  }
}
```

### 7. 更新横幅排序
**POST** `/banners/{banner_id}/sort-order`

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
    "banner_id": "banner_id",
    "old_sort_order": 1,
    "new_sort_order": 3
  }
}
```

### 8. 记录横幅查看
**POST** `/banners/{banner_id}/view`

#### 请求示例
```bash
POST /banners/banner_id/view
```

#### 响应示例
```json
{
  "code": 200,
  "message": "查看记录成功",
  "data": {
    "banner_id": "banner_id",
    "viewed_at": "2025-01-09T10:00:00"
  }
}
```

### 9. 记录横幅点击
**POST** `/banners/{banner_id}/click`

#### 请求示例
```bash
POST /banners/banner_id/click
```

#### 响应示例
```json
{
  "code": 200,
  "message": "点击记录成功",
  "data": {
    "banner_id": "banner_id",
    "clicked_at": "2025-01-09T10:00:00"
  }
}
```

### 10. 删除横幅
**DELETE** `/banners/{banner_id}`

#### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| banner_id | string | 是 | 横幅ID |

#### 请求示例
```bash
DELETE /banners/banner_id
```

#### 响应示例
```json
{
  "code": 200,
  "message": "横幅删除成功",
  "data": {
    "banner_id": "banner_id",
    "deleted_at": "2025-01-09T12:00:00"
  }
}
```

## 数据表结构

### Banners 表字段
| 字段名 | 类型 | 说明 |
|--------|------|------|
| objectId | string | 主键ID |
| title | string | 横幅标题 |
| show | bool | 是否显示 |
| click | bool | 是否可点击 |
| content | string | 横幅内容 |
| action | string | 动作类型 |
| imageurl | string | 图片URL |
| sort_order | int | 排序顺序 |
| createdAt | datetime | 创建时间 |
| updatedAt | datetime | 更新时间 |

**注意**: `is_active` 字段是动态计算的，基于 `show` 字段的值，不会存储在数据库中。

## 动作类型说明
- `url`: 跳转到URL
- `page`: 跳转到应用内页面
- `download`: 下载文件
- `modal`: 显示弹窗
- `share`: 分享功能
- `none`: 无动作

## 错误响应

### 常见错误码
- `BANNER_NOT_FOUND`: 横幅不存在
- `MISSING_REQUIRED_FIELD`: 缺少必填字段
- `INVALID_ACTION_TYPE`: 无效的动作类型
- `PERMISSION_DENIED`: 权限不足

### 错误响应示例
```json
{
  "code": 404,
  "message": "Banner not found"
}
```

## 注意事项

1. **权限控制**：
   - 创建和删除横幅接口都不需要管理员权限验证
   - 任何人都可以查看横幅列表和详情

2. **排序功能**：
   - `sort_order` 数值越小，排序越靠前
   - 可以通过更新排序接口调整横幅显示顺序

3. **状态管理**：
   - `is_active` 字段是动态计算的，基于 `show` 字段的值
   - 只有 `show=true` 的横幅才会在活跃列表中显示

4. **统计功能**：
   - 提供查看和点击统计接口
   - 统计数据可用于分析横幅效果
