from flask import jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, Forum

def delete_forum_post(object_id):
    """删除社区帖子"""
    try:
        post = Forum.query.get_or_404(object_id)
        db.session.delete(post)
        db.session.commit()
        
        return deleted_response(message='Forum post deleted successfully'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500) 