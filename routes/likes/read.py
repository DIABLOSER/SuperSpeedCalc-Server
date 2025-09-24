from flask import request
from models import Posts, MyUser, Likes
from sqlalchemy import desc
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response
)

def get_post_likers(post_id):
    """获取帖子点赞用户列表"""
    try:
        # 验证帖子是否存在
        post = Posts.query.get(post_id)
        if not post:
            return not_found_response(message="帖子不存在")
        
        # 分页参数
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 20, 1), 100)
        
        # 获取点赞记录
        query = Likes.query.filter_by(post=post_id)
        query = query.order_by(desc(Likes.createdAt))
        
        total = query.count()
        likes = query.limit(per_page).offset((page - 1) * per_page).all()
        pages = (total + per_page - 1) // per_page if per_page else 1
        
        return success_response(
            data={
                'post': {
                    'objectId': post.objectId,
                    'content_preview': post.content[:50] + '...' if len(post.content) > 50 else post.content,
                    'likeCount': post.get_actual_like_count()
                },
                'likers': [like.to_dict(include_full_post=False, include_full_user=True) for like in likes],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages,
                    'has_next': page < pages,
                    'has_prev': page > 1
                }
            },
            message="获取帖子点赞列表成功"
        )
        
    except Exception as e:
        return internal_error_response(
            message="获取帖子点赞列表失败"
        )

def get_user_liked_posts(user_id):
    """获取用户点赞的帖子列表"""
    try:
        # 验证用户是否存在
        user = MyUser.query.get(user_id)
        if not user:
            return not_found_response(message="用户不存在")
        
        # 分页参数
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 20, 1), 100)
        
        # 获取用户点赞的帖子
        query = Likes.query.filter_by(user=user_id)
        query = query.order_by(desc(Likes.createdAt))
        
        total = query.count()
        likes = query.limit(per_page).offset((page - 1) * per_page).all()
        pages = (total + per_page - 1) // per_page if per_page else 1
        
        return success_response(
            data={
                'user': {
                    'objectId': user.objectId,
                    'username': user.username,
                    'avatar': user.avatar
                },
                'liked_posts': [like.to_dict(include_full_post=True, include_full_user=False) for like in likes],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages,
                    'has_next': page < pages,
                    'has_prev': page > 1
                }
            },
            message="获取用户点赞帖子列表成功"
        )
        
    except Exception as e:
        return internal_error_response(
            message="获取用户点赞帖子列表失败"
        )

def get_like_status(user_id, post_id):
    """检查用户是否点赞了指定帖子"""
    try:
        # 验证帖子是否存在
        post = Posts.query.get(post_id)
        if not post:
            return not_found_response(message="帖子不存在")
        
        # 验证用户是否存在
        user = MyUser.query.get(user_id)
        if not user:
            return not_found_response(message="用户不存在")
        
        # 检查点赞状态
        is_liked = Likes.is_user_liked_post(post_id, user_id)
        
        return success_response(
            data={
                'post_id': post_id,
                'user_id': user_id,
                'is_liked': is_liked,
                'like_count': post.get_actual_like_count()
            },
            message="获取点赞状态成功"
        )
        
    except Exception as e:
        return internal_error_response(
            message="获取点赞状态失败"
        )

def sync_all_post_like_counts():
    """同步所有帖子的点赞数（管理员功能）"""
    try:
        # 获取请求数据
        data = request.get_json() or {}
        admin_user_id = data.get('admin_user_id')
        
        # 验证管理员用户（可选）
        if admin_user_id:
            admin_user = MyUser.query.get(admin_user_id)
            if not admin_user:
                return not_found_response(message="管理员用户不存在")
        
        # 获取所有帖子
        posts = Posts.query.all()
        updated_count = 0
        
        for post in posts:
            # 获取实际点赞数
            actual_like_count = Likes.get_post_like_count(post.objectId)
            
            # 如果数量不一致，则更新
            if post.likeCount != actual_like_count:
                post.likeCount = actual_like_count
                updated_count += 1
        
        # 提交更改
        from models import db
        db.session.commit()
        
        return success_response(
            data={
                'total_posts': len(posts),
                'updated_posts': updated_count,
                'admin_user': admin_user_id
            },
            message=f"同步完成，更新了 {updated_count} 个帖子的点赞数"
        )
        
    except Exception as e:
        from models import db
        db.session.rollback()
        return internal_error_response(
            message="同步点赞数失败"
        )
