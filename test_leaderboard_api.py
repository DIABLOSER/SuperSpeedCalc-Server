#!/usr/bin/env python3
"""
测试History排行榜API的脚本
"""

import requests
import json
import time

# API基础URL
BASE_URL = 'http://localhost:5003/api'

def test_leaderboard_api():
    """测试History排行榜API的所有功能"""
    
    print("🧪 开始测试History排行榜API...")
    
    # 1. 首先获取用户列表
    print("\n1. 获取用户列表...")
    try:
        response = requests.get(f'{BASE_URL}/users/')
        if response.status_code == 200:
            users = response.json().get('data', [])
            if len(users) < 2:
                print("❌ 需要至少2个用户来测试排行榜功能")
                return
            test_users = users[:2]  # 使用前两个用户
            print(f"✅ 使用用户: {test_users[0]['username']} 和 {test_users[1]['username']}")
        else:
            print(f"❌ 获取用户失败: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 连接服务器失败: {str(e)}")
        return
    
    # 2. 为两个用户创建一些历史记录
    print("\n2. 创建测试历史记录...")
    history_ids = []
    
    # 为用户1创建记录
    for i in range(3):
        history_data = {
            'title': f'用户1测试记录{i+1}',
            'score': 100 + i * 50,  # 100, 150, 200
            'user': test_users[0]['objectId']
        }
        
        try:
            response = requests.post(
                f'{BASE_URL}/history/',
                json=history_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                created_history = response.json().get('data')
                history_ids.append(created_history['objectId'])
                print(f"✅ 为用户1创建记录: {created_history['title']} (score: {created_history['score']})")
            else:
                print(f"❌ 创建历史记录失败: {response.status_code}")
                return
        except Exception as e:
            print(f"❌ 创建历史记录失败: {str(e)}")
            return
    
    # 为用户2创建记录
    for i in range(2):
        history_data = {
            'title': f'用户2测试记录{i+1}',
            'score': 80 + i * 30,  # 80, 110
            'user': test_users[1]['objectId']
        }
        
        try:
            response = requests.post(
                f'{BASE_URL}/history/',
                json=history_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                created_history = response.json().get('data')
                history_ids.append(created_history['objectId'])
                print(f"✅ 为用户2创建记录: {created_history['title']} (score: {created_history['score']})")
            else:
                print(f"❌ 创建历史记录失败: {response.status_code}")
                return
        except Exception as e:
            print(f"❌ 创建历史记录失败: {str(e)}")
            return
    
    # 等待一秒确保数据写入
    time.sleep(1)
    
    # 3. 测试总排行榜
    print("\n3. 测试总排行榜...")
    try:
        response = requests.get(f'{BASE_URL}/history/leaderboard?period=all')
        if response.status_code == 200:
            leaderboard = response.json().get('data', [])
            print(f"✅ 总排行榜获取成功，共 {len(leaderboard)} 个用户")
            for i, item in enumerate(leaderboard[:3]):  # 显示前3名
                print(f"  第{item['rank']}名: {item['user']['username']} - 总分: {item['total_score']}")
        else:
            print(f"❌ 获取总排行榜失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取总排行榜失败: {str(e)}")
    
    # 4. 测试日榜
    print("\n4. 测试日榜...")
    try:
        response = requests.get(f'{BASE_URL}/history/leaderboard?period=daily')
        if response.status_code == 200:
            leaderboard = response.json().get('data', [])
            print(f"✅ 日榜获取成功，共 {len(leaderboard)} 个用户")
            for i, item in enumerate(leaderboard[:3]):
                print(f"  第{item['rank']}名: {item['user']['username']} - 今日总分: {item['total_score']}")
        else:
            print(f"❌ 获取日榜失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取日榜失败: {str(e)}")
    
    # 5. 测试月榜
    print("\n5. 测试月榜...")
    try:
        response = requests.get(f'{BASE_URL}/history/leaderboard?period=monthly')
        if response.status_code == 200:
            leaderboard = response.json().get('data', [])
            print(f"✅ 月榜获取成功，共 {len(leaderboard)} 个用户")
            for i, item in enumerate(leaderboard[:3]):
                print(f"  第{item['rank']}名: {item['user']['username']} - 本月总分: {item['total_score']}")
        else:
            print(f"❌ 获取月榜失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取月榜失败: {str(e)}")
    
    # 6. 测试年榜
    print("\n6. 测试年榜...")
    try:
        response = requests.get(f'{BASE_URL}/history/leaderboard?period=yearly')
        if response.status_code == 200:
            leaderboard = response.json().get('data', [])
            print(f"✅ 年榜获取成功，共 {len(leaderboard)} 个用户")
            for i, item in enumerate(leaderboard[:3]):
                print(f"  第{item['rank']}名: {item['user']['username']} - 今年总分: {item['total_score']}")
        else:
            print(f"❌ 获取年榜失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取年榜失败: {str(e)}")
    
    # 7. 测试用户统计
    print("\n7. 测试用户统计...")
    try:
        response = requests.get(f'{BASE_URL}/history/stats?user={test_users[0]["objectId"]}')
        if response.status_code == 200:
            stats = response.json().get('data', {})
            print(f"✅ 用户统计获取成功: {stats['user']['username']}")
            print(f"  今日: 总分 {stats['stats']['today']['total_score']}, 记录数 {stats['stats']['today']['count']}")
            print(f"  本月: 总分 {stats['stats']['month']['total_score']}, 记录数 {stats['stats']['month']['count']}")
            print(f"  今年: 总分 {stats['stats']['year']['total_score']}, 记录数 {stats['stats']['year']['count']}")
            print(f"  总计: 总分 {stats['stats']['total']['total_score']}, 记录数 {stats['stats']['total']['count']}")
        else:
            print(f"❌ 获取用户统计失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取用户统计失败: {str(e)}")
    
    # 8. 清理测试数据
    print("\n8. 清理测试数据...")
    for history_id in history_ids:
        try:
            response = requests.delete(f'{BASE_URL}/history/{history_id}')
            if response.status_code == 200:
                print(f"✅ 删除历史记录: {history_id}")
            else:
                print(f"❌ 删除历史记录失败: {history_id}")
        except Exception as e:
            print(f"❌ 删除历史记录失败: {str(e)}")
    
    print("\n🎉 History排行榜API测试完成!")

if __name__ == '__main__':
    test_leaderboard_api()
