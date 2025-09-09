from flask import request, jsonify
from models import db, History, MyUser
from datetime import datetime
from utils.response import (
    created_response, bad_request_response, internal_error_response,
    not_found_response
)

def create_history():
    """创建历史记录"""
    try:
        data = request.get_json()
        
        # 验证必需字段
        if not data:
            return bad_request_response(
                message='请求数据不能为空',
                # error_code='EMPTY_REQUEST_DATA'
            )
        
        title = data.get('title')
        score = data.get('score')
        user = data.get('user')
        
        if not title:
            return bad_request_response(
                message='标题不能为空',
                # error_code='MISSING_TITLE'
            )
        
        if score is None:
            return bad_request_response(
                message='分数不能为空',
                # error_code='MISSING_SCORE'
            )
        
        if not user:
            return bad_request_response(
                message='用户ID不能为空',
                # error_code='MISSING_USER_ID'
            )
        
        # 验证用户是否存在
        user_obj = MyUser.query.get(user)
        if not user_obj:
            return not_found_response(
                message='用户不存在',
                # error_code='USER_NOT_FOUND'
            )
        
        # 验证score是否为整数
        try:
            score = int(score)
        except (ValueError, TypeError):
            return bad_request_response(
                message='分数必须是整数',
                # error_code='INVALID_SCORE_FORMAT'
            )
        
        # 创建历史记录
        history = History(
            title=title,
            score=score,
            user=user
        )
        
        db.session.add(history)
        db.session.commit()
        
        return created_response(
            data=history.to_dict(),
            message='历史记录创建成功'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(
            message="创建历史记录失败",
            # error_code="HISTORY_CREATION_FAILED"
        )
