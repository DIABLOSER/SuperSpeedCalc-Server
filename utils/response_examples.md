# API响应格式使用示例

## 统一响应格式

所有API接口都使用统一的响应格式，确保前端处理的一致性。采用智能的 `code`、`message`、`data` 格式：

- **基础只有三个字段**：`code`、`message`、`data`
- **成功时**：`data` 包含所有返回数据（JSON字符串格式）
- **错误时**：`data` 为 `null`
- **其他信息**（如分页、元数据等）都包含在 `data` 中

### 成功响应格式

```json
{
  "code": 200,
  "message": "操作成功",
  "data": "{\"id\": 1, \"username\": \"用户1\", \"email\": \"user@example.com\"}"
}
```

### 错误响应格式

```json
{
  "code": 400,
  "message": "请求参数错误",
  "data": null
}
```

### 分页响应格式

```json
{
  "code": 200,
  "message": "获取成功",
  "data": "{\"list\": [{\"id\": 1, \"name\": \"用户1\"}, {\"id\": 2, \"name\": \"用户2\"}], \"pagination\": {\"page\": 1, \"per_page\": 20, \"total\": 100, \"pages\": 5, \"has_next\": true, \"has_prev\": false}}"
}
```

## 使用示例

### 1. 基本成功响应

```python
from utils.response import success_response

# 返回数据
return success_response(data=user.to_dict(), message="用户信息获取成功")

# 只返回消息
return success_response(message="操作完成")
```

### 2. 创建成功响应

```python
from utils.response import created_response

return created_response(data=new_user.to_dict(), message="用户创建成功")
```

### 3. 更新成功响应

```python
from utils.response import updated_response

return updated_response(data=user.to_dict(), message="用户信息更新成功")
```

### 4. 删除成功响应

```python
from utils.response import deleted_response

return deleted_response(message="用户删除成功")
```

### 5. 分页响应

```python
from utils.response import paginated_response

return paginated_response(
    data=[item.to_dict() for item in items],
    page=1,
    per_page=20,
    total=100,
    message="数据获取成功"
)
```

### 6. 错误响应

```python
from utils.response import bad_request_response, not_found_response, internal_error_response

# 参数错误
return bad_request_response(message="用户名不能为空")

# 资源不存在
return not_found_response(message="用户不存在")

# 服务器错误
return internal_error_response(message="数据库连接失败")
```

### 7. 认证相关响应

```python
from utils.response import unauthorized_response, forbidden_response

# 未授权
return unauthorized_response(message="请先登录")

# 禁止访问
return forbidden_response(message="权限不足")
```

## 常用HTTP状态码

- `200` - 成功
- `201` - 创建成功
- `400` - 请求参数错误
- `401` - 未授权
- `403` - 禁止访问
- `404` - 资源不存在
- `500` - 服务器内部错误

## 响应格式特点

### 优势
1. **极简设计**：只有 `code`、`message`、`data` 三个字段
2. **智能处理**：成功时 `data` 有值（JSON字符串），错误时 `data` 为 `null`
3. **统一标准**：所有接口都使用相同的格式
4. **易于处理**：前端可以统一处理响应格式
5. **灵活扩展**：所有额外信息都包含在 `data` 中
6. **字符串格式**：`data` 字段为JSON字符串，便于某些特殊场景处理

### 使用建议
1. **成功响应**：`code` 为 2xx，`data` 包含返回的数据（JSON字符串）
2. **错误响应**：`code` 为 4xx 或 5xx，`data` 固定为 `null`
3. **分页数据**：`data` 包含 `list` 和 `pagination` 两个字段（JSON字符串）
4. **消息本地化**：`message` 字段支持中英文，便于国际化
5. **前端处理**：只需判断 `code` 是否为 2xx 即可判断成功或失败
6. **数据解析**：前端需要将 `data` 字符串解析为JSON对象使用
