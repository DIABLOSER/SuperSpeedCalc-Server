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
        
        user_id = data.get('user_id', 'anonymous')  # 当前用户ID，默认为匿名
        
        # 移除权限检查，任何人都可以删除帖子
        delete_reason = f'Deleted by user: {user_id}'
        
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
