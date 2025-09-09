from flask import jsonify, request
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import Reply, Posts, MyUser
from sqlalchemy import desc, asc

def get_post_replies(post_id):
    """获取帖子的所有评论（分页、支持层级筛选）"""
    try:
        # 验证帖子是否存在
        post = Posts.query.get_or_404(post_id)
        
        # 分页参数
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 20, 1), 100)
        
        # 层级筛选参数
        level = request.args.get('level', type=int)  # 1=一级评论，2=二级评论，None=所有
        include_children = request.args.get('include_children', 'false').lower() == 'true'
        
        # 当前查看用户ID（用于权限控制）
        viewer_id = request.args.get('viewer_id')
        
        # 检查帖子是否可见
        if not post.is_visible_to_user(viewer_id):
            return internal_error_response(message='Post not visible or not approved'
            , code=403)
        
        # 构建查询
        query = Reply.query.filter_by(post=post_id)
        
        if level == 1:
            # 只获取一级评论
            query = query.filter(Reply.parent.is_(None))
        elif level == 2:
            # 只获取二级评论
            query = query.filter(Reply.parent.isnot(None))
        
        # 排序：一级评论按创建时间排序，二级评论也按创建时间排序
        query = query.order_by(asc(Reply.createdAt))
        
        # 预加载用户信息
        query = query.join(MyUser, Reply.user == MyUser.objectId)
        
        total = query.count()
        replies = query.limit(per_page).offset((page - 1) * per_page).all()
        pages = (total + per_page - 1) // per_page if per_page else 1
        
        return success_response(
            data={
                'post': {
                    'objectId': post.objectId,
                    'content_preview': post.content[:50] + '...' if len(post.content) > 50 else post.content,
                    'replyCount': post.replyCount,
                    'actual_reply_count': post.get_actual_reply_count()
                },
                'replies': [
                    reply.to_dict(include_details=True, include_children=include_children, include_full_post=False) 
                    for reply in replies
                ],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages
                },
                'stats': {
                    'total_replies': post.get_actual_reply_count(),
                    'first_level_count': post.get_first_level_reply_count(),
                    'second_level_count': post.get_second_level_reply_count()
                }
            },
            message='获取帖子回复成功'
        )
        
    except Exception as e:
        return internal_error_response(message=str(e), code=500)

def get_reply(reply_id):
    """获取单个评论详情"""
    try:
        reply = Reply.query.get_or_404(reply_id)
        
        # 当前查看用户ID（用于权限控制）
        viewer_id = request.args.get('viewer_id')
        
        # 检查帖子是否可见
        if not reply.post_ref.is_visible_to_user(viewer_id):
            return internal_error_response(message='Post not visible or not approved'
            , code=403)
        
        include_children = request.args.get('include_children', 'true').lower() == 'true'
        
        include_full_post = request.args.get('include_full_post', 'false').lower() == 'true'
        
        return success_response(data=reply.to_dict(include_details=True, include_children=include_children, include_full_post=include_full_post)
        )
        
    except Exception as e:
        return internal_error_response(message=str(e), code=500)

def get_user_replies(user_id):
    """获取用户的评论列表"""
    try:
        # 验证用户是否存在
        user = MyUser.query.get_or_404(user_id)
        
        # 分页参数
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 20, 1), 100)
        
        # 当前查看用户ID（用于权限控制）
        viewer_id = request.args.get('viewer_id')
        
        # 层级筛选
        level = request.args.get('level', type=int)
        
        query = Reply.query.filter_by(user=user_id)
        
        if level == 1:
            query = query.filter(Reply.parent.is_(None))
        elif level == 2:
            query = query.filter(Reply.parent.isnot(None))
        
        # 如果不是本人查看，只显示公开且已审核帖子的评论
        if viewer_id != user_id:
            query = query.join(Posts, Reply.post == Posts.objectId).filter(
                Posts.visible == True,
                Posts.audit_state == 'approved'
            )
        
        # 按创建时间倒序排列
        query = query.order_by(desc(Reply.createdAt))
        
        total = query.count()
        replies = query.limit(per_page).offset((page - 1) * per_page).all()
        pages = (total + per_page - 1) // per_page if per_page else 1
        
        return success_response(
            data={
                'user': {
                    'objectId': user.objectId,
                    'username': user.username,
                    'avatar': user.avatar
                },
                'replies': [
                    reply.to_dict(include_details=True, include_children=False, include_full_post=True) 
                    for reply in replies
                ],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages
                },
                'stats': {
                    'total_replies': Reply.get_user_reply_count(user_id)
                }
            },
            message='获取用户回复成功'
        )
        
    except Exception as e:
        return internal_error_response(message=str(e), code=500)

def get_first_level_replies(post_id):
    """获取帖子的一级评论（带子评论）"""
    try:
        # 验证帖子是否存在
        post = Posts.query.get_or_404(post_id)
        
        # 分页参数
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 10, 1), 50)  # 一级评论分页数量较少，因为包含子评论
        
        # 当前查看用户ID（用于权限控制）
        viewer_id = request.args.get('viewer_id')
        
        # 检查帖子是否可见
        if not post.is_visible_to_user(viewer_id):
            return internal_error_response(message='Post not visible or not approved'
            , code=403)
        
        # 只获取一级评论
        query = Reply.query.filter_by(post=post_id).filter(Reply.parent.is_(None))
        query = query.order_by(asc(Reply.createdAt))
        query = query.join(MyUser, Reply.user == MyUser.objectId)
        
        total = query.count()
        first_level_replies = query.limit(per_page).offset((page - 1) * per_page).all()
        pages = (total + per_page - 1) // per_page if per_page else 1
        
        return success_response(
            data={
                'post': {
                    'objectId': post.objectId,
                    'content_preview': post.content[:50] + '...' if len(post.content) > 50 else post.content,
                    'replyCount': post.replyCount
                },
                'first_level_replies': [
                    reply.to_dict(include_details=True, include_children=True, include_full_post=False)  # 包含子评论
                    for reply in first_level_replies
                ],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages
                },
                'stats': {
                    'first_level_count': post.get_first_level_reply_count(),
                    'second_level_count': post.get_second_level_reply_count()
                }
            },
            message='获取一级回复成功'
        )
        
    except Exception as e:
        return internal_error_response(message=str(e), code=500)
