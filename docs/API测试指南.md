# API 测试指南

## 📋 概述

本指南提供了完整的API测试方法和工具，帮助开发者快速验证接口功能。

## 🚀 快速开始

### 环境准备
```bash
# 1. 启动服务器
python start_development.py  # 开发环境 (端口 8000)

# 2. 验证服务器状态
curl http://localhost:8000/health
```

### 测试工具
- **curl**: 命令行HTTP客户端
- **Python requests**: 自动化测试脚本
- **Postman**: 图形化API测试工具

## 🧪 测试脚本

### 1. 基础功能测试脚本

#### 简单测试脚本 (`simple_test.py`)
```python
#!/usr/bin/env python3
"""
简化的点赞和评论接口测试
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_like_and_reply():
    """测试点赞和评论功能"""
    print("🚀 开始测试点赞和评论接口...")
    
    # 1. 获取测试数据
    users_response = requests.get(f"{BASE_URL}/users/")
    users = users_response.json()['data']['items']
    test_user = users[1]
    
    posts_response = requests.get(f"{BASE_URL}/posts/")
    posts = posts_response.json()['data']['items']
    test_post = posts[0]
    
    # 2. 测试点赞
    like_data = {'user_id': test_user['objectId']}
    like_response = requests.post(f"{BASE_URL}/posts/{test_post['objectId']}/like", 
                                 json=like_data, 
                                 headers={'Content-Type': 'application/json'})
    
    if like_response.status_code == 200:
        print("✅ 点赞成功")
    else:
        print(f"❌ 点赞失败: {like_response.status_code}")
    
    # 3. 测试评论
    reply_data = {
        'post': test_post['objectId'],
        'user': test_user['objectId'],
        'content': '这是一个测试评论'
    }
    
    reply_response = requests.post(f"{BASE_URL}/replies/", 
                                  json=reply_data, 
                                  headers={'Content-Type': 'application/json'})
    
    if reply_response.status_code == 201:
        print("✅ 创建评论成功")
    else:
        print(f"❌ 创建评论失败: {reply_response.status_code}")

if __name__ == '__main__':
    test_like_and_reply()
```

#### 全面测试脚本 (`comprehensive_test.py`)
```python
#!/usr/bin/env python3
"""
全面的评论和点赞接口测试
"""

import requests
import json
import random

BASE_URL = "http://localhost:8000"

def test_all_functions():
    """测试所有功能"""
    print("🚀 开始全面测试...")
    
    # 测试点赞功能
    test_like_operations()
    
    # 测试评论功能
    test_reply_operations()
    
    # 测试错误情况
    test_error_cases()

def test_like_operations():
    """测试点赞相关操作"""
    print("\n🧪 测试点赞相关操作")
    
    # 获取测试数据
    users, posts = get_test_data()
    test_post = random.choice(posts)
    test_users = random.sample(users, min(3, len(users)))
    
    # 测试点赞
    for user in test_users:
        like_data = {'user_id': user['objectId']}
        response = requests.post(f"{BASE_URL}/posts/{test_post['objectId']}/like", 
                                json=like_data, 
                                headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            print(f"✅ 用户 {user['username']} 点赞成功")
        else:
            print(f"❌ 用户 {user['username']} 点赞失败")
    
    # 测试取消点赞
    for user in test_users[:2]:
        unlike_data = {'user_id': user['objectId']}
        response = requests.delete(f"{BASE_URL}/posts/{test_post['objectId']}/like", 
                                  json=unlike_data, 
                                  headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            print(f"✅ 用户 {user['username']} 取消点赞成功")
        else:
            print(f"❌ 用户 {user['username']} 取消点赞失败")

def test_reply_operations():
    """测试评论相关操作"""
    print("\n🧪 测试评论相关操作")
    
    # 获取测试数据
    users, posts = get_test_data()
    test_post = random.choice(posts)
    test_users = random.sample(users, min(3, len(users)))
    
    # 测试创建评论
    for user in test_users:
        reply_data = {
            'post': test_post['objectId'],
            'user': user['objectId'],
            'content': f'这是用户 {user["username"]} 的评论'
        }
        
        response = requests.post(f"{BASE_URL}/replies/", 
                                json=reply_data, 
                                headers={'Content-Type': 'application/json'})
        
        if response.status_code == 201:
            print(f"✅ 用户 {user['username']} 创建评论成功")
        else:
            print(f"❌ 用户 {user['username']} 创建评论失败")

def test_error_cases():
    """测试错误情况"""
    print("\n🧪 测试错误情况")
    
    # 测试不存在的资源
    fake_post_id = "nonexistent_post_123"
    fake_user_id = "nonexistent_user_123"
    
    # 点赞不存在的帖子
    like_data = {'user_id': fake_user_id}
    response = requests.post(f"{BASE_URL}/posts/{fake_post_id}/like", 
                            json=like_data, 
                            headers={'Content-Type': 'application/json'})
    
    if response.status_code == 404:
        print("✅ 不存在帖子点赞错误处理正确")
    else:
        print(f"❌ 不存在帖子点赞错误处理异常: {response.status_code}")

def get_test_data():
    """获取测试数据"""
    users_response = requests.get(f"{BASE_URL}/users/")
    users = users_response.json()['data']['items']
    
    posts_response = requests.get(f"{BASE_URL}/posts/")
    posts = posts_response.json()['data']['items']
    
    return users, posts

if __name__ == '__main__':
    test_all_functions()
```

