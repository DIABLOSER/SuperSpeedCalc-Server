#!/usr/bin/env python3
"""
检查历史记录数据脚本
"""
import requests
import json

BASE_URL = "http://localhost:5003/api"

def check_history_data():
    """检查历史记录数据"""
    print("🔍 检查历史记录数据")
    print("=" * 50)
    
    # 获取历史记录总数
    try:
        response = requests.get(f"{BASE_URL}/history/count")
        if response.status_code == 200:
            count_data = response.json()
            total_count = count_data.get('data', {}).get('count', 0)
            print(f"📊 总历史记录数: {total_count}")
        else:
            print(f"❌ 获取总数失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取总数异常: {str(e)}")
    
    print()
    
    # 获取所有历史记录
    try:
        response = requests.get(f"{BASE_URL}/history/")
        if response.status_code == 200:
            data = response.json()
            histories = data.get('data', [])
            print(f"📋 获取到 {len(histories)} 条历史记录")
            print()
            
            # 显示前10条记录
            print("📝 前10条历史记录:")
            print("-" * 50)
            
            for i, history in enumerate(histories[:10], 1):
                title = history.get('title', '无标题')
                score = history.get('score', 0)
                user_info = history.get('user', {})
                username = user_info.get('username', '未知用户') if isinstance(user_info, dict) else str(user_info)
                created_at = history.get('createdAt', '')
                
                print(f"{i:2d}. {title} - {score}分 (用户: {username})")
                print(f"    创建时间: {created_at}")
                print()
            
            if len(histories) > 10:
                print(f"... 还有 {len(histories) - 10} 条记录")
                
        else:
            print(f"❌ 获取历史记录失败: {response.status_code}")
            print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"❌ 获取历史记录异常: {str(e)}")
    
    print()
    
    # 测试排行榜
    print("🏆 测试排行榜:")
    print("-" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/history/leaderboard?period=all")
        if response.status_code == 200:
            data = response.json()
            leaderboard = data.get('data', [])
            print(f"📈 总排行榜 (共{len(leaderboard)}个用户):")
            
            for i, item in enumerate(leaderboard[:5], 1):
                user_info = item.get('user', {})
                username = user_info.get('username', '未知用户')
                total_score = item.get('total_score', 0)
                record_count = item.get('record_count', 0)
                print(f"   {i}. {username} - {total_score}分 ({record_count}条记录)")
        else:
            print(f"❌ 获取排行榜失败: {response.status_code}")
            print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"❌ 获取排行榜异常: {str(e)}")

if __name__ == '__main__':
    check_history_data()
