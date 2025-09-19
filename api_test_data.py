#!/usr/bin/env python3
"""
使用API接口创建测试数据
通过调用每个表的创建接口来生成30条测试数据
"""

import os
import sys
import json
import random
import requests
from datetime import datetime, date

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 服务器配置
BASE_URL = "http://localhost:8000"  # 使用修改后的端口
API_ENDPOINTS = {
    'users': '/users',
    'charts': '/charts', 
    'posts': '/posts',
    'history': '/history',
    'relationships': '/users',  # 关注关系使用用户接口
    'replies': '/replies',
    'likes': '/posts',  # 点赞使用帖子接口
    'banners': '/banners',
    'releases': '/releases',
    'images': '/images'
}

def make_request(method, endpoint, data=None):
    """发送HTTP请求"""
    url = f"{BASE_URL}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, json=data)
        elif method.upper() == 'PUT':
            response = requests.put(url, headers=headers, json=data)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        return response
    except requests.exceptions.ConnectionError:
        print(f"❌ 无法连接到服务器 {url}")
        return None
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return None

def create_users(count=30):
    """创建用户测试数据"""
    print(f"正在创建 {count} 个用户...")
    users = []
    
    for i in range(count):
        user_data = {
            'username': f'test_user_{i+1:02d}',
            'mobile': f'138{random.randint(10000000, 99999999)}',
            'password': 'password123',
            'avatar': f'https://api.dicebear.com/7.x/avataaars/svg?seed=user{i+1}',
            'bio': f'这是测试用户{i+1}的个人简介，用于测试数据展示。',
            'experience': random.randint(0, 10000),
            'boluo': random.randint(0, 1000),
            'isActive': random.choice([True, True, True, False]),
            'admin': random.choice([True, False, False, False, False]),
            'sex': random.choice([0, 1]),
            'birthday': f'199{random.randint(0, 9)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}'
        }
        
        response = make_request('POST', f"{API_ENDPOINTS['users']}/", user_data)
        if response and response.status_code == 201:
            user_info = response.json()
            users.append(user_info['data'])
            print(f"✅ 创建用户 {i+1}: {user_data['username']}")
        else:
            print(f"❌ 创建用户 {i+1} 失败")
    
    print(f"✅ 成功创建 {len(users)} 个用户")
    return users

def create_charts(users, count=30):
    """创建图表测试数据"""
    print(f"正在创建 {count} 个图表...")
    
    chart_titles = [
        "数学速算挑战", "心算大师", "数字记忆王", "计算速度测试",
        "算术练习", "数学竞赛", "速算达人", "数字游戏",
        "计算挑战", "数学训练", "心算练习", "算术测试",
        "数字速算", "计算大师", "数学游戏", "速算竞赛",
        "算术挑战", "数学练习", "心算测试", "数字训练",
        "计算练习", "数学速算", "算术游戏", "心算挑战",
        "数字计算", "数学测试", "速算练习", "算术训练",
        "计算游戏", "数学挑战"
    ]
    
    for i in range(count):
        if not users:
            print("❌ 没有用户数据，无法创建图表")
            break
            
        user = random.choice(users)
        chart_data = {
            'title': random.choice(chart_titles),
            'achievement': round(random.uniform(0.0, 100.0), 2),
            'user': user['objectId']
        }
        
        response = make_request('POST', f"{API_ENDPOINTS['charts']}/", chart_data)
        if response and response.status_code == 201:
            print(f"✅ 创建图表 {i+1}: {chart_data['title']}")
        else:
            print(f"❌ 创建图表 {i+1} 失败")
    
    print(f"✅ 图表创建完成")

