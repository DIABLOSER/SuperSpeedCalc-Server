#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
收藏功能API测试脚本
测试收藏功能的创建、查询、删除等操作
"""

import requests
import json
import time

# 服务器配置
BASE_URL = "http://localhost:8000"
COLLECT_API = f"{BASE_URL}/collect"

def test_create_collect():
    """测试创建收藏"""
    print("🧪 测试创建收藏...")
    
    # 使用实际的用户ID和帖子ID（从日志中获取）
    collect_data = {
        "user_id": "biqy6flpeh",  # 从日志中获取的用户ID
        "post_id": "ov4qfg6j7c"   # 从日志中获取的帖子ID
    }
    
    try:
        response = requests.post(f"{COLLECT_API}/create", json=collect_data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 收藏创建成功!")
            print(f"收藏ID: {result['data']['collect_id']}")
            return result['data']['collect_id']
        else:
            print(f"❌ 创建失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return None

def test_get_user_collects():
    """测试获取用户收藏列表"""
    print("\n🧪 测试获取用户收藏列表...")
    
    user_id = "biqy6flpeh"
    params = {
        "page": 1,
        "per_page": 10
    }
    
    try:
        response = requests.get(f"{COLLECT_API}/user/{user_id}/posts", params=params)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 获取用户收藏列表成功!")
            print(f"收藏数量: {result['data']['pagination']['total']}")
            print(f"当前页: {result['data']['pagination']['page']}")
            return result['data'].get('collected_posts', [])
        else:
            print(f"❌ 获取失败: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return []

def test_get_collect_status():
    """测试获取收藏状态"""
    print("\n🧪 测试获取收藏状态...")
    
    user_id = "biqy6flpeh"
    post_id = "ov4qfg6j7c"
    
    try:
        response = requests.get(f"{COLLECT_API}/status/{user_id}/{post_id}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 获取收藏状态成功!")
            print(f"是否已收藏: {result['data']['is_collected']}")
            return result['data']
        else:
            print(f"❌ 获取失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return None

def test_get_user_collect_stats():
    """测试获取用户收藏统计"""
    print("\n🧪 测试获取用户收藏统计...")
    
    user_id = "biqy6flpeh"
    
    try:
        response = requests.get(f"{COLLECT_API}/user/{user_id}/stats")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 获取用户收藏统计成功!")
            print(f"收藏总数: {result['data']['collect_count']}")
            return result['data']
        else:
            print(f"❌ 获取失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return None

def test_delete_collect(collect_id):
    """测试删除收藏"""
    print(f"\n🧪 测试删除收藏 (ID: {collect_id})...")
    
    try:
        response = requests.delete(f"{COLLECT_API}/{collect_id}")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 删除收藏成功!")
            print(f"删除的收藏ID: {result['data']['collect_id']}")
            return True
        else:
            print(f"❌ 删除失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return False

def test_duplicate_collect():
    """测试重复收藏"""
    print("\n🧪 测试重复收藏...")
    
    collect_data = {
        "user_id": "biqy6flpeh",
        "post_id": "ov4qfg6j7c"
    }
    
    try:
        response = requests.post(f"{COLLECT_API}/create", json=collect_data)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 400:
            result = response.json()
            print("✅ 重复收藏检测正常!")
            print(f"错误信息: {result['message']}")
            return True
        else:
            print(f"❌ 重复收藏检测异常: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return False

def test_invalid_collect():
    """测试无效收藏（不存在的用户或帖子）"""
    print("\n🧪 测试无效收藏...")
    
    # 测试不存在的用户
    invalid_data = {
        "user_id": "invalid_user_id",
        "post_id": "ov4qfg6j7c"
    }
    
    try:
        response = requests.post(f"{COLLECT_API}/create", json=invalid_data)
        print(f"不存在的用户 - 状态码: {response.status_code}")
        
        if response.status_code == 404:
            print("✅ 无效用户检测正常!")
        else:
            print(f"❌ 无效用户检测异常: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
    
    # 测试不存在的帖子
    invalid_data = {
        "user_id": "biqy6flpeh",
        "post_id": "invalid_post_id"
    }
    
    try:
        response = requests.post(f"{COLLECT_API}/create", json=invalid_data)
        print(f"不存在的帖子 - 状态码: {response.status_code}")
        
        if response.status_code == 404:
            print("✅ 无效帖子检测正常!")
        else:
            print(f"❌ 无效帖子检测异常: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")

def main():
    """主测试函数"""
    print("🚀 开始测试收藏功能API...")
    print("=" * 50)
    
    # 先测试查询功能
    print("📋 测试查询功能...")
    collects = test_get_user_collects()
    collect_status = test_get_collect_status()
    collect_stats = test_get_user_collect_stats()
    
    # 测试重复收藏
    print("\n🔄 测试重复收藏...")
    duplicate_test = test_duplicate_collect()
    
    # 测试无效收藏
    print("\n❌ 测试无效收藏...")
    test_invalid_collect()
    
    # 如果有收藏记录，测试删除功能
    if collects and len(collects) > 0:
        print("\n🗑️ 测试删除功能...")
        collect_id = collects[0]['objectId']
        delete_success = test_delete_collect(collect_id)
        
        # 删除后重新创建收藏
        print("\n➕ 重新创建收藏...")
        collect_id = test_create_collect()
    else:
        print("\n➕ 测试创建收藏...")
        collect_id = test_create_collect()
        delete_success = False
    
    print("\n" + "=" * 50)
    print("🎉 测试完成!")
    print(f"✅ 获取收藏列表: {'成功' if collects else '失败'}")
    print(f"✅ 获取收藏状态: {'成功' if collect_status else '失败'}")
    print(f"✅ 获取收藏统计: {'成功' if collect_stats else '失败'}")
    print(f"✅ 重复收藏检测: {'成功' if duplicate_test else '失败'}")
    print(f"✅ 创建收藏: {'成功' if collect_id else '失败'}")
    print(f"✅ 删除收藏: {'成功' if delete_success else '失败'}")

if __name__ == '__main__':
    main()
