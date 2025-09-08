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
            return jsonify({'error': '历史记录不存在'}), 404
        
        db.session.delete(history)
        db.session.commit()
        
        return jsonify({
            'message': '历史记录删除成功'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'删除历史记录失败: {str(e)}'}), 500
