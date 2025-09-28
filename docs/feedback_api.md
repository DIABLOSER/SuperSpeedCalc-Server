# 意见反馈系统完整文档

## 🎯 功能概述

意见反馈系统为SuperSpeedCalc-Server项目提供了完整的用户反馈管理功能，包括数据模型、API接口、数据库迁移和详细文档。系统支持用户创建、查看、更新反馈，管理员处理反馈、回复用户，以及完整的统计和搜索功能。

## 📋 系统架构

### 1. 数据模型设计 ✅

**文件**: `models/feedback.py`

创建了功能完善的Feedback模型，包含以下特性：

- **基础字段**: objectId, createdAt, updatedAt
- **用户关联**: user (支持匿名反馈)
- **反馈信息**: feedback_type, title, content
- **状态管理**: status, priority
- **联系信息**: contact
- **设备信息**: device_info (JSON), app_version, os_info
- **附件支持**: attachments (JSON数组)
- **管理员功能**: admin_reply, admin_reply_at, admin_user
- **用户评分**: rating (1-5分)
- **公开设置**: is_public
- **标签系统**: tags (JSON数组)

### 2. API路由实现 ✅

**目录**: `routes/feedback/`

#### 创建功能 (`create.py`)
- `POST /api/feedback/create` - 创建单个反馈
- `POST /api/feedback/batch_create` - 批量创建反馈

#### 查询功能 (`read.py`)
- `GET /api/feedback/list` - 获取反馈列表（支持分页、过滤、搜索）
- `GET /api/feedback/{id}` - 获取反馈详情
- `GET /api/feedback/stats` - 获取统计信息
- `GET /api/feedback/my` - 获取我的反馈
- `GET /api/feedback/public` - 获取公开反馈

#### 更新功能 (`update.py`)
- `PUT /api/feedback/{id}` - 更新反馈信息
- `PUT /api/feedback/{id}/status` - 更新状态（管理员）
- `PUT /api/feedback/{id}/priority` - 更新优先级（管理员）
- `POST /api/feedback/{id}/reply` - 管理员回复
- `POST /api/feedback/{id}/attachments` - 添加附件
- `DELETE /api/feedback/{id}/attachments` - 移除附件

#### 删除功能 (`delete.py`)
- `DELETE /api/feedback/{id}` - 删除反馈
- `DELETE /api/feedback/batch_delete` - 批量删除
- `DELETE /api/feedback/{id}/soft_delete` - 软删除
- `DELETE /api/feedback/cleanup` - 清理旧反馈（管理员）

### 3. 数据库迁移 ✅

**文件**: `scripts/migrate_add_feedback_table.py`

- 自动创建feedback表
- 包含完整的表结构信息
- 支持外键关联
- 提供详细的迁移日志

### 4. 主应用集成 ✅

**文件**: `app.py`

- 注册反馈路由蓝图
- 更新模型导入
- 集成到数据库初始化

### 5. 测试脚本 ✅

**文件**: `test_feedback_api.py`

提供完整的API测试功能：
- 创建反馈测试
- 查询功能测试
- 更新功能测试
- 管理员功能测试
- 统计信息测试

## 🚀 功能特性

### 反馈类型
- `bug` - Bug报告
- `feature` - 功能建议
- `complaint` - 投诉
- `praise` - 表扬
- `other` - 其他

### 状态管理
- `pending` - 待处理
- `processing` - 处理中
- `resolved` - 已解决
- `closed` - 已关闭

### 优先级
- `low` - 低
- `medium` - 中
- `high` - 高
- `urgent` - 紧急

### 权限控制
- **用户权限**: 创建、查看自己的反馈、查看公开反馈
- **管理员权限**: 查看所有反馈、更新状态、回复反馈、清理数据

### 高级功能
- 支持匿名反馈
- 设备信息收集
- 附件上传
- 标签分类
- 搜索功能
- 分页支持
- 统计信息
- 批量操作

## 📊 数据库表结构

```sql
CREATE TABLE feedback (
    "objectId" VARCHAR(20) NOT NULL PRIMARY KEY,
    user VARCHAR(20),
    feedback_type VARCHAR(20) NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,
    priority VARCHAR(20) NOT NULL,
    contact VARCHAR(100),
    device_info TEXT,
    app_version VARCHAR(50),
    os_info VARCHAR(100),
    attachments TEXT,
    admin_reply TEXT,
    admin_reply_at DATETIME,
    admin_user VARCHAR(20),
    rating INTEGER,
    is_public BOOLEAN NOT NULL,
    tags TEXT,
    "createdAt" DATETIME NOT NULL,
    "updatedAt" DATETIME NOT NULL,
    FOREIGN KEY(user) REFERENCES my_user ("objectId"),
    FOREIGN KEY(admin_user) REFERENCES my_user ("objectId")
);
```

