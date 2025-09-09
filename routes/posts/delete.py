from flask import request, jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, Posts, MyUser

def delete_post(post_id):
    """删除帖子"""
    try:
        post = Posts.query.get_or_404(post_id)
        data = request.get_json() or {}
        
        user_id = data.get('user_id')  # 当前用户ID
        is_admin = data.get('is_admin', False)  # 是否为管理员操作
        
        if not user_id:
            return internal_error_response(message='User ID is required', code=400)
        
        # 权限检查：作者或管理员可以删除帖子
        if user_id == post.user:
            # 作者删除自己的帖子
            delete_reason = 'Deleted by author'
        elif is_admin:
            # 验证管理员权限
            admin_user = MyUser.query.get(user_id)
            if not admin_user or not admin_user.admin:
                return internal_error_response(message='Permission denied. Admin access required.', code=403)
            delete_reason = f'Deleted by admin: {admin_user.username}'
        else:
            return internal_error_response(message='Permission denied. Only the author or admin can delete this post.', code=403)
        
        # 记录被删除的帖子信息（用于日志）
        post_info = {
            'post_id': post.objectId,
            'author_id': post.user,
            'content_preview': post.content[:50] + '...' if len(post.content) > 50 else post.content,
            'delete_reason': delete_reason,
            'deleted_by': user_id
        }
        
        # 删除帖子
        db.session.delete(post)
        db.session.commit()
        
        return created_response(data=post_info
        , message='Post deleted successfully')
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500)