def create_posts(users, count=30):
    """创建帖子测试数据"""
    print(f"正在创建 {count} 个帖子...")
    posts = []
    
    post_contents = [
        "今天完成了数学速算挑战，感觉自己的计算能力又提升了！",
        "分享一个快速计算的小技巧，希望对大家有帮助。",
        "刚刚在速算比赛中获得了第一名，太开心了！",
        "数学真的很有趣，每天练习都有新的收获。",
        "推荐几个好用的数学学习APP，大家一起进步。",
        "心算练习真的很锻炼大脑，推荐大家试试。",
        "今天学习了新的计算方法，效率提升了很多。",
        "数学竞赛即将开始，大家一起加油！",
        "分享一些数学公式的记忆方法。",
        "速算技巧分享：如何快速计算两位数乘法。",
        "数学学习心得：坚持练习最重要。",
        "今天挑战了高难度数学题，虽然很难但很有成就感。",
        "推荐几本数学学习书籍，适合各个年龄段。",
        "数学游戏推荐：寓教于乐的学习方式。",
        "速算训练营开课了，欢迎大家参加。",
        "数学思维训练：如何提高逻辑思维能力。",
        "今天在数学课上学会了新方法，分享给大家。",
        "数学竞赛经验分享：如何准备和应对。",
        "速算技巧大全：从基础到高级。",
        "数学学习计划：如何制定有效的学习计划。",
        "今天完成了100道速算题，感觉很有成就感！",
        "数学公式记忆法：让学习更轻松。",
        "速算比赛回顾：精彩瞬间分享。",
        "数学学习方法：如何提高学习效率。",
        "今天学习了新的数学概念，感觉很有趣。",
        "速算练习心得：坚持就是胜利。",
        "数学竞赛准备：如何系统性地复习。",
        "今天挑战了心算极限，结果超出预期！",
        "数学学习资源推荐：优质学习材料分享。",
        "速算技巧进阶：高级计算方法分享。"
    ]
    
    for i in range(count):
        if not users:
            print("❌ 没有用户数据，无法创建帖子")
            break
            
        user = random.choice(users)
        post_data = {
            'user': user['objectId'],
            'content': random.choice(post_contents),
            'visible': random.choice([True, True, True, False]),
            'audit_state': random.choice(['approved', 'approved', 'approved', 'pending']),
            'images': []
        }
        
        # 随机添加图片
        if random.choice([True, False]):
            image_count = random.randint(1, 3)
            for j in range(image_count):
                post_data['images'].append(f"https://picsum.photos/400/300?random={i*10+j}")
        
        response = make_request('POST', f"{API_ENDPOINTS['posts']}/", post_data)
        if response and response.status_code == 201:
            post_info = response.json()
            posts.append(post_info['data'])
            print(f"✅ 创建帖子 {i+1}: {post_data['content'][:20]}...")
        else:
            print(f"❌ 创建帖子 {i+1} 失败")
    
    print(f"✅ 成功创建 {len(posts)} 个帖子")
    return posts

def create_history(users, count=30):
    """创建历史记录测试数据"""
    print(f"正在创建 {count} 个历史记录...")
    
    history_titles = [
        "数学速算练习", "心算挑战", "计算速度测试", "算术竞赛",
        "数字记忆训练", "数学游戏", "速算比赛", "计算练习",
        "数学测试", "心算训练", "算术挑战", "数字游戏",
        "计算竞赛", "数学练习", "速算训练", "算术测试",
        "数字计算", "数学挑战", "心算竞赛", "计算游戏",
        "数学速算", "算术练习", "数字训练", "计算测试",
        "数学竞赛", "速算练习", "心算游戏", "算术训练",
        "数字速算", "计算挑战"
    ]
    
    for i in range(count):
        if not users:
            print("❌ 没有用户数据，无法创建历史记录")
            break
            
        user = random.choice(users)
        history_data = {
            'title': random.choice(history_titles),
            'score': random.randint(-50, 100),
            'user': user['objectId']
        }
        
        response = make_request('POST', f"{API_ENDPOINTS['history']}/", history_data)
        if response and response.status_code == 201:
            print(f"✅ 创建历史记录 {i+1}: {history_data['title']}")
        else:
            print(f"❌ 创建历史记录 {i+1} 失败")
    
    print(f"✅ 历史记录创建完成")

def create_relationships(users, count=30):
    """创建用户关注关系测试数据"""
    print(f"正在创建 {count} 个关注关系...")
    
    existing_relationships = set()
    
    for i in range(count):
        if len(users) < 2:
            print("❌ 用户数量不足，无法创建关注关系")
            break
            
        follower = random.choice(users)
        followed = random.choice(users)
        
        # 不能关注自己
        if follower['objectId'] == followed['objectId']:
            continue
            
        # 检查是否已经存在这个关注关系
        relationship_key = (follower['objectId'], followed['objectId'])
        if relationship_key in existing_relationships:
            continue
            
        existing_relationships.add(relationship_key)
        
        # 使用关注接口
        response = make_request('POST', f"{API_ENDPOINTS['relationships']}/{follower['objectId']}/follow/{followed['objectId']}")
        if response and response.status_code == 200:
            print(f"✅ 创建关注关系 {len(existing_relationships)}: {follower['username']} -> {followed['username']}")
        else:
            print(f"❌ 创建关注关系失败")
    
    print(f"✅ 成功创建 {len(existing_relationships)} 个关注关系")

