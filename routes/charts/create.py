from flask import request, jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, Charts, MyUser

def create_chart():
    """创建新图表"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['title', 'user']
        for field in required_fields:
            if field not in data:
                return bad_request_response(
                    message=f'{field} is required',
                    error_code='MISSING_REQUIRED_FIELD',
                    details={'field': field}
                )
        
        # 验证用户是否存在
        user = MyUser.query.get(data['user'])
        if not user:
            return not_found_response(
                message='用户不存在',
                error_code='USER_NOT_FOUND'
            )
        
        # 创建新图表
        chart = Charts(
            title=data['title'],
            achievement=data.get('achievement', 0.0),
            user=data['user']
        )
        
        db.session.add(chart)
        db.session.commit()
        
        return success_response(data=chart.to_dict(include_user=True)
        ), 201
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500) 