#!/usr/bin/env python3
"""
测试History API返回的用户信息是否完整
"""

import requests
import json

# API基础URL
BASE_URL = 'http://localhost:5003/api'

def test_user_info():
    """测试返回的用户信息是否完整"""
    
    print("🧪 开始测试用户信息返回...")
    
    # 1. 获取用户列表
    print("\n1. 获取用户列表...")
    try:
        response = requests.get(f'{BASE_URL}/users/')
        if response.status_code == 200:
            users = response.json().get('data', [])
            if users:
                test_user = users[0]
                user_id = test_user['objectId']
                print(f"✅ 使用用户: {test_user['username']} (ID: {user_id})")
                print(f"   用户信息: {json.dumps(test_user, indent=2, ensure_ascii=False)}")
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
        'title': '测试用户信息',
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
    
    # 3. 测试获取历史记录列表的用户信息
    print("\n3. 测试历史记录列表的用户信息...")
    try:
        response = requests.get(f'{BASE_URL}/history/')
        if response.status_code == 200:
            histories = response.json().get('data', [])
            if histories:
                history = histories[0]
                print(f"✅ 获取历史记录列表成功，用户信息:")
                if 'user' in history:
                    user_info = history['user']
                    print(f"   用户ID: {user_info.get('objectId')}")
                    print(f"   用户名: {user_info.get('username')}")
                    print(f"   头像: {user_info.get('avatar')}")
                    print(f"   简介: {user_info.get('bio')}")
                    print(f"   积分: {user_info.get('score')}")
                    print(f"   经验: {user_info.get('experence')}")
                    print(f"   菠萝币: {user_info.get('boluo')}")
                    print(f"   是否激活: {user_info.get('isActive')}")
                    print(f"   是否管理员: {user_info.get('admin')}")
                    print(f"   性别: {user_info.get('sex')}")
                    print(f"   生日: {user_info.get('birthday')}")
                    print(f"   创建时间: {user_info.get('createdAt')}")
                    print(f"   更新时间: {user_info.get('updatedAt')}")
                else:
                    print("❌ 历史记录中没有用户信息")
            else:
                print("❌ 没有获取到历史记录")
        else:
            print(f"❌ 获取历史记录列表失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取历史记录列表失败: {str(e)}")
    
    # 4. 测试获取单个历史记录的用户信息
    print("\n4. 测试单个历史记录的用户信息...")
    try:
        response = requests.get(f'{BASE_URL}/history/{history_id}')
        if response.status_code == 200:
            history = response.json().get('data')
            print(f"✅ 获取单个历史记录成功，用户信息:")
            if 'user' in history:
                user_info = history['user']
                print(f"   用户ID: {user_info.get('objectId')}")
                print(f"   用户名: {user_info.get('username')}")
                print(f"   头像: {user_info.get('avatar')}")
                print(f"   简介: {user_info.get('bio')}")
                print(f"   积分: {user_info.get('score')}")
                print(f"   经验: {user_info.get('experience')}")
                print(f"   菠萝币: {user_info.get('boluo')}")
                print(f"   是否激活: {user_info.get('isActive')}")
                print(f"   是否管理员: {user_info.get('admin')}")
                print(f"   性别: {user_info.get('sex')}")
                print(f"   生日: {user_info.get('birthday')}")
                print(f"   创建时间: {user_info.get('createdAt')}")
                print(f"   更新时间: {user_info.get('updatedAt')}")
            else:
                print("❌ 历史记录中没有用户信息")
        else:
            print(f"❌ 获取单个历史记录失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取单个历史记录失败: {str(e)}")
    
    # 5. 测试排行榜的用户信息
    print("\n5. 测试排行榜的用户信息...")
    try:
        response = requests.get(f'{BASE_URL}/history/leaderboard?period=all')
        if response.status_code == 200:
            leaderboard = response.json().get('data', [])
            if leaderboard:
                item = leaderboard[0]
                print(f"✅ 获取排行榜成功，第一名用户信息:")
                if 'user' in item:
                    user_info = item['user']
                    print(f"   排名: {item.get('rank')}")
                    print(f"   用户ID: {user_info.get('objectId')}")
                    print(f"   用户名: {user_info.get('username')}")
                    print(f"   头像: {user_info.get('avatar')}")
                    print(f"   简介: {user_info.get('bio')}")
                    print(f"   积分: {user_info.get('score')}")
                    print(f"   经验: {user_info.get('experience')}")
                    print(f"   菠萝币: {user_info.get('boluo')}")
                    print(f"   是否激活: {user_info.get('isActive')}")
                    print(f"   是否管理员: {user_info.get('admin')}")
                    print(f"   性别: {user_info.get('sex')}")
                    print(f"   生日: {user_info.get('birthday')}")
                    print(f"   创建时间: {user_info.get('createdAt')}")
                    print(f"   更新时间: {user_info.get('updatedAt')}")
                    print(f"   总分: {item.get('total_score')}")
                    print(f"   记录数: {item.get('history_count')}")
                else:
                    print("❌ 排行榜中没有用户信息")
            else:
                print("❌ 没有获取到排行榜数据")
        else:
            print(f"❌ 获取排行榜失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取排行榜失败: {str(e)}")
    
    # 6. 测试用户统计的用户信息
    print("\n6. 测试用户统计的用户信息...")
    try:
        response = requests.get(f'{BASE_URL}/history/stats?user={user_id}')
        if response.status_code == 200:
            stats = response.json().get('data', {})
            print(f"✅ 获取用户统计成功，用户信息:")
            if 'user' in stats:
                user_info = stats['user']
                print(f"   用户ID: {user_info.get('objectId')}")
                print(f"   用户名: {user_info.get('username')}")
                print(f"   头像: {user_info.get('avatar')}")
                print(f"   简介: {user_info.get('bio')}")
                print(f"   积分: {user_info.get('score')}")
                print(f"   经验: {user_info.get('experience')}")
                print(f"   菠萝币: {user_info.get('boluo')}")
                print(f"   是否激活: {user_info.get('isActive')}")
                print(f"   是否管理员: {user_info.get('admin')}")
                print(f"   性别: {user_info.get('sex')}")
                print(f"   生日: {user_info.get('birthday')}")
                print(f"   创建时间: {user_info.get('createdAt')}")
                print(f"   更新时间: {user_info.get('updatedAt')}")
            else:
                print("❌ 用户统计中没有用户信息")
        else:
            print(f"❌ 获取用户统计失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取用户统计失败: {str(e)}")
    
    # 7. 清理测试数据
    print("\n7. 清理测试数据...")
    try:
        response = requests.delete(f'{BASE_URL}/history/{history_id}')
        if response.status_code == 200:
            print("✅ 历史记录删除成功")
        else:
            print(f"❌ 删除历史记录失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 删除历史记录失败: {str(e)}")
    
    print("\n🎉 用户信息测试完成!")

if __name__ == '__main__':
    test_user_info()
