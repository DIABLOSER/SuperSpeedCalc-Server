#!/usr/bin/env python3
"""
API 测试脚本
运行此脚本可以测试所有 API 端点
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_health():
    """测试健康检查"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print("❌ Health check failed")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the server is running.")
        return False

def test_user_apis():
    """测试用户相关 API"""
    print("\n👤 Testing User APIs...")
    
    # 创建用户
    user_data = {
        "username": "testuser001",
        "email": "test001@example.com",
        "password": "password123",
        "avatar": "https://example.com/avatar.jpg",
        "bio": "这是一个测试用户",
        "score": 100,
        "experence": 50,
        "boluo": 10
    }
    
    print("  Creating user...")
    response = requests.post(f"{BASE_URL}/api/users", json=user_data)
    if response.status_code == 201:
        print("  ✅ User created successfully")
        user = response.json()['data']
        user_id = user['objectId']
        print(f"     User ID: {user_id}")
        print(f"     Score: {user.get('score', 0)}")
        print(f"     Experience: {user.get('experence', 0)}")
        print(f"     Boluo: {user.get('boluo', 0)}")
        
        # 获取用户
        print("  Getting user...")
        response = requests.get(f"{BASE_URL}/api/users/{user_id}")
        if response.status_code == 200:
            print("  ✅ User retrieved successfully")
        
        # 用户登录
        print("  Testing login...")
        login_data = {"username": "testuser001", "password": "password123"}
        response = requests.post(f"{BASE_URL}/api/users/login", json=login_data)
        if response.status_code == 200:
            print("  ✅ Login successful")
        
        # 更新用户
        print("  Updating user...")
        update_data = {
            "avatar": "https://example.com/new-avatar.jpg",
            "score": 200
        }
        response = requests.put(f"{BASE_URL}/api/users/{user_id}", json=update_data)
        if response.status_code == 200:
            print("  ✅ User updated successfully")
        
        # 测试积分更新
        print("  Testing score update...")
        score_data = {"score_change": 50}
        response = requests.post(f"{BASE_URL}/api/users/{user_id}/score", json=score_data)
        if response.status_code == 200:
            print("  ✅ Score updated successfully")
            user_updated = response.json()['data']
            print(f"     New Score: {user_updated.get('score', 0)}")
        
        # 测试经验值更新
        print("  Testing experience update...")
        exp_data = {"exp_change": 25}
        response = requests.post(f"{BASE_URL}/api/users/{user_id}/experence", json=exp_data)
        if response.status_code == 200:
            print("  ✅ Experience updated successfully")
            user_updated = response.json()['data']
            print(f"     New Experience: {user_updated.get('experence', 0)}")
        
        # 测试菠萝币更新
        print("  Testing boluo update...")
        boluo_data = {"boluo_change": 5}
        response = requests.post(f"{BASE_URL}/api/users/{user_id}/boluo", json=boluo_data)
        if response.status_code == 200:
            print("  ✅ Boluo updated successfully")
            user_updated = response.json()['data']
            print(f"     New Boluo: {user_updated.get('boluo', 0)}")
        
        return user_id
    else:
        print(f"  ❌ Failed to create user: {response.text}")
        return None

def test_charts_apis(user_id):
    """测试图表相关 API"""
    print("\n📊 Testing Charts APIs...")
    
    if not user_id:
        print("  ❌ No user ID available for testing charts")
        return None
    
    # 创建图表
    chart_data = {
        "title": "测试排行榜记录",
        "achievement": 100.5,
        "user": user_id
    }
    
    print("  Creating chart...")
    response = requests.post(f"{BASE_URL}/api/charts", json=chart_data)
    if response.status_code == 201:
        print("  ✅ Chart created successfully")
        chart = response.json()['data']
        chart_id = chart['objectId']
        print(f"     Chart ID: {chart_id}")
        print(f"     Achievement: {chart.get('achievement', 0)}")
        
        # 获取图表
        print("  Getting chart...")
        response = requests.get(f"{BASE_URL}/api/charts/{chart_id}")
        if response.status_code == 200:
            print("  ✅ Chart retrieved successfully")
        
        # 获取排行榜
        print("  Getting leaderboard...")
        response = requests.get(f"{BASE_URL}/api/charts/leaderboard")
        if response.status_code == 200:
            print("  ✅ Leaderboard retrieved successfully")
        
        # 更新图表
        print("  Updating chart...")
        update_data = {"title": "更新后的排行榜记录", "achievement": 150.0}
        response = requests.put(f"{BASE_URL}/api/charts/{chart_id}", json=update_data)
        if response.status_code == 200:
            print("  ✅ Chart updated successfully")
        
        # 测试成绩值更新
        print("  Testing achievement update...")
        achievement_data = {"achievement_change": 25.5}
        response = requests.post(f"{BASE_URL}/api/charts/{chart_id}/achievement", json=achievement_data)
        if response.status_code == 200:
            print("  ✅ Achievement updated successfully")
            chart_updated = response.json()['data']
            print(f"     New Achievement: {chart_updated.get('achievement', 0)}")
        
        return chart_id
    else:
        print(f"  ❌ Failed to create chart: {response.text}")
        return None

