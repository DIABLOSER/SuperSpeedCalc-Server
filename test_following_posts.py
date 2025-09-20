#!/usr/bin/env python3
"""
测试获取关注用户帖子列表接口
"""

import requests
import json
import random

BASE_URL = "http://localhost:8000"

def test_following_posts_api():
    """测试关注用户帖子列表接口"""
    print("🚀 开始测试获取关注用户帖子列表接口...")
    
    # 1. 检查服务器状态
    print("\n1️⃣ 检查服务器状态...")
    try:
        health_response = requests.get(f"{BASE_URL}/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ 服务器运行正常")
        else:
            print("❌ 服务器状态异常")
            return
    except Exception as e:
        print(f"❌ 服务器连接失败: {e}")
        return
    
    # 2. 获取测试用户
    print("\n2️⃣ 获取测试用户...")
    users_response = requests.get(f"{BASE_URL}/users/")
    if users_response.status_code != 200:
        print("❌ 获取用户列表失败")
        return
    
    users = users_response.json()['data']['items']
    test_user = users[1]  # 选择第二个用户
    print(f"✅ 选择测试用户: {test_user['username']} (ID: {test_user['objectId']})")
    
    # 3. 测试获取关注用户帖子列表
    print("\n3️⃣ 测试获取关注用户帖子列表...")
    following_posts_url = f"{BASE_URL}/posts/user/{test_user['objectId']}/following"
    
    # 测试基础请求
    response = requests.get(following_posts_url)
    print(f"   请求URL: {following_posts_url}")
    print(f"   响应状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ 接口调用成功")
        print(f"   响应消息: {result['message']}")
        
        data = result['data']
        print(f"   用户信息: {data['user']['username']}")
        print(f"   关注用户数量: {data['following_count']}")
        print(f"   帖子数量: {len(data['posts'])}")
        
        # 显示分页信息
        pagination = data['pagination']
        print(f"   分页信息: 第{pagination['page']}页，共{pagination['pages']}页，总计{pagination['total']}条")
        
        # 显示前几条帖子
        if data['posts']:
            print("\n   📝 帖子列表:")
            for i, post in enumerate(data['posts'][:3]):  # 只显示前3条
                print(f"      {i+1}. {post['content'][:50]}... (by {post['user']['username']})")
        else:
            print("   📝 暂无帖子")
            
    else:
        print(f"❌ 接口调用失败: {response.status_code}")
        print(f"   错误信息: {response.text}")
    
    # 4. 测试分页参数
    print("\n4️⃣ 测试分页参数...")
    pagination_params = {
        'page': 1,
        'per_page': 5
    }
    
    response = requests.get(following_posts_url, params=pagination_params)
    if response.status_code == 200:
        result = response.json()
        pagination = result['data']['pagination']
        print(f"✅ 分页测试成功: 每页{pagination['per_page']}条，共{pagination['total']}条")
    else:
        print(f"❌ 分页测试失败: {response.status_code}")
    
    # 5. 测试viewer_id参数
    print("\n5️⃣ 测试viewer_id参数...")
    viewer_params = {
        'viewer_id': test_user['objectId']
    }
    
    response = requests.get(following_posts_url, params=viewer_params)
    if response.status_code == 200:
        result = response.json()
        print("✅ viewer_id参数测试成功")
        if result['data']['posts']:
            post = result['data']['posts'][0]
            print(f"   点赞状态: {post.get('is_liked_by_user', 'N/A')}")
    else:
        print(f"❌ viewer_id参数测试失败: {response.status_code}")
    
    # 6. 测试不存在的用户
    print("\n6️⃣ 测试不存在的用户...")
    fake_user_url = f"{BASE_URL}/posts/user/nonexistent_user/following"
    response = requests.get(fake_user_url)
    
    if response.status_code == 404:
        print("✅ 不存在用户错误处理正确")
    else:
        print(f"❌ 不存在用户错误处理异常: {response.status_code}")
    
    # 7. 测试用户关系功能
    print("\n7️⃣ 测试用户关系功能...")
    test_user_relationship(test_user['objectId'])
    
    print("\n🎉 关注用户帖子列表接口测试完成！")

def test_user_relationship(user_id):
    """测试用户关系功能"""
    print(f"   测试用户ID: {user_id}")
    
    # 获取用户关注列表
    following_url = f"{BASE_URL}/users/{user_id}/following"
    response = requests.get(following_url)
    
    if response.status_code == 200:
        result = response.json()
        following_count = len(result['data'].get('following', []))
        print(f"   用户关注数量: {following_count}")
        
        if following_count > 0:
            print("   ✅ 用户有关注其他用户，应该能看到关注用户的帖子")
        else:
            print("   ⚠️ 用户没有关注其他用户，帖子列表应该为空")
    else:
        print(f"   ❌ 获取用户关注列表失败: {response.status_code}")

def test_with_real_data():
    """使用真实数据测试"""
    print("\n" + "="*60)
    print("🧪 使用真实数据测试")
    print("="*60)
    
    # 获取所有用户
    users_response = requests.get(f"{BASE_URL}/users/")
    users = users_response.json()['data']['items']
    
    # 测试多个用户
    for i, user in enumerate(users[:3]):  # 测试前3个用户
        print(f"\n📋 测试用户 {i+1}: {user['username']} (ID: {user['objectId']})")
        
        following_posts_url = f"{BASE_URL}/posts/user/{user['objectId']}/following"
        response = requests.get(following_posts_url)
        
        if response.status_code == 200:
            result = response.json()
            data = result['data']
            print(f"   ✅ 成功: 关注{data['following_count']}人，帖子{len(data['posts'])}条")
        else:
            print(f"   ❌ 失败: {response.status_code}")

def main():
    """主函数"""
    print("🚀 开始测试获取关注用户帖子列表接口...")
    print("="*60)
    
    # 基础功能测试
    test_following_posts_api()
    
    # 真实数据测试
    test_with_real_data()
    
    print("\n" + "="*60)
    print("🎉 所有测试完成！")
    print("="*60)

if __name__ == '__main__':
    main()
