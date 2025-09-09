# API 接口文档

本目录包含 SuperSpeedCalc Server 的详细API接口文档。

## 📋 文档列表

| 模块 | 文档文件 | 说明 |
|------|----------|------|
| 用户管理 | [user_api.md](./user_api.md) | 用户注册、登录、信息管理 |
| 排行榜 | [charts_api.md](./charts_api.md) | 用户成绩记录、排名统计 |
| 论坛 | [forum_api.md](./forum_api.md) | 论坛帖子发布、管理 |
| 图片管理 | [image_api.md](./image_api.md) | 图片上传、管理 |
| 历史记录 | [history_api.md](./history_api.md) | 用户操作历史记录 |
| 应用发布 | [releases_api.md](./releases_api.md) | APK版本管理、更新控制 |
| 用户关系 | [relationship_api.md](./relationship_api.md) | 关注/粉丝关系管理 |
| 帖子管理 | [posts_api.md](./posts_api.md) | 用户帖子发布、管理 |
| 点赞功能 | [likes_api.md](./likes_api.md) | 帖子点赞功能 |
| 回复功能 | [replies_api.md](./replies_api.md) | 评论回复功能 |
| 横幅管理 | [banners_api.md](./banners_api.md) | 轮播图、广告管理 |
| 短信服务 | [sms_api.md](./sms_api.md) | 短信验证码发送、验证 |

## 🔧 统一响应格式

所有API接口都使用统一的响应格式：

### 成功响应
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "key": "value"
  }
}
```

### 分页响应
```json
{
  "code": 200,
  "message": "获取数据成功",
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total": 100,
      "pages": 10
    }
  }
}
```

### 错误响应
```json
{
  "code": 400,
  "message": "错误描述"
}
```

## 📝 使用说明

1. **基础URL**: `http://localhost:5000/api`
2. **请求方式**: 支持 GET、POST、PUT、DELETE
3. **数据格式**: JSON
4. **认证方式**: 部分接口需要用户认证

## 🔍 快速查找

- 需要用户认证的接口会在文档中标注 `🔒 需要认证`
- 分页接口会标注 `📄 支持分页`
- 文件上传接口会标注 `📁 文件上传`

## 📞 技术支持

如有问题，请查看具体的API文档文件或联系开发团队。
