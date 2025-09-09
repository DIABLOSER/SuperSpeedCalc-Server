from flask import jsonify, request
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import Posts, MyUser, Likes
from sqlalchemy import desc

def get_post_likers(post_id):
    """获取点赞某帖子的用户列表"""
    try:
        # 检查帖子是否存在
        post = Posts.query.get_or_404(post_id)
        
        # 分页参数
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 20, 1), 100)
        
        # 当前查看用户ID（用于权限控制）
        viewer_id = request.args.get('viewer_id')
        
        # 检查帖子是否可见
        if not post.is_visible_to_user(viewer_id):
            return internal_error_response(message='Post not visible or not approved', code=403)
        
        # 查询点赞用户
        query = Likes.query.filter_by(post=post_id).order_by(desc(Likes.createdAt))
        query = query.join(MyUser, Likes.user == MyUser.objectId)
        
        total = query.count()
        likes = query.limit(per_page).offset((page - 1) * per_page).all()
        pages = (total + per_page - 1) // per_page if per_page else 1
        
        return success_response(
            data={
                'post': {
                    'objectId': post.objectId,
                    'content_preview': post.content[:50] + '...' if len(post.content) > 50 else post.content,
                    'likeCount': post.likeCount
                },
                'likers': [
                    {
                        'like_id': like.objectId,
                        'user_data': like.user_ref.to_dict(include_stats=False) if like.user_ref else None,
                        'liked_at': like.createdAt.isoformat(),
                        # 兼容旧版本
                        'user': {
                            'objectId': like.user_ref.objectId,
                            'username': like.user_ref.username,
                            'avatar': like.user_ref.avatar
                        } if like.user_ref else None
                    }
                    for like in likes
                ],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages
                }
            },
            message='获取帖子点赞列表成功'
        )
        
    except Exception as e:
        return internal_error_response(message=str(e), code=500)

def get_user_liked_posts(user_id):
    """获取用户点赞的帖子列表"""
    try:
        # 检查用户是否存在
        user = MyUser.query.get_or_404(user_id)
        
        # 分页参数
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 20, 1), 100)
        
        # 当前查看用户ID（用于权限控制）
        viewer_id = request.args.get('viewer_id')
        
        # 查询用户点赞的帖子
        query = Likes.query.filter_by(user=user_id).order_by(desc(Likes.createdAt))
        query = query.join(Posts, Likes.post == Posts.objectId)
        
        # 如果不是本人查看，只显示公开且已审核的帖子
        if viewer_id != user_id:
            query = query.filter(
                Posts.visible == True,
                Posts.audit_state == 'approved'
            )
        
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
                'liked_posts': [
                    {
                        'like_id': like.objectId,
                        'post_data': like.post_ref.to_dict(include_author=True, user_id=viewer_id, include_full_author=True),
                        'liked_at': like.createdAt.isoformat(),
                        # 兼容旧版本
                        'post': like.post_ref.to_dict(include_author=True, user_id=viewer_id, include_full_author=False)
                    }
                    for like in likes
                ],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages
                }
            },
            message='获取用户点赞帖子列表成功'
        )
        
    except Exception as e:
        return internal_error_response(message=str(e), code=500)

def sync_all_post_like_counts():
    """同步所有帖子的点赞数量（管理员工具）"""
    try:
        # 这是一个管理员工具函数，用于修复数据不一致问题
        admin_user_id = request.args.get('admin_user_id')
        if admin_user_id:
            admin_user = MyUser.query.get(admin_user_id)
            if not admin_user or not admin_user.admin:
                return internal_error_response(message='Permission denied. Admin access required.', code=403)
        
        # 获取所有帖子
        posts = Posts.query.all()
        updated_count = 0
        
        for post in posts:
            if post.sync_like_count():
                updated_count += 1
        
        # 批量提交更改
        from models import db
        db.session.commit()
        
        return success_response(
            data={
                'total_posts': len(posts),
                'updated_posts': updated_count,
                'admin_user': admin_user_id
            },
            message=f'Synchronized like counts for {updated_count} posts'
        )
        
    except Exception as e:
        from models import db
        db.session.rollback()
        return internal_error_response(message=str(e), code=500)