## 🔧 使用方法

### 1. 运行迁移脚本
```bash
python scripts/migrate_add_feedback_table.py
```

### 2. 启动服务器
```bash
python app.py
```

### 3. 测试API
```bash
python test_feedback_api.py
```

### 4. 查看API文档
查看本文档获取完整的API使用说明。

## 📈 统计信息

- **总反馈数**: 支持统计所有反馈数量
- **按状态统计**: 待处理、处理中、已解决、已关闭
- **按类型统计**: Bug、功能建议、投诉、表扬、其他
- **按优先级统计**: 低、中、高、紧急
- **解决率**: 已解决反馈占比

---

## API接口详细说明

## 基础信息

- **基础URL**: `/api/feedback`
- **认证方式**: 通过请求参数传递用户ID和管理员标识
- **数据格式**: JSON

## 反馈类型

| 类型 | 说明 |
|------|------|
| `bug` | Bug报告 |
| `feature` | 功能建议 |
| `complaint` | 投诉 |
| `praise` | 表扬 |
| `other` | 其他 |

## 反馈状态

| 状态 | 说明 |
|------|------|
| `pending` | 待处理 |
| `processing` | 处理中 |
| `resolved` | 已解决 |
| `closed` | 已关闭 |

## 优先级

| 优先级 | 说明 |
|--------|------|
| `low` | 低 |
| `medium` | 中 |
| `high` | 高 |
| `urgent` | 紧急 |

## API接口

### 1. 创建反馈

**POST** `/api/feedback/create`

创建新的意见反馈。

#### 请求参数

```json
{
  "user_id": "string",           // 用户ID（可选，支持匿名反馈）
  "feedback_type": "string",     // 反馈类型（必填）
  "title": "string",            // 反馈标题（必填，最大200字符）
  "content": "string",          // 反馈内容（必填）
  "priority": "string",         // 优先级（可选，默认medium）
  "contact": "string",          // 联系方式（可选，最大100字符）
  "device_info": {              // 设备信息（可选）
    "device": "string",
    "os": "string",
    "browser": "string"
  },
  "app_version": "string",      // 应用版本（可选，最大50字符）
  "os_info": "string",         // 操作系统信息（可选，最大100字符）
  "attachments": ["string"],    // 附件列表（可选）
  "tags": ["string"],           // 标签列表（可选）
  "is_public": boolean,         // 是否公开（可选，默认false）
  "rating": integer             // 评分（可选，1-5分）
}
```

#### 响应示例

```json
{
  "success": true,
  "message": "反馈创建成功",
  "data": {
    "feedback": {
      "objectId": "abc123def4",
      "user": "user123",
      "feedback_type": "bug",
      "title": "登录页面显示异常",
      "content": "在登录时页面出现白屏",
      "status": "pending",
      "priority": "medium",
      "contact": "user@example.com",
      "device_info": {
        "device": "iPhone 12",
        "os": "iOS 15.0"
      },
      "app_version": "1.0.0",
      "os_info": "iOS 15.0",
      "attachments": [],
      "tags": ["登录", "显示"],
      "is_public": false,
      "rating": null,
      "createdAt": "2024-01-01T00:00:00Z",
      "updatedAt": "2024-01-01T00:00:00Z",
      "can_edit": true,
      "can_view": true,
      "is_resolved": false,
      "is_high_priority": false
    }
  }
}
```

### 2. 批量创建反馈

**POST** `/api/feedback/batch_create`

批量创建多个反馈。

#### 请求参数

```json
{
  "user_id": "string",
  "feedbacks": [
    {
      "feedback_type": "string",
      "title": "string",
      "content": "string",
      // ... 其他字段同单个创建
    }
  ]
}
```

### 3. 获取反馈列表

**GET** `/api/feedback/list`

获取反馈列表，支持分页和过滤。

#### 查询参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `page` | integer | 页码（默认1） |
| `per_page` | integer | 每页数量（默认20） |
| `feedback_type` | string | 反馈类型过滤 |
| `status` | string | 状态过滤 |
| `priority` | string | 优先级过滤 |
| `user_id` | string | 用户ID过滤 |
| `is_public` | boolean | 是否公开过滤 |
| `search` | string | 搜索关键词（标题和内容） |
| `sort_by` | string | 排序字段（默认createdAt） |
| `sort_order` | string | 排序方向（asc/desc，默认desc） |
| `current_user_id` | string | 当前用户ID |
| `is_admin` | boolean | 是否为管理员 |

#### 响应示例

