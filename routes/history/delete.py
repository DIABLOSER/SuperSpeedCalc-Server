from flask import jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, History

def delete_history(object_id):
    """删除历史记录"""
    try:
        history = History.query.get(object_id)
        
        if not history:
            return not_found_response(
                message='历史记录不存在',
                # error_code='HISTORY_NOT_FOUND'
            )
        
        db.session.delete(history)
        db.session.commit()
        
        return deleted_response(message='历史记录删除成功')
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(
            message='删除历史记录失败',
            # error_code='HISTORY_DELETE_FAILED'
        )