def test_forum_apis(user_id):
    """测试论坛相关 API"""
    print("\n💬 Testing Forum APIs...")
    
    if not user_id:
        print("  ❌ No user ID available for testing forum")
        return None
    
    # 创建论坛帖子
    post_data = {
        "content": "这是第一个测试帖子，欢迎大家积极讨论！",
        "category": "公告",
        "tags": ["欢迎", "公告", "测试"],
        "public": True,
        "images": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
        "user": user_id
    }
    
    print("  Creating forum post...")
    response = requests.post(f"{BASE_URL}/api/forum", json=post_data)
    if response.status_code == 201:
        print("  ✅ Forum post created successfully")
        post = response.json()['data']
        post_id = post['objectId']
        print(f"     Post ID: {post_id}")
        print(f"     Public: {post.get('public', False)}")
        print(f"     Images count: {len(post.get('images', []))}")
        
        # 获取帖子
        print("  Getting forum post...")
        response = requests.get(f"{BASE_URL}/api/forum/{post_id}")
        if response.status_code == 200:
            print("  ✅ Forum post retrieved successfully")
        
        # 给帖子点赞
        print("  Liking forum post...")
        response = requests.post(f"{BASE_URL}/api/forum/{post_id}/like")
        if response.status_code == 200:
            print("  ✅ Forum post liked successfully")
        
        # 获取所有帖子
        print("  Getting all forum posts...")
        response = requests.get(f"{BASE_URL}/api/forum")
        if response.status_code == 200:
            print("  ✅ All forum posts retrieved successfully")
        
        # 获取公开帖子
        print("  Getting public posts...")
        response = requests.get(f"{BASE_URL}/api/forum/public")
        if response.status_code == 200:
            print("  ✅ Public posts retrieved successfully")
        
        # 更新帖子
        print("  Updating forum post...")
        update_data = {
            "content": "更新后的帖子内容",
            "public": False,
            "images": ["https://example.com/new-image.jpg"]
        }
        response = requests.put(f"{BASE_URL}/api/forum/{post_id}", json=update_data)
        if response.status_code == 200:
            print("  ✅ Forum post updated successfully")
        
        return post_id
    else:
        print(f"  ❌ Failed to create forum post: {response.text}")
        return None

