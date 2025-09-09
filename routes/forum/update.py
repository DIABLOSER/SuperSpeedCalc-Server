from flask import request, jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, Forum
from datetime import datetime

def update_forum_post(object_id):
    """更新社区帖子"""
    try:
        post = Forum.query.get_or_404(object_id)
        data = request.get_json()
        
        # 更新允许的字段
        allowed_fields = ['content', 'category', 'tags', 'public', 'images', 'isPinned', 'isClosed']
        for field in allowed_fields:
            if field in data:
                setattr(post, field, data[field])
        
        post.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return success_response(data=post.to_dict(include_user=True))
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500)

def like_forum_post(object_id):
    """给社区帖子点赞"""
    try:
        post = Forum.query.get_or_404(object_id)
        
        # 增加点赞数
        post.likeCount += 1
        post.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return success_response(
            data=post.to_dict(include_user=True),
            message='Post liked successfully'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500) 