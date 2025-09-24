#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
点赞API测试脚本
"""

import requests
import json
from datetime import datetime

# 服务器地址
BASE_URL = "http://192.168.40.26:8000"

# 测试数据
TEST_POST_ID = "turq0o5jtt"
TEST_USER_ID = "rgng24sqyi"

def test_like_status():
    """测试点赞状态查询"""
    print("=" * 50)
    print("测试点赞状态查询")
    print("=" * 50)
    
    url = f"{BASE_URL}/likes/status/{TEST_USER_ID}/{TEST_POST_ID}"
    print(f"请求URL: {url}")
    
    try:
        response = requests.get(url)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应体: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"解析后的数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        return response
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def test_like_toggle():
    """测试点赞切换"""
    print("=" * 50)
    print("测试点赞切换")
    print("=" * 50)
    
    url = f"{BASE_URL}/likes/toggle"
    data = {
        "post_id": TEST_POST_ID,
        "user_id": TEST_USER_ID
    }
    
    print(f"请求URL: {url}")
    print(f"请求数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应体: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"解析后的数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        return response
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def test_post_likers():
    """测试帖子点赞用户列表"""
    print("=" * 50)
    print("测试帖子点赞用户列表")
    print("=" * 50)
    
    url = f"{BASE_URL}/likes/post/{TEST_POST_ID}/likers"
    params = {
        "page": 1,
        "per_page": 20
    }
    
    print(f"请求URL: {url}")
    print(f"查询参数: {params}")
    
    try:
        response = requests.get(url, params=params)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应体: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"解析后的数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        return response
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def test_user_liked_posts():
    """测试用户点赞的帖子列表"""
    print("=" * 50)
    print("测试用户点赞的帖子列表")
    print("=" * 50)
    
    url = f"{BASE_URL}/likes/user/{TEST_USER_ID}/liked"
    params = {
        "page": 1,
        "per_page": 20
    }
    
    print(f"请求URL: {url}")
    print(f"查询参数: {params}")
    
    try:
        response = requests.get(url, params=params)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应体: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"解析后的数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        return response
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def main():
    """主测试函数"""
    print("开始测试点赞API接口")
    print(f"测试时间: {datetime.now()}")
    print(f"服务器地址: {BASE_URL}")
    print(f"测试帖子ID: {TEST_POST_ID}")
    print(f"测试用户ID: {TEST_USER_ID}")
    
    # 测试各个接口
    test_like_status()
    test_like_toggle()
    test_post_likers()
    test_user_liked_posts()
    
    print("\n" + "=" * 50)
    print("测试完成")
    print("=" * 50)

if __name__ == "__main__":
    main()
