#!/usr/bin/env python3
"""
测试History API的脚本
"""

import requests
import json

# API基础URL
BASE_URL = 'http://localhost:5003/api'

def test_history_api():
    """测试History API的所有功能"""
    
    print("🧪 开始测试History API...")
    
    # 1. 首先获取一个用户用于测试
    print("\n1. 获取用户列表...")
    try:
        response = requests.get(f'{BASE_URL}/users/')
        if response.status_code == 200:
            users = response.json().get('data', [])
            if users:
                test_user = users[0]
                user_id = test_user['objectId']
                print(f"✅ 使用用户: {test_user['username']} (ID: {user_id})")
            else:
                print("❌ 没有找到用户，无法继续测试")
                return
        else:
            print(f"❌ 获取用户失败: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 连接服务器失败: {str(e)}")
        return
    
    # 2. 创建历史记录
    print("\n2. 创建历史记录...")
    history_data = {
        'title': '测试历史记录',
        'score': 100,
        'user': user_id
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/history/',
            json=history_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            created_history = response.json().get('data')
            history_id = created_history['objectId']
            print(f"✅ 历史记录创建成功: {created_history['title']} (ID: {history_id})")
        else:
            print(f"❌ 创建历史记录失败: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ 创建历史记录失败: {str(e)}")
        return
    
    # 3. 获取历史记录列表
    print("\n3. 获取历史记录列表...")
    try:
        response = requests.get(f'{BASE_URL}/history/')
        if response.status_code == 200:
            histories = response.json().get('data', [])
            print(f"✅ 获取到 {len(histories)} 条历史记录")
        else:
            print(f"❌ 获取历史记录列表失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取历史记录列表失败: {str(e)}")
    
    # 4. 获取单个历史记录
    print("\n4. 获取单个历史记录...")
    try:
        response = requests.get(f'{BASE_URL}/history/{history_id}')
        if response.status_code == 200:
            history = response.json().get('data')
            print(f"✅ 获取历史记录成功: {history['title']}")
        else:
            print(f"❌ 获取单个历史记录失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取单个历史记录失败: {str(e)}")
    
    # 5. 更新历史记录
    print("\n5. 更新历史记录...")
    update_data = {
        'title': '更新后的历史记录',
        'score': 200
    }
    
    try:
        response = requests.put(
            f'{BASE_URL}/history/{history_id}',
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            updated_history = response.json().get('data')
            print(f"✅ 历史记录更新成功: {updated_history['title']} (score: {updated_history['score']})")
        else:
            print(f"❌ 更新历史记录失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 更新历史记录失败: {str(e)}")
    
    # 6. 获取历史记录总数
    print("\n6. 获取历史记录总数...")
    try:
        response = requests.get(f'{BASE_URL}/history/count')
        if response.status_code == 200:
            count = response.json().get('data', {}).get('count', 0)
            print(f"✅ 历史记录总数: {count}")
        else:
            print(f"❌ 获取历史记录总数失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取历史记录总数失败: {str(e)}")
    
    # 7. 删除历史记录
    print("\n7. 删除历史记录...")
    try:
        response = requests.delete(f'{BASE_URL}/history/{history_id}')
        if response.status_code == 200:
            print("✅ 历史记录删除成功")
        else:
            print(f"❌ 删除历史记录失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 删除历史记录失败: {str(e)}")
    
    print("\n🎉 History API测试完成!")

if __name__ == '__main__':
    test_history_api()
