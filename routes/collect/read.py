from flask import request
from models import Posts, MyUser, Collect
from sqlalchemy import desc
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response
)

def get_user_collected_posts(user_id):
    """获取用户收藏的帖子列表"""
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
        
        # 获取用户收藏的帖子
        query = Collect.query.filter_by(user=user_id)
        query = query.order_by(desc(Collect.createdAt))
        
        total = query.count()
        collects = query.limit(per_page).offset((page - 1) * per_page).all()
        pages = (total + per_page - 1) // per_page if per_page else 1
        
        return success_response(
            data={
                'user': {
                    'objectId': user.objectId,
                    'username': user.username,
                    'avatar': user.avatar
                },
                'collected_posts': [collect.to_dict(include_full_post=True, include_full_user=False) for collect in collects],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages,
                    'has_next': page < pages,
                    'has_prev': page > 1
                }
            },
            message="获取用户收藏帖子列表成功"
        )
        
    except Exception as e:
        return internal_error_response(
            message="获取用户收藏帖子列表失败"
        )

def get_post_collectors(post_id):
    """获取收藏指定帖子的用户列表"""
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
        
        # 获取收藏记录
        query = Collect.query.filter_by(post=post_id)
        query = query.order_by(desc(Collect.createdAt))
        
        total = query.count()
        collects = query.limit(per_page).offset((page - 1) * per_page).all()
        pages = (total + per_page - 1) // per_page if per_page else 1
        
        return success_response(
            data={
                'post': {
                    'objectId': post.objectId,
                    'content_preview': post.content[:50] + '...' if len(post.content) > 50 else post.content,
                    'collect_count': Collect.get_post_collect_count(post_id)
                },
                'collectors': [collect.to_dict(include_full_post=False, include_full_user=True) for collect in collects],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages,
                    'has_next': page < pages,
                    'has_prev': page > 1
                }
            },
            message="获取帖子收藏用户列表成功"
        )
        
    except Exception as e:
        return internal_error_response(
            message="获取帖子收藏用户列表失败"
        )

def get_collect_status(user_id, post_id):
    """检查用户是否收藏了指定帖子"""
    try:
        # 验证帖子是否存在
        post = Posts.query.get(post_id)
        if not post:
            return not_found_response(message="帖子不存在")
        
        # 验证用户是否存在
        user = MyUser.query.get(user_id)
        if not user:
            return not_found_response(message="用户不存在")
        
        # 检查收藏状态
        is_collected = Collect.is_user_collected_post(post_id, user_id)
        
        # 如果已收藏，获取收藏记录ID
        collect_id = None
        if is_collected:
            collect_record = Collect.query.filter_by(post=post_id, user=user_id).first()
            if collect_record:
                collect_id = collect_record.objectId
        
        return success_response(
            data={
                'post_id': post_id,
                'user_id': user_id,
                'is_collected': is_collected,
                'collect_id': collect_id,
                'collect_count': Collect.get_post_collect_count(post_id)
            },
            message="获取收藏状态成功"
        )
        
    except Exception as e:
        return internal_error_response(
            message="获取收藏状态失败"
        )

def get_user_collect_stats(user_id):
    """获取用户收藏统计信息"""
    try:
        # 验证用户是否存在
        user = MyUser.query.get(user_id)
        if not user:
            return not_found_response(message="用户不存在")
        
        # 获取收藏统计
        collect_count = Collect.get_user_collect_count(user_id)
        
        return success_response(
            data={
                'user': {
                    'objectId': user.objectId,
                    'username': user.username,
                    'avatar': user.avatar
                },
                'collect_count': collect_count
            },
            message="获取用户收藏统计成功"
        )
        
    except Exception as e:
        return internal_error_response(
            message="获取用户收藏统计失败"
        )