```json
{
  "success": true,
  "data": {
    "feedbacks": [
      {
        "objectId": "abc123def4",
        "user": {
          "objectId": "user123",
          "username": "testuser",
          "avatar": "avatar.jpg",
          "admin": false
        },
        "feedback_type": "bug",
        "title": "登录页面显示异常",
        "content": "在登录时页面出现白屏",
        "status": "pending",
        "priority": "medium",
        "createdAt": "2024-01-01T00:00:00Z",
        "updatedAt": "2024-01-01T00:00:00Z",
        "can_edit": true,
        "can_view": true,
        "is_resolved": false,
        "is_high_priority": false
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 100,
      "pages": 5,
      "has_prev": false,
      "has_next": true
    }
  }
}
```

### 4. 获取反馈详情

**GET** `/api/feedback/{feedback_id}`

获取指定反馈的详细信息。

#### 查询参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `current_user_id` | string | 当前用户ID |
| `is_admin` | boolean | 是否为管理员 |

#### 响应示例

```json
{
  "success": true,
  "data": {
    "feedback": {
      "objectId": "abc123def4",
      "user": {
        "objectId": "user123",
        "username": "testuser",
        "avatar": "avatar.jpg",
        "admin": false
      },
      "feedback_type": "bug",
      "title": "登录页面显示异常",
      "content": "在登录时页面出现白屏",
      "status": "pending",
      "priority": "medium",
      "contact": "user@example.com",
      "device_info": {
        "device": "iPhone 12",
        "os": "iOS 15.0"
      },
      "app_version": "1.0.0",
      "os_info": "iOS 15.0",
      "attachments": [],
      "tags": ["登录", "显示"],
      "is_public": false,
      "rating": null,
      "admin_reply": null,
      "admin_reply_at": null,
      "admin_user": null,
      "createdAt": "2024-01-01T00:00:00Z",
      "updatedAt": "2024-01-01T00:00:00Z",
      "can_edit": true,
      "can_view": true,
      "is_resolved": false,
      "is_high_priority": false
    }
  }
}
```

### 5. 获取反馈统计

**GET** `/api/feedback/stats`

获取反馈统计信息。

#### 响应示例

```json
{
  "success": true,
  "data": {
    "stats": {
      "total_count": 100,
      "pending_count": 20,
      "resolved_count": 70,
      "closed_count": 10,
      "bug_count": 50,
      "feature_count": 30,
      "complaint_count": 15,
      "praise_count": 3,
      "other_count": 2,
      "low_priority_count": 20,
      "medium_priority_count": 60,
      "high_priority_count": 15,
      "urgent_priority_count": 5,
      "feedback_types": {
        "bug": "Bug报告",
        "feature": "功能建议",
        "complaint": "投诉",
        "praise": "表扬",
        "other": "其他"
      },
      "statuses": {
        "pending": "待处理",
        "processing": "处理中",
        "resolved": "已解决",
        "closed": "已关闭"
      },
      "priorities": {
        "low": "低",
        "medium": "中",
        "high": "高",
        "urgent": "紧急"
      }
    }
  }
}
```

### 6. 获取我的反馈

**GET** `/api/feedback/my`

获取当前用户的反馈列表。

#### 查询参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `user_id` | string | 用户ID（必填） |
| `page` | integer | 页码（默认1） |
| `per_page` | integer | 每页数量（默认20） |
| `feedback_type` | string | 反馈类型过滤 |
| `status` | string | 状态过滤 |
| `sort_by` | string | 排序字段（默认createdAt） |
| `sort_order` | string | 排序方向（asc/desc，默认desc） |

### 7. 获取公开反馈

**GET** `/api/feedback/public`

获取公开的反馈列表。

#### 查询参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `page` | integer | 页码（默认1） |
| `per_page` | integer | 每页数量（默认20） |
| `feedback_type` | string | 反馈类型过滤 |
| `search` | string | 搜索关键词 |
| `sort_by` | string | 排序字段（默认createdAt） |
| `sort_order` | string | 排序方向（asc/desc，默认desc） |

### 8. 更新反馈

**PUT** `/api/feedback/{feedback_id}`

更新反馈信息。

#### 请求参数

```json
{
  "title": "string",            // 反馈标题
  "content": "string",          // 反馈内容
  "feedback_type": "string",    // 反馈类型
  "contact": "string",          // 联系方式
  "app_version": "string",     // 应用版本
  "os_info": "string",         // 操作系统信息
  "rating": integer,           // 评分（1-5分）
  "is_public": boolean,        // 是否公开
  "device_info": {},           // 设备信息
  "attachments": ["string"],   // 附件列表
  "tags": ["string"],          // 标签列表
  "status": "string",          // 状态（管理员专用）
  "priority": "string",        // 优先级（管理员专用）
  "admin_reply": "string"      // 管理员回复（管理员专用）
}
```

#### 查询参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `current_user_id` | string | 当前用户ID |
| `is_admin` | boolean | 是否为管理员 |

### 9. 更新反馈状态

**PUT** `/api/feedback/{feedback_id}/status`

更新反馈状态（管理员专用）。

#### 请求参数

```json
{
  "status": "string"  // 新状态
}
```

