from flask import request, jsonify
from models import db, Posts, MyUser
from datetime import datetime
from utils.response import (
    created_response, bad_request_response, internal_error_response,
    not_found_response
)

def create_post():
    """创建新帖子"""
    try:
        data = request.get_json()
        
        # 检查必需的参数
        user_id = data.get('user')
        content = data.get('content')
        
        if not user_id or not content:
            return bad_request_response(
                message='User ID and content are required',
                error_code='MISSING_REQUIRED_FIELDS'
            )
        
        # 验证用户是否存在
        user = MyUser.query.get(user_id)
        if not user:
            return not_found_response(
                message='User not found',
                error_code='USER_NOT_FOUND'
            )
        
        # 检查内容长度
        if len(content.strip()) == 0:
            return bad_request_response(
                message='Content cannot be empty',
                error_code='EMPTY_CONTENT'
            )
        
        # 创建帖子
        post = Posts(
            user=user_id,
            content=content.strip(),
            visible=data.get('visible', True),
            audit_state=data.get('audit_state', 'pending')
        )
        
        # 处理图片列表
        images = data.get('images', [])
        if isinstance(images, list):
            post.set_images_list(images)
        
        db.session.add(post)
        db.session.commit()
        
        return created_response(
            data=post.to_dict(include_author=True, user_id=user_id),
            message='帖子创建成功'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(
            message="创建帖子失败",
            error_code="POST_CREATION_FAILED",
            details=str(e)
        )
