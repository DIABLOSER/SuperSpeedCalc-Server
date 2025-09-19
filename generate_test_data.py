#!/usr/bin/env python3
"""
测试数据生成脚本
为每个表生成30条测试数据，方便开发和测试
"""

import os
import sys
import random
import hashlib
from datetime import datetime, date, timedelta
from faker import Faker

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db
from models.user import MyUser
from models.chart import Charts
from models.posts import Posts
from models.history import History
from models.relationship import UserRelationship
from models.reply import Reply
from models.likes import Likes
from models.banner import Banner
from models.releases import AppRelease
from models.image import Image

# 初始化Faker
fake = Faker('zh_CN')  # 使用中文数据

def generate_users(count=30):
    """生成用户测试数据"""
    print(f"正在生成 {count} 个用户...")
    users = []
    
    for i in range(count):
        # 生成用户名，确保唯一性
        username = f"test_user_{i+1:02d}"
        
        # 生成手机号
        mobile = f"138{random.randint(10000000, 99999999)}"
        
        # 生成密码（简单加密）
        password = hashlib.md5(f"password{i+1}".encode()).hexdigest()
        
        # 生成头像URL
        avatar = f"https://api.dicebear.com/7.x/avataaars/svg?seed={username}"
        
        # 生成个人简介
        bio = fake.sentence(nb_words=random.randint(5, 15))
        
        # 生成经验值和菠萝数量
        experience = random.randint(0, 10000)
        boluo = random.randint(0, 1000)
        
        # 生成生日
        birthday = fake.date_of_birth(minimum_age=18, maximum_age=60)
        
        user = MyUser(
            username=username,
            mobile=mobile,
            password=password,
            avatar=avatar,
            bio=bio,
            experience=experience,
            boluo=boluo,
            isActive=random.choice([True, True, True, False]),  # 大部分用户是活跃的
            admin=random.choice([True, False, False, False, False]),  # 少数管理员
            sex=random.choice([0, 1])
        )
        user.birthday = birthday
        
        users.append(user)
        db.session.add(user)
    
    db.session.commit()
    print(f"✅ 成功生成 {count} 个用户")
    return users

def generate_charts(users, count=30):
    """生成图表测试数据"""
    print(f"正在生成 {count} 个图表...")
    
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
        user = random.choice(users)
        title = random.choice(chart_titles)
        achievement = round(random.uniform(0.0, 100.0), 2)
        
        chart = Charts(
            title=title,
            achievement=achievement,
            user=user.objectId
        )
        
        db.session.add(chart)
    
    db.session.commit()
    print(f"✅ 成功生成 {count} 个图表")

def generate_posts(users, count=30):
    """生成帖子测试数据"""
    print(f"正在生成 {count} 个帖子...")
    
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
        user = random.choice(users)
        content = random.choice(post_contents)
        
        # 随机生成图片列表
        images = []
        if random.choice([True, False]):  # 50%概率有图片
            image_count = random.randint(1, 3)
            for j in range(image_count):
                images.append(f"https://picsum.photos/400/300?random={i*10+j}")
        
        post = Posts(
            user=user.objectId,
            content=content,
            visible=random.choice([True, True, True, False]),  # 大部分公开
            audit_state=random.choice(['approved', 'approved', 'approved', 'pending']),  # 大部分已审核
            images=images,
            likeCount=random.randint(0, 50),
            replyCount=random.randint(0, 20)
        )
        
        db.session.add(post)
    
    db.session.commit()
    print(f"✅ 成功生成 {count} 个帖子")

def generate_history(users, count=30):
    """生成历史记录测试数据"""
    print(f"正在生成 {count} 个历史记录...")
    
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
        user = random.choice(users)
        title = random.choice(history_titles)
        score = random.randint(-50, 100)  # 分数可以是负数
        
        history = History(
            title=title,
            score=score,
            user=user.objectId
        )
        
        db.session.add(history)
    
    db.session.commit()
    print(f"✅ 成功生成 {count} 个历史记录")

def generate_relationships(users, count=30):
    """生成用户关注关系测试数据"""
    print(f"正在生成 {count} 个关注关系...")
    
    # 确保不会重复关注
    existing_relationships = set()
    
    for i in range(count):
        follower = random.choice(users)
        followed = random.choice(users)
        
        # 不能关注自己
        if follower.objectId == followed.objectId:
            continue
            
        # 检查是否已经存在这个关注关系
        relationship_key = (follower.objectId, followed.objectId)
        if relationship_key in existing_relationships:
            continue
            
        existing_relationships.add(relationship_key)
        
        relationship = UserRelationship(
            follower=follower.objectId,
            followed=followed.objectId
        )
        
        db.session.add(relationship)
    
    db.session.commit()
    print(f"✅ 成功生成 {len(existing_relationships)} 个关注关系")

