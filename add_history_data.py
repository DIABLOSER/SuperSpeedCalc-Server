#!/usr/bin/env python3
"""
添加历史记录测试数据脚本
"""
import requests
import json
import time
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5003/api"

def get_users():
    """获取用户列表"""
    try:
        response = requests.get(f"{BASE_URL}/users/")
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        else:
            print(f"❌ 获取用户列表失败: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ 获取用户列表异常: {str(e)}")
        return []

def create_history_record(title, score, user_id):
    """创建历史记录"""
    try:
        data = {
            "title": title,
            "score": score,
            "user": user_id
        }
        
        response = requests.post(
            f"{BASE_URL}/history/",
            headers={"Content-Type": "application/json"},
            json=data
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ 创建历史记录成功: {title} (分数: {score})")
            return result.get('data', {}).get('objectId')
        else:
            print(f"❌ 创建历史记录失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ 创建历史记录异常: {str(e)}")
        return None

def add_test_data():
    """添加测试数据"""
    print("🚀 开始添加历史记录测试数据...")
    
    # 获取用户列表
    users = get_users()
    if not users:
        print("❌ 没有找到用户，无法添加数据")
        return
    
    print(f"📋 找到 {len(users)} 个用户")
    
    # 测试数据配置
    test_data = [
        # 用户1的数据 - 高分用户
        {"user_index": 0, "records": [
            {"title": "超级速度计算挑战", "score": 1500},
            {"title": "数学竞赛第一轮", "score": 1200},
            {"title": "每日练习", "score": 800},
            {"title": "周末挑战赛", "score": 2000},
            {"title": "月度测试", "score": 1800},
            {"title": "快速计算训练", "score": 950},
            {"title": "数学游戏", "score": 1100},
            {"title": "速度测试", "score": 1300}
        ]},
        
        # 用户2的数据 - 中等分数用户
        {"user_index": 1, "records": [
            {"title": "基础计算练习", "score": 600},
            {"title": "数学小测验", "score": 750},
            {"title": "日常训练", "score": 500},
            {"title": "周末练习", "score": 900},
            {"title": "月度考核", "score": 850},
            {"title": "计算速度训练", "score": 700},
            {"title": "数学游戏", "score": 650}
        ]},
        
        # 用户3的数据 - 低分用户
        {"user_index": 2, "records": [
            {"title": "入门练习", "score": 200},
            {"title": "基础测试", "score": 300},
            {"title": "简单计算", "score": 150},
            {"title": "练习模式", "score": 250},
            {"title": "新手挑战", "score": 180}
        ]},
        
        # 用户4的数据 - 波动分数用户
        {"user_index": 3, "records": [
            {"title": "第一次尝试", "score": 100},
            {"title": "进步练习", "score": 400},
            {"title": "突破训练", "score": 800},
            {"title": "失误记录", "score": -50},
            {"title": "重新开始", "score": 300},
            {"title": "稳定发挥", "score": 600},
            {"title": "再次突破", "score": 1000},
            {"title": "保持状态", "score": 750}
        ]}
    ]
    
    created_count = 0
    
    # 为每个用户添加数据
    for user_data in test_data:
        user_index = user_data["user_index"]
        if user_index >= len(users):
            print(f"⚠️ 用户索引 {user_index} 超出范围，跳过")
            continue
            
        user = users[user_index]
        user_id = user.get('objectId')
        username = user.get('username', f'用户{user_index}')
        
        print(f"\n👤 为用户 {username} 添加数据...")
        
        for record in user_data["records"]:
            # 添加一些随机延迟，模拟真实场景
            time.sleep(0.1)
            
            history_id = create_history_record(
                record["title"],
                record["score"],
                user_id
            )
            
            if history_id:
                created_count += 1
    
    print(f"\n🎉 数据添加完成！")
    print(f"📊 总共创建了 {created_count} 条历史记录")
    print(f"👥 涉及 {len(test_data)} 个用户")
    
    # 显示当前数据统计
    print(f"\n📈 当前数据统计:")
    try:
        response = requests.get(f"{BASE_URL}/history/count")
        if response.status_code == 200:
            count_data = response.json()
            total_count = count_data.get('data', {}).get('count', 0)
            print(f"   总历史记录数: {total_count}")
    except Exception as e:
        print(f"   获取统计信息失败: {str(e)}")

if __name__ == '__main__':
    add_test_data()
