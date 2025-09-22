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
        post = Posts.query.get(post_id)
        if not post:
            return not_found_response(message='Post not found')
        
        # 记录被删除的帖子信息（用于日志）
        post_info = {
            'post_id': post.objectId,
            'author_id': post.user,
            'content_preview': post.content[:50] + '...' if len(post.content) > 50 else post.content
        }
        
        # 删除帖子
        db.session.delete(post)
        db.session.commit()
        
        return created_response(data=post_info, message='Post deleted successfully')
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500)