## 🔧 手动测试命令

### 基础功能测试
```bash
# 1. 健康检查
curl http://localhost:8000/health

# 2. 获取用户列表
curl "http://localhost:8000/users/?page=1&per_page=5"

# 3. 获取帖子列表
curl "http://localhost:8000/posts/?page=1&per_page=5"
```

### 社交功能测试
```bash
# 1. 点赞帖子 (需要替换实际的post_id和user_id)
curl -X POST "http://localhost:8000/posts/{post_id}/like" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123"}'

# 2. 取消点赞
curl -X DELETE "http://localhost:8000/posts/{post_id}/like" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123"}'

# 3. 获取帖子点赞用户
curl "http://localhost:8000/posts/{post_id}/likers"

# 4. 创建评论
curl -X POST "http://localhost:8000/replies/" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "这是一条测试评论",
    "post": "post123",
    "user": "user123"
  }'

# 5. 获取帖子评论
curl "http://localhost:8000/replies/post/{post_id}"

# 6. 获取一级评论
curl "http://localhost:8000/replies/post/{post_id}/first-level"
```

### 错误情况测试
```bash
# 1. 测试不存在的资源
curl -X POST "http://localhost:8000/posts/nonexistent/like" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "nonexistent"}'

# 2. 测试重复点赞
curl -X POST "http://localhost:8000/posts/{post_id}/like" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123"}'
# 再次执行相同命令，应该返回400错误

# 3. 测试取消未点赞的帖子
curl -X DELETE "http://localhost:8000/posts/{post_id}/like" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123"}'
# 如果用户未点赞过，应该返回400错误
```

## 📊 测试结果验证

### 成功响应格式
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "key": "value"
  }
}
```

### 错误响应格式
```json
{
  "code": 400,
  "message": "错误描述"
}
```

### 分页响应格式
```json
{
  "code": 200,
  "message": "获取数据成功",
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 100,
      "pages": 5
    }
  }
}
```

## 🎯 测试重点

### 1. 点赞功能测试重点
- ✅ 正常点赞流程
- ✅ 重复点赞错误处理
- ✅ 取消点赞流程
- ✅ 取消未点赞错误处理
- ✅ 点赞数量同步
- ✅ 点赞用户列表获取

### 2. 评论功能测试重点
- ✅ 一级评论创建
- ✅ 二级评论（回复）创建
- ✅ 评论列表获取
- ✅ 一级评论列表获取
- ✅ 用户评论列表获取
- ✅ 评论树形结构正确性

### 3. 错误处理测试重点
- ✅ 不存在资源处理
- ✅ 参数验证
- ✅ 权限控制
- ✅ 数据一致性

## 📈 性能测试

### 响应时间要求
- 点赞操作: < 100ms
- 评论操作: < 150ms
- 查询操作: < 200ms

### 并发测试
```python
import concurrent.futures
import requests
import time

def test_concurrent_likes():
    """测试并发点赞"""
    def like_post(post_id, user_id):
        response = requests.post(f"{BASE_URL}/posts/{post_id}/like", 
                                json={'user_id': user_id}, 
                                headers={'Content-Type': 'application/json'})
        return response.status_code
    
    # 并发执行10个点赞请求
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(like_post, "post123", f"user{i}") 
                  for i in range(10)]
        
        results = [future.result() for future in futures]
        print(f"并发测试结果: {results}")

if __name__ == '__main__':
    test_concurrent_likes()
```

## 🔍 调试技巧

### 1. 查看详细响应
```bash
# 使用 -v 参数查看详细请求信息
curl -v "http://localhost:8000/users/"

# 使用 -i 参数查看响应头
curl -i "http://localhost:8000/users/"
```

### 2. 保存响应到文件
```bash
# 保存响应到文件
curl "http://localhost:8000/users/" > response.json

# 格式化JSON输出
curl "http://localhost:8000/users/" | python -m json.tool
```

### 3. 测试特定状态码
```bash
# 只显示HTTP状态码
curl -o /dev/null -s -w "%{http_code}\n" "http://localhost:8000/users/"
```

## 📝 测试报告模板

### 测试执行记录
```
测试时间: 2025-09-19
测试环境: 开发环境 (localhost:8000)
测试人员: [姓名]

功能测试结果:
- 点赞功能: ✅ 通过
- 评论功能: ✅ 通过
- 错误处理: ✅ 通过

性能测试结果:
- 平均响应时间: 120ms
- 并发处理能力: 正常

发现问题:
- 无

建议改进:
- 无
```

## 🚨 常见问题

### 1. 连接被拒绝
```bash
# 检查服务器是否启动
curl http://localhost:8000/health

# 如果失败，启动服务器
python start_development.py
```

### 2. 404错误
- 检查URL路径是否正确
- 确认资源ID是否存在
- 验证请求方法是否正确

### 3. 400错误
- 检查请求参数格式
- 验证必填字段是否提供
- 确认参数类型是否正确

### 4. 500错误
- 查看服务器日志
- 检查数据库连接
- 验证数据完整性

---

**注意**: 测试前请确保服务器已启动，并且有足够的测试数据。
