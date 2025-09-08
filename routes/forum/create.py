from flask import request, jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, Forum, MyUser

def create_forum_post():
    """创建新的社区帖子"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['content', 'user']
        for field in required_fields:
            if field not in data:
                return bad_request_response(
                    message=f'{field} is required',
                    error_code='MISSING_REQUIRED_FIELD',
                    details={'field': field}
                )
        
        # 验证作者是否存在
        author = MyUser.query.get(data['user'])
        if not author:
            return not_found_response(
                message='作者不存在',
                error_code='AUTHOR_NOT_FOUND'
            )
        
        # 创建新帖子
        post = Forum(
            content=data['content'],
            category=data.get('category'),
            tags=data.get('tags', []),
            public=data.get('public', True),
            images=data.get('images', []),
            user=data['user']
        )
        
        db.session.add(post)
        db.session.commit()
        
        return success_response(data=post.to_dict(include_user=True)
        ), 201
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500) 