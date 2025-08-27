# History排行榜API使用示例

## 概述

History排行榜API提供了基于用户历史记录中`scope`字段的得分排行榜功能，支持日榜、月榜、年榜和总榜。

## API端点

### 1. 获取排行榜

**端点**: `GET /api/history/leaderboard`

**参数**:
- `period` (可选): 时间段筛选
  - `all`: 总榜（默认）
  - `daily`: 日榜（今日数据）
  - `monthly`: 月榜（本月数据）
  - `yearly`: 年榜（今年数据）
- `page` (可选): 页码，默认1
- `per_page` (可选): 每页数量，默认10

**示例请求**:
```bash
# 获取总排行榜
curl "http://localhost:5003/api/history/leaderboard?period=all&page=1&per_page=10"

# 获取日榜
curl "http://localhost:5003/api/history/leaderboard?period=daily"

# 获取月榜
curl "http://localhost:5003/api/history/leaderboard?period=monthly"

# 获取年榜
curl "http://localhost:5003/api/history/leaderboard?period=yearly"
```

**响应示例**:
```json
{
  "message": "获取all排行榜成功",
  "data": [
    {
      "rank": 1,
      "user": {
        "objectId": "abc123",
        "username": "张三",
        "avatar": "/uploads/avatar1.jpg"
      },
      "total_score": 450,
      "history_count": 3
    },
    {
      "rank": 2,
      "user": {
        "objectId": "def456",
        "username": "李四",
        "avatar": "/uploads/avatar2.jpg"
      },
      "total_score": 190,
      "history_count": 2
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 2,
    "pages": 1,
    "has_next": false,
    "has_prev": false
  },
  "period": "all"
}
```

### 2. 获取用户统计

**端点**: `GET /api/history/stats`

**参数**:
- `user_id` (必需): 用户ID

**示例请求**:
```bash
curl "http://localhost:5003/api/history/stats?user_id=abc123"
```

**响应示例**:
```json
{
  "message": "获取用户score统计成功",
  "data": {
    "user": {
      "objectId": "abc123",
      "username": "张三",
      "avatar": "/uploads/avatar1.jpg"
    },
    "stats": {
      "today": {
        "total_score": 450,
        "count": 3
      },
      "month": {
        "total_score": 450,
        "count": 3
      },
      "year": {
        "total_score": 450,
        "count": 3
      },
      "total": {
        "total_score": 450,
        "count": 3
      }
    }
  }
}
```

## 使用场景

### 1. 游戏排行榜
```javascript
// 获取今日游戏排行榜
fetch('/api/history/leaderboard?period=daily')
  .then(response => response.json())
  .then(data => {
    console.log('今日排行榜:', data.data);
  });
```

### 2. 用户个人统计
```javascript
// 获取用户个人统计
fetch(`/api/history/stats?user_id=${userId}`)
  .then(response => response.json())
  .then(data => {
    const stats = data.data.stats;
    console.log('今日得分:', stats.today.total_score);
    console.log('本月得分:', stats.month.total_score);
  });
```

### 3. 排行榜展示
```javascript
// 展示不同时间段的排行榜
const periods = ['daily', 'monthly', 'yearly', 'all'];
const periodNames = ['日榜', '月榜', '年榜', '总榜'];

periods.forEach((period, index) => {
  fetch(`/api/history/leaderboard?period=${period}`)
    .then(response => response.json())
    .then(data => {
      console.log(`${periodNames[index]}:`, data.data);
    });
});
```

## 注意事项

1. **时间计算**: 排行榜基于UTC时间计算
   - 日榜: 当天00:00:00开始
   - 月榜: 当月1号00:00:00开始
   - 年榜: 当年1月1日00:00:00开始

2. **分数计算**: 排行榜按`scope`字段的总和进行排序，支持正负数

3. **分页**: 支持分页查询，建议每页不超过100条记录

4. **性能**: 对于大量数据的排行榜查询，建议添加适当的缓存机制

## 错误处理

```javascript
fetch('/api/history/leaderboard?period=daily')
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    console.log('排行榜数据:', data);
  })
  .catch(error => {
    console.error('获取排行榜失败:', error);
  });
```