def test_image_apis(user_id):
    """测试图片相关 API"""
    print("\n🖼️ Testing Image APIs...")
    
    # 创建图片记录（JSON方式）
    image_data = {
        "fileName": "test_image.jpg",
        "path": "/uploads/images/test_image.jpg",
        "url": "https://example.com/images/test_image.jpg",
        "fileSize": 256000
    }
    
    print("  Creating image record...")
    response = requests.post(f"{BASE_URL}/api/images", json=image_data)
    if response.status_code == 201:
        print("  ✅ Image record created successfully")
        image = response.json()['data']
        image_id = image['objectId']
        print(f"     Image ID: {image_id}")
        print(f"     File Name: {image.get('fileName', '')}")
        print(f"     File Size: {image.get('fileSize', 0)} bytes")
        
        # 获取图片
        print("  Getting image...")
        response = requests.get(f"{BASE_URL}/api/images/{image_id}")
        if response.status_code == 200:
            print("  ✅ Image retrieved successfully")
        
        # 获取所有图片
        print("  Getting all images...")
        response = requests.get(f"{BASE_URL}/api/images")
        if response.status_code == 200:
            print("  ✅ All images retrieved successfully")
        
        # 获取图片统计
        print("  Getting image stats...")
        response = requests.get(f"{BASE_URL}/api/images/stats")
        if response.status_code == 200:
            print("  ✅ Image stats retrieved successfully")
            stats = response.json()['data']
            print(f"     Total images: {stats.get('total_images', 0)}")
            print(f"     Total size: {stats.get('total_size_mb', 0)} MB")
        
        # 搜索图片
        print("  Searching images...")
        response = requests.get(f"{BASE_URL}/api/images/search?q=test")
        if response.status_code == 200:
            print("  ✅ Image search successful")
        
        # 更新图片
        print("  Updating image...")
        update_data = {
            "fileName": "updated_test_image.jpg",
            "fileSize": 512000
        }
        response = requests.put(f"{BASE_URL}/api/images/{image_id}", json=update_data)
        if response.status_code == 200:
            print("  ✅ Image updated successfully")
        
        # 更新图片URL
        print("  Updating image URL...")
        url_data = {"url": "https://example.com/images/updated_test_image.jpg"}
        response = requests.post(f"{BASE_URL}/api/images/{image_id}/url", json=url_data)
        if response.status_code == 200:
            print("  ✅ Image URL updated successfully")
        
        # 创建第二个图片用于批量删除测试
        image_data2 = {
            "fileName": "test_image2.jpg",
            "path": "/uploads/images/test_image2.jpg",
            "url": "https://example.com/images/test_image2.jpg",
            "fileSize": 128000
        }
        response2 = requests.post(f"{BASE_URL}/api/images", json=image_data2)
        if response2.status_code == 201:
            image2_id = response2.json()['data']['objectId']
            
            # 测试批量删除
            print("  Testing batch delete...")
            batch_data = {"image_ids": [image_id, image2_id]}
            response = requests.post(f"{BASE_URL}/api/images/batch/delete", json=batch_data)
            if response.status_code == 200:
                print("  ✅ Batch delete successful")
                return None  # 图片已被删除
        
        return image_id
    else:
        print(f"  ❌ Failed to create image record: {response.text}")
        return None

def test_image_upload():
    """测试图片上传功能（需要实际文件）"""
    print("\n📤 Testing Image Upload (simulated)...")
    
    # 注意：这里只是模拟测试，实际使用时需要真实文件
    print("  ⚠️ File upload tests require actual files - skipping simulation")
    print("  📝 To test file upload manually:")
    print(f"     Single upload: curl -X POST -F 'file=@image.jpg' {BASE_URL}/api/images/upload")
    print(f"     Multiple upload: curl -X POST -F 'files=@image1.jpg' -F 'files=@image2.jpg' {BASE_URL}/api/images/upload/multiple")
    
    return True

def main():
    """运行所有测试"""
    print("🚀 Starting API Tests for SuperSpeedCalc Server")
    print("=" * 50)
    
    # 测试健康检查
    if not test_health():
        print("\n❌ Server is not running. Please start the server first:")
        print("   python app.py")
        return
    
    # 测试用户 API
    user_id = test_user_apis()
    
    # 测试图表 API
    chart_id = test_charts_apis(user_id)
    
    # 测试论坛 API
    post_id = test_forum_apis(user_id)
    
    # 测试图片 API
    image_id = test_image_apis(user_id)
    
    # 测试图片上传功能
    test_image_upload()
    
    print("\n" + "=" * 50)
    print("🎉 API Tests Completed!")
    
    if user_id:
        print(f"📝 Test Data Created:")
        print(f"   User ID: {user_id}")
        if chart_id:
            print(f"   Chart ID: {chart_id}")
        if post_id:
            print(f"   Forum Post ID: {post_id}")
        if image_id:
            print(f"   Image ID: {image_id}")
        
        print(f"\n🌐 You can now test the APIs manually:")
        print(f"   Users: {BASE_URL}/api/users")
        print(f"   Charts: {BASE_URL}/api/charts")
        print(f"   Forum: {BASE_URL}/api/forum")
        print(f"   Images: {BASE_URL}/api/images")

if __name__ == "__main__":
    main() 