def generate_replies(users, posts, count=30):
    """生成评论测试数据"""
    print(f"正在生成 {count} 个评论...")
    
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
        user = random.choice(users)
        post = random.choice(posts)
        content = random.choice(reply_contents)
        
        # 随机决定是一级评论还是二级评论
        is_first_level = random.choice([True, True, True, False])  # 75%是一级评论
        
        if is_first_level:
            # 一级评论
            reply = Reply(
                post=post.objectId,
                user=user.objectId,
                content=content,
                recipient=None,
                parent=None
            )
        else:
            # 二级评论，需要找到该帖子的一级评论作为父评论
            first_level_replies = Reply.query.filter_by(post=post.objectId, parent=None).all()
            if first_level_replies:
                parent_reply = random.choice(first_level_replies)
                recipient = parent_reply.user
                
                reply = Reply(
                    post=post.objectId,
                    user=user.objectId,
                    content=content,
                    recipient=recipient,
                    parent=parent_reply.objectId
                )
            else:
                # 如果没有一级评论，就创建一级评论
                reply = Reply(
                    post=post.objectId,
                    user=user.objectId,
                    content=content,
                    recipient=None,
                    parent=None
                )
        
        db.session.add(reply)
    
    db.session.commit()
    print(f"✅ 成功生成 {count} 个评论")

def generate_likes(users, posts, count=30):
    """生成点赞测试数据"""
    print(f"正在生成 {count} 个点赞...")
    
    # 确保不会重复点赞
    existing_likes = set()
    
    for i in range(count):
        user = random.choice(users)
        post = random.choice(posts)
        
        # 检查是否已经点赞过这个帖子
        like_key = (post.objectId, user.objectId)
        if like_key in existing_likes:
            continue
            
        existing_likes.add(like_key)
        
        like = Likes(
            post=post.objectId,
            user=user.objectId
        )
        
        db.session.add(like)
    
    db.session.commit()
    print(f"✅ 成功生成 {len(existing_likes)} 个点赞")

def generate_banners(count=30):
    """生成横幅测试数据"""
    print(f"正在生成 {count} 个横幅...")
    
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
        title = random.choice(banner_titles)
        content = random.choice(banner_contents)
        
        banner = Banner(
            title=title,
            show=random.choice([True, True, True, False]),  # 大部分显示
            click=random.choice([True, True, False]),  # 大部分可点击
            content=content,
            action=random.choice(['url', 'page', 'modal', 'download', 'none']),
            imageurl=f"https://picsum.photos/800/400?random={i}",
            sort_order=random.randint(0, 100)
        )
        
        db.session.add(banner)
    
    db.session.commit()
    print(f"✅ 成功生成 {count} 个横幅")

def generate_releases(count=30):
    """生成应用发布版本测试数据"""
    print(f"正在生成 {count} 个应用发布版本...")
    
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
        version_name = random.choice(version_names)
        version_code = random.randint(100, 999)
        content = random.choice(update_contents)
        environment = random.choice(environments)
        
        release = AppRelease(
            title="超级速算",
            version_name=version_name,
            version_code=version_code,
            content=content,
            download_url=f"https://example.com/download/app_v{version_name}.apk",
            environment=environment,
            is_test=random.choice([True, False, False, False]),  # 25%是测试版本
            is_update=random.choice([True, True, False]),  # 大部分需要更新
            force_update=random.choice([True, False, False, False])  # 25%强制更新
        )
        
        db.session.add(release)
    
    db.session.commit()
    print(f"✅ 成功生成 {count} 个应用发布版本")

def generate_images(count=30):
    """生成图片测试数据"""
    print(f"正在生成 {count} 个图片记录...")
    
    for i in range(count):
        filename = f"test_image_{i+1:03d}.jpg"
        path = f"/uploads/images/{filename}"
        url = f"https://example.com/uploads/images/{filename}"
        file_size = random.randint(10000, 1000000)  # 10KB到1MB
        
        image = Image(
            fileName=filename,
            path=path,
            url=url,
            fileSize=file_size
        )
        
        db.session.add(image)
    
    db.session.commit()
    print(f"✅ 成功生成 {count} 个图片记录")

def main():
    """主函数"""
    print("🚀 开始生成测试数据...")
    print("=" * 50)
    
    # 创建应用实例
    app = create_app('development')
    
    # 临时禁用日志配置以避免权限问题
    app.logger.disabled = True
    
    with app.app_context():
        # 清空现有数据（可选）
        print("⚠️  正在清空现有数据...")
        db.drop_all()
        db.create_all()
        print("✅ 数据库已重置")
        
        # 生成测试数据
        users = generate_users(30)
        generate_charts(users, 30)
        posts = generate_posts(users, 30)
        generate_history(users, 30)
        generate_relationships(users, 30)
        generate_replies(users, posts, 30)
        generate_likes(users, posts, 30)
        generate_banners(30)
        generate_releases(30)
        generate_images(30)
        
        print("=" * 50)
        print("🎉 所有测试数据生成完成！")
        print(f"📊 数据统计：")
        print(f"   - 用户: {MyUser.query.count()} 个")
        print(f"   - 图表: {Charts.query.count()} 个")
        print(f"   - 帖子: {Posts.query.count()} 个")
        print(f"   - 历史记录: {History.query.count()} 个")
        print(f"   - 关注关系: {UserRelationship.query.count()} 个")
        print(f"   - 评论: {Reply.query.count()} 个")
        print(f"   - 点赞: {Likes.query.count()} 个")
        print(f"   - 横幅: {Banner.query.count()} 个")
        print(f"   - 应用版本: {AppRelease.query.count()} 个")
        print(f"   - 图片: {Image.query.count()} 个")
        print("=" * 50)

if __name__ == '__main__':
    main()