def create_replies(users, posts, count=30):
    """创建评论测试数据"""
    print(f"正在创建 {count} 个评论...")
    
    reply_contents = [
        "太厉害了！", "学到了，谢谢分享！", "这个方法很实用", "我也要试试",
        "赞一个！", "很有用的技巧", "感谢分享", "学到了新知识",
        "太棒了！", "这个方法不错", "很有帮助", "谢谢楼主",
        "学到了！", "很实用的方法", "赞！", "感谢分享经验",
        "太厉害了！", "这个方法很好", "学到了新技巧", "谢谢分享",
        "很棒！", "很实用的分享", "学到了", "感谢楼主",
        "太棒了！", "这个方法很赞", "很有用", "谢谢分享",
        "学到了！", "很实用的技巧", "赞一个", "感谢分享",
        "太厉害了！", "这个方法不错", "很有帮助", "谢谢楼主"
    ]
    
    for i in range(count):
        if not users or not posts:
            print("❌ 没有用户或帖子数据，无法创建评论")
            break
            
        user = random.choice(users)
        post = random.choice(posts)
        
        # 随机决定是一级评论还是二级评论
        is_first_level = random.choice([True, True, True, False])
        
        reply_data = {
            'post': post['objectId'],
            'user': user['objectId'],
            'content': random.choice(reply_contents),
            'parent': None,
            'recipient': None
        }
        
        response = make_request('POST', f"{API_ENDPOINTS['replies']}/", reply_data)
        if response and response.status_code == 201:
            print(f"✅ 创建评论 {i+1}: {reply_data['content']}")
        else:
            print(f"❌ 创建评论 {i+1} 失败")
    
    print(f"✅ 评论创建完成")

def create_likes(users, posts, count=30):
    """创建点赞测试数据"""
    print(f"正在创建 {count} 个点赞...")
    
    existing_likes = set()
    
    for i in range(count):
        if not users or not posts:
            print("❌ 没有用户或帖子数据，无法创建点赞")
            break
            
        user = random.choice(users)
        post = random.choice(posts)
        
        # 检查是否已经点赞过这个帖子
        like_key = (post['objectId'], user['objectId'])
        if like_key in existing_likes:
            continue
            
        existing_likes.add(like_key)
        
        # 使用点赞接口
        like_data = {'user_id': user['objectId']}
        response = make_request('POST', f"{API_ENDPOINTS['likes']}/{post['objectId']}/like", like_data)
        if response and response.status_code == 200:
            print(f"✅ 创建点赞 {len(existing_likes)}: {user['username']} -> 帖子")
        else:
            print(f"❌ 创建点赞失败")
    
    print(f"✅ 成功创建 {len(existing_likes)} 个点赞")

def create_banners(count=30):
    """创建横幅测试数据"""
    print(f"正在创建 {count} 个横幅...")
    
    banner_titles = [
        "数学速算挑战赛", "新用户福利", "限时优惠活动", "学习资料下载",
        "数学竞赛报名", "速算技巧分享", "学习计划制定", "数学游戏推荐",
        "心算训练营", "计算能力测试", "数学公式大全", "速算比赛",
        "学习成就展示", "数学知识科普", "速算技巧进阶", "学习社区",
        "数学工具推荐", "速算练习计划", "学习心得分享", "数学竞赛",
        "新功能上线", "用户反馈收集", "学习资源更新", "数学挑战",
        "速算达人榜", "学习进度跟踪", "数学游戏", "速算技巧",
        "学习计划", "数学竞赛"
    ]
    
    banner_contents = [
        "参与数学速算挑战，提升计算能力！",
        "新用户注册即送学习大礼包！",
        "限时优惠，不要错过！",
        "免费下载优质学习资料。",
        "数学竞赛火热报名中！",
        "分享速算技巧，共同进步。",
        "制定专属学习计划。",
        "推荐有趣的数学游戏。",
        "心算训练营开课啦！",
        "测试你的计算能力。",
        "数学公式大全免费查看。",
        "速算比赛等你来挑战！",
        "展示你的学习成就。",
        "数学知识科普文章。",
        "速算技巧进阶教程。",
        "加入学习社区交流。",
        "推荐实用的数学工具。",
        "制定速算练习计划。",
        "分享学习心得经验。",
        "数学竞赛报名进行中。",
        "新功能上线，快来体验！",
        "收集用户反馈意见。",
        "学习资源持续更新。",
        "数学挑战等你来战！",
        "速算达人排行榜。",
        "跟踪学习进度。",
        "有趣的数学游戏。",
        "实用的速算技巧。",
        "个性化学习计划。",
        "精彩数学竞赛。"
    ]
    
    for i in range(count):
        banner_data = {
            'title': random.choice(banner_titles),
            'show': random.choice([True, True, True, False]),
            'click': random.choice([True, True, False]),
            'content': random.choice(banner_contents),
            'action': random.choice(['url', 'page', 'modal', 'download', 'none']),
            'imageurl': f"https://picsum.photos/800/400?random={i}",
            'sort_order': random.randint(0, 100)
        }
        
        response = make_request('POST', f"{API_ENDPOINTS['banners']}/", banner_data)
        if response and response.status_code == 201:
            print(f"✅ 创建横幅 {i+1}: {banner_data['title']}")
        else:
            print(f"❌ 创建横幅 {i+1} 失败")
    
    print(f"✅ 横幅创建完成")

