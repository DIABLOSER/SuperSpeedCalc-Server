#!/usr/bin/env python3
"""
展示历史记录数据脚本
"""
import requests
import json

BASE_URL = "http://localhost:5003/api"

def get_all_history():
    """获取所有历史记录"""
    try:
        response = requests.get(f"{BASE_URL}/history/")
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        else:
            print(f"❌ 获取历史记录失败: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ 获取历史记录异常: {str(e)}")
        return []

def get_leaderboard(period="all"):
    """获取排行榜"""
    try:
        response = requests.get(f"{BASE_URL}/history/leaderboard?period={period}")
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        else:
            print(f"❌ 获取{period}排行榜失败: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ 获取{period}排行榜异常: {str(e)}")
        return []

def get_user_stats(user_id):
    """获取用户统计"""
    try:
        response = requests.get(f"{BASE_URL}/history/stats?user={user_id}")
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {})
        else:
            print(f"❌ 获取用户统计失败: {response.status_code}")
            return {}
    except Exception as e:
        print(f"❌ 获取用户统计异常: {str(e)}")
        return {}

def show_history_data():
    """展示历史记录数据"""
    print("📊 历史记录数据展示")
    print("=" * 50)
    
    # 获取所有历史记录
    histories = get_all_history()
    if not histories:
        print("❌ 没有找到历史记录数据")
        return
    
    print(f"📋 总记录数: {len(histories)}")
    print()
    
    # 按用户分组显示数据
    user_data = {}
    for history in histories:
        user_id = history.get('user')
        if isinstance(user_id, dict):
            user_id = user_id.get('objectId')
        
        if user_id not in user_data:
            user_data[user_id] = {
                'username': history.get('user', {}).get('username', user_id) if isinstance(history.get('user'), dict) else user_id,
                'records': [],
                'total_score': 0,
                'count': 0
            }
        
        score = history.get('score', 0)
        user_data[user_id]['records'].append({
            'title': history.get('title'),
            'score': score,
            'createdAt': history.get('createdAt')
        })
        user_data[user_id]['total_score'] += score
        user_data[user_id]['count'] += 1
    
    # 显示每个用户的数据
    print("👥 用户数据详情:")
    print("-" * 50)
    
    for user_id, data in user_data.items():
        print(f"\n👤 用户: {data['username']} (ID: {user_id})")
        print(f"   总分数: {data['total_score']}")
        print(f"   记录数: {data['count']}")
        print(f"   平均分: {data['total_score'] / data['count']:.1f}")
        print("   记录列表:")
        
        for i, record in enumerate(data['records'][:5], 1):  # 只显示前5条
            print(f"     {i}. {record['title']} - {record['score']}分")
        
        if len(data['records']) > 5:
            print(f"     ... 还有 {len(data['records']) - 5} 条记录")
    
    # 显示排行榜
    print("\n🏆 排行榜信息:")
    print("-" * 50)
    
    periods = [
        ("总榜", "all"),
        ("日榜", "daily"),
        ("月榜", "monthly"),
        ("年榜", "yearly")
    ]
    
    for period_name, period in periods:
        leaderboard = get_leaderboard(period)
        if leaderboard:
            print(f"\n📈 {period_name}:")
            for i, item in enumerate(leaderboard[:5], 1):  # 只显示前5名
                user_info = item.get('user', {})
                username = user_info.get('username', '未知用户')
                total_score = item.get('total_score', 0)
                record_count = item.get('record_count', 0)
                print(f"   {i}. {username} - {total_score}分 ({record_count}条记录)")
    
    # 显示用户统计详情
    print("\n📊 用户统计详情:")
    print("-" * 50)
    
    for user_id, data in user_data.items():
        stats = get_user_stats(user_id)
        if stats:
            print(f"\n👤 {data['username']} 的统计:")
            print(f"   今日: {stats.get('today_score', 0)}分 ({stats.get('today_count', 0)}条)")
            print(f"   本月: {stats.get('monthly_score', 0)}分 ({stats.get('monthly_count', 0)}条)")
            print(f"   今年: {stats.get('yearly_score', 0)}分 ({stats.get('yearly_count', 0)}条)")
            print(f"   总计: {stats.get('total_score', 0)}分 ({stats.get('total_count', 0)}条)")

if __name__ == '__main__':
    show_history_data()
