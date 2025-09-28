#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
意见反馈API测试脚本
测试反馈功能的创建、查询、更新和删除
"""

import requests
import json
import time

# 服务器配置
BASE_URL = "http://localhost:8000"
FEEDBACK_API = f"{BASE_URL}/api/feedback"

def test_create_feedback():
    """测试创建反馈"""
    print("🧪 测试创建反馈...")
    
    feedback_data = {
        "user_id": "test_user_123",
        "feedback_type": "bug",
        "title": "登录页面显示异常",
        "content": "在登录时页面出现白屏，无法正常使用",
        "priority": "high",
        "contact": "test@example.com",
        "device_info": {
            "device": "iPhone 12",
            "os": "iOS 15.0",
            "browser": "Safari"
        },
        "app_version": "1.0.0",
        "os_info": "iOS 15.0",
        "attachments": [],
        "tags": ["登录", "显示", "Bug"],
        "is_public": False,
        "rating": 3
    }
    
    try:
        response = requests.post(f"{FEEDBACK_API}/create", json=feedback_data)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 反馈创建成功!")
            print(f"反馈ID: {result['data']['feedback']['objectId']}")
            return result['data']['feedback']['objectId']
        else:
            print(f"❌ 创建失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return None

def test_get_feedback_list():
    """测试获取反馈列表"""
    print("\n🧪 测试获取反馈列表...")
    
    params = {
        "page": 1,
        "per_page": 10,
        "current_user_id": "test_user_123",
        "is_admin": "false"
    }
    
    try:
        response = requests.get(f"{FEEDBACK_API}/list", params=params)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 获取反馈列表成功!")
            print(f"总数量: {result['data']['pagination']['total']}")
            print(f"当前页: {result['data']['pagination']['page']}")
            print(f"每页数量: {result['data']['pagination']['per_page']}")
            return result['data']['feedbacks']
        else:
            print(f"❌ 获取失败: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return []

def test_get_feedback_detail(feedback_id):
    """测试获取反馈详情"""
    print(f"\n🧪 测试获取反馈详情 (ID: {feedback_id})...")
    
    params = {
        "current_user_id": "test_user_123",
        "is_admin": "false"
    }
    
    try:
        response = requests.get(f"{FEEDBACK_API}/{feedback_id}", params=params)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 获取反馈详情成功!")
            feedback = result['data']['feedback']
            print(f"标题: {feedback['title']}")
            print(f"类型: {feedback['feedback_type']}")
            print(f"状态: {feedback['status']}")
            print(f"优先级: {feedback['priority']}")
            return feedback
        else:
            print(f"❌ 获取失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return None

def test_update_feedback(feedback_id):
    """测试更新反馈"""
    print(f"\n🧪 测试更新反馈 (ID: {feedback_id})...")
    
    update_data = {
        "title": "登录页面显示异常 - 已更新",
        "content": "在登录时页面出现白屏，无法正常使用。经过测试，问题依然存在。",
        "rating": 4,
        "tags": ["登录", "显示", "Bug", "已更新"]
    }
    
    params = {
        "current_user_id": "test_user_123",
        "is_admin": "false"
    }
    
    try:
        response = requests.put(f"{FEEDBACK_API}/{feedback_id}", json=update_data, params=params)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 反馈更新成功!")
            print(f"新标题: {result['data']['feedback']['title']}")
            print(f"新评分: {result['data']['feedback']['rating']}")
            return result['data']['feedback']
        else:
            print(f"❌ 更新失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return None

def test_admin_reply(feedback_id):
    """测试管理员回复"""
    print(f"\n🧪 测试管理员回复 (ID: {feedback_id})...")
    
    reply_data = {
        "reply": "感谢您的反馈！我们已经定位到问题，将在下个版本中修复。"
    }
    
    params = {
        "current_user_id": "admin_123",
        "is_admin": "true"
    }
    
    try:
        response = requests.post(f"{FEEDBACK_API}/{feedback_id}/reply", json=reply_data, params=params)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 管理员回复成功!")
            print(f"回复内容: {result['data']['feedback']['admin_reply']}")
            return result['data']['feedback']
        else:
            print(f"❌ 回复失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return None

def test_get_stats():
    """测试获取统计信息"""
    print("\n🧪 测试获取反馈统计...")
    
    try:
        response = requests.get(f"{FEEDBACK_API}/stats")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 获取统计信息成功!")
            stats = result['data']['stats']
            print(f"总反馈数: {stats['total_count']}")
            print(f"待处理: {stats['pending_count']}")
            print(f"已解决: {stats['resolved_count']}")
            return stats
        else:
            print(f"❌ 获取失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return None

def test_my_feedback():
    """测试获取我的反馈"""
    print("\n🧪 测试获取我的反馈...")
    
    params = {
        "user_id": "test_user_123",
        "page": 1,
        "per_page": 10
    }
    
    try:
        response = requests.get(f"{FEEDBACK_API}/my", params=params)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 获取我的反馈成功!")
            print(f"我的反馈数量: {result['data']['pagination']['total']}")
            return result['data']['feedbacks']
        else:
            print(f"❌ 获取失败: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")
        return []

def main():
    """主测试函数"""
    print("🚀 开始测试意见反馈API...")
    print("=" * 50)
    
    # 测试创建反馈
    feedback_id = test_create_feedback()
    if not feedback_id:
        print("❌ 创建反馈失败，终止测试")
        return
    
    # 等待一下，确保数据已保存
    time.sleep(1)
    
    # 测试获取反馈列表
    feedbacks = test_get_feedback_list()
    
    # 测试获取反馈详情
    feedback_detail = test_get_feedback_detail(feedback_id)
    
    # 测试更新反馈
    updated_feedback = test_update_feedback(feedback_id)
    
    # 测试管理员回复
    replied_feedback = test_admin_reply(feedback_id)
    
    # 测试获取统计信息
    stats = test_get_stats()
    
    # 测试获取我的反馈
    my_feedbacks = test_my_feedback()
    
    print("\n" + "=" * 50)
    print("🎉 测试完成!")
    print(f"✅ 创建反馈: {'成功' if feedback_id else '失败'}")
    print(f"✅ 获取列表: {'成功' if feedbacks else '失败'}")
    print(f"✅ 获取详情: {'成功' if feedback_detail else '失败'}")
    print(f"✅ 更新反馈: {'成功' if updated_feedback else '失败'}")
    print(f"✅ 管理员回复: {'成功' if replied_feedback else '失败'}")
    print(f"✅ 获取统计: {'成功' if stats else '失败'}")
    print(f"✅ 我的反馈: {'成功' if my_feedbacks else '失败'}")

if __name__ == '__main__':
    main()