def create_releases(count=30):
    """创建应用发布版本测试数据"""
    print(f"正在创建 {count} 个应用发布版本...")
    
    version_names = [
        "1.0.0", "1.0.1", "1.0.2", "1.1.0", "1.1.1", "1.1.2",
        "1.2.0", "1.2.1", "1.2.2", "1.3.0", "1.3.1", "1.3.2",
        "2.0.0", "2.0.1", "2.0.2", "2.1.0", "2.1.1", "2.1.2",
        "2.2.0", "2.2.1", "2.2.2", "2.3.0", "2.3.1", "2.3.2",
        "3.0.0", "3.0.1", "3.0.2", "3.1.0", "3.1.1", "3.1.2"
    ]
    
    environments = ["测试", "taptap", "正式", "内测", "公测"]
    
    update_contents = [
        "修复已知问题，提升稳定性",
        "新增数学速算功能",
        "优化用户界面，提升体验",
        "修复计算错误问题",
        "新增心算挑战模式",
        "优化性能，提升响应速度",
        "新增学习进度跟踪",
        "修复登录问题",
        "新增数学竞赛功能",
        "优化数据同步机制",
        "新增个性化学习计划",
        "修复界面显示问题",
        "新增速算技巧分享",
        "优化内存使用",
        "新增学习成就系统",
        "修复网络连接问题",
        "新增数学公式查询",
        "优化用户体验",
        "新增学习社区功能",
        "修复数据统计问题",
        "新增离线练习模式",
        "优化界面布局",
        "新增学习提醒功能",
        "修复崩溃问题",
        "新增数学游戏",
        "优化计算算法",
        "新增学习报告",
        "修复同步问题",
        "新增主题切换",
        "优化启动速度"
    ]
    
    for i in range(count):
        release_data = {
            'title': '超级速算',
            'version_name': random.choice(version_names),
            'version_code': random.randint(100, 999),
            'content': random.choice(update_contents),
            'download_url': f"https://example.com/download/app_v{random.choice(version_names)}.apk",
            'environment': random.choice(environments),
            'is_test': random.choice([True, False, False, False]),
            'is_update': random.choice([True, True, False]),
            'force_update': random.choice([True, False, False, False])
        }
        
        response = make_request('POST', f"{API_ENDPOINTS['releases']}/", release_data)
        if response and response.status_code == 201:
            print(f"✅ 创建应用版本 {i+1}: {release_data['version_name']}")
        else:
            print(f"❌ 创建应用版本 {i+1} 失败")
    
    print(f"✅ 应用版本创建完成")

def create_images(count=30):
    """创建图片测试数据"""
    print(f"正在创建 {count} 个图片记录...")
    
    for i in range(count):
        image_data = {
            'fileName': f'test_image_{i+1:03d}.jpg',
            'path': f'/uploads/images/test_image_{i+1:03d}.jpg',
            'url': f'https://example.com/uploads/images/test_image_{i+1:03d}.jpg',
            'fileSize': random.randint(10000, 1000000)
        }
        
        response = make_request('POST', f"{API_ENDPOINTS['images']}/", image_data)
        if response and response.status_code == 201:
            print(f"✅ 创建图片记录 {i+1}: {image_data['fileName']}")
        else:
            print(f"❌ 创建图片记录 {i+1} 失败")
    
    print(f"✅ 图片记录创建完成")

def check_server_status():
    """检查服务器状态"""
    print("🔍 检查服务器状态...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response and response.status_code == 200:
            print("✅ 服务器运行正常")
            return True
        else:
            print("❌ 服务器未运行或无法访问")
            print("💡 请先启动服务器: python start_development.py")
            return False
    except Exception as e:
        print(f"❌ 服务器连接失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始使用API接口创建测试数据...")
    print("=" * 50)
    
    # 检查服务器状态
    if not check_server_status():
        return
    
    # 创建测试数据
    users = create_users(30)
    create_charts(users, 30)
    posts = create_posts(users, 30)
    create_history(users, 30)
    create_relationships(users, 30)
    create_replies(users, posts, 30)
    create_likes(users, posts, 30)
    create_banners(30)
    create_releases(30)
    create_images(30)
    
    print("=" * 50)
    print("🎉 所有测试数据创建完成！")
    print("=" * 50)

if __name__ == '__main__':
    main()
