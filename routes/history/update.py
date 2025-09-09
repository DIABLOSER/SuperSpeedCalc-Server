from flask import request, jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, History

def update_history(object_id):
    """更新历史记录"""
    try:
        history = History.query.get(object_id)
        
        if not history:
            return not_found_response(
                message='历史记录不存在',
                error_code='HISTORY_NOT_FOUND'
            )
        
        data = request.get_json()
        
        if not data:
            return bad_request_response(
                message='请求数据不能为空',
                error_code='EMPTY_REQUEST_DATA'
            )
        
        # 更新字段
        if 'title' in data:
            if not data['title']:
                return bad_request_response(
                    message='标题不能为空',
                    error_code='EMPTY_TITLE'
                )
            history.title = data['title']
        
        if 'score' in data:
            try:
                score = int(data['score'])
                history.score = score
            except (ValueError, TypeError):
                return bad_request_response(
                    message='分数必须是整数',
                    error_code='INVALID_SCORE'
                )
        
        if 'user' in data:
            if not data['user']:
                return bad_request_response(
                    message='用户ID不能为空',
                    error_code='EMPTY_USER_ID'
                )
            history.user = data['user']
        
        db.session.commit()
        
        return updated_response(
            data=history.to_dict(),
            message='历史记录更新成功'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(
            message='更新历史记录失败',
            error_code='HISTORY_UPDATE_FAILED',
            details=str(e)
        )