#### 查询参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `current_user_id` | string | 当前用户ID |
| `is_admin` | boolean | 是否为管理员（必填true） |

### 10. 更新反馈优先级

**PUT** `/api/feedback/{feedback_id}/priority`

更新反馈优先级（管理员专用）。

#### 请求参数

```json
{
  "priority": "string"  // 新优先级
}
```

### 11. 管理员回复反馈

**POST** `/api/feedback/{feedback_id}/reply`

管理员回复反馈。

#### 请求参数

```json
{
  "reply": "string"  // 回复内容
}
```

### 12. 添加附件

**POST** `/api/feedback/{feedback_id}/attachments`

为反馈添加附件。

#### 请求参数

```json
{
  "attachment_url": "string"  // 附件URL
}
```

### 13. 移除附件

**DELETE** `/api/feedback/{feedback_id}/attachments`

从反馈中移除附件。

#### 请求参数

```json
{
  "attachment_url": "string"  // 附件URL
}
```

### 14. 删除反馈

**DELETE** `/api/feedback/{feedback_id}`

删除反馈。

#### 查询参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `current_user_id` | string | 当前用户ID |
| `is_admin` | boolean | 是否为管理员 |

### 15. 批量删除反馈

**DELETE** `/api/feedback/batch_delete`

批量删除反馈。

#### 请求参数

```json
{
  "feedback_ids": ["string"]  // 反馈ID列表
}
```

### 16. 软删除反馈

**DELETE** `/api/feedback/{feedback_id}/soft_delete`

软删除反馈（将状态设置为已关闭）。

### 17. 清理旧反馈

**DELETE** `/api/feedback/cleanup`

清理旧反馈（管理员专用）。

#### 请求参数

```json
{
  "days_old": integer,        // 天数（默认365）
  "status_filter": "string"   // 状态过滤（默认closed）
}
```

## 权限说明

### 用户权限

- **创建反馈**: 所有用户都可以创建反馈，支持匿名反馈
- **查看反馈**: 
  - 可以查看自己的反馈
  - 可以查看公开的反馈
  - 管理员可以查看所有反馈
- **编辑反馈**: 只有反馈作者可以编辑，且状态为待处理或处理中
- **删除反馈**: 只有反馈作者或管理员可以删除

### 管理员权限

- **查看所有反馈**: 可以查看所有反馈，包括非公开的
- **更新状态**: 可以更新反馈状态
- **更新优先级**: 可以更新反馈优先级
- **回复反馈**: 可以回复反馈
- **清理反馈**: 可以清理旧反馈

## 错误码

| 错误码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 403 | 权限不足 |
| 404 | 反馈不存在 |
| 500 | 服务器内部错误 |

## 使用示例

### 创建反馈

```bash
curl -X POST http://localhost:8000/api/feedback/create \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "feedback_type": "bug",
    "title": "登录页面显示异常",
    "content": "在登录时页面出现白屏",
    "priority": "high",
    "contact": "user@example.com",
    "device_info": {
      "device": "iPhone 12",
      "os": "iOS 15.0"
    },
    "app_version": "1.0.0",
    "tags": ["登录", "显示"]
  }'
```

### 获取反馈列表

```bash
curl -X GET "http://localhost:8000/api/feedback/list?page=1&per_page=10&feedback_type=bug&status=pending&current_user_id=user123&is_admin=false"
```

### 管理员回复反馈

```bash
curl -X POST http://localhost:8000/api/feedback/abc123def4/reply \
  -H "Content-Type: application/json" \
  -d '{
    "reply": "感谢您的反馈，我们已修复此问题"
  }' \
  -G -d "current_user_id=admin123" -d "is_admin=true"
```

## 注意事项

1. **匿名反馈**: 支持匿名反馈，user_id字段可以为空
2. **权限控制**: 所有操作都需要检查用户权限
3. **数据验证**: 所有输入数据都会进行验证
4. **JSON字段**: device_info、attachments、tags等字段存储为JSON格式
5. **状态管理**: 反馈有完整的状态管理流程
6. **搜索功能**: 支持按标题和内容搜索
7. **分页支持**: 所有列表接口都支持分页
8. **排序功能**: 支持多种排序方式

---

## 🎉 系统总结

意见反馈功能已完全实现，包括：

✅ **完整的数据模型** - 支持所有反馈功能需求  
✅ **丰富的API接口** - 17个API端点覆盖所有操作  
✅ **权限控制系统** - 用户和管理员权限分离  
✅ **数据库迁移** - 自动创建表结构  
✅ **详细文档** - 完整的API使用说明  
✅ **测试脚本** - 验证所有功能正常  

现在用户可以通过API创建、查看、更新反馈，管理员可以处理反馈、回复用户，系统还提供了完整的统计和搜索功能。整个反馈系统已经可以投入生产使用！
