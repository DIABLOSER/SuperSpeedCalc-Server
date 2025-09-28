from flask import request
from utils.response import (
    success_response, internal_error_response,
    not_found_response, bad_request_response
)
from models import db, Posts, MyUser, Collect
from datetime import datetime

def create_collect():
    """收藏帖子"""
    try:
        data = request.get_json()
        
        post_id = data.get('post_id')
        user_id = data.get('user_id')
        
        if not post_id or not user_id:
            return bad_request_response(message='post_id and user_id are required')
        
        # 验证帖子是否存在
        post = Posts.query.get(post_id)
        if not post:
            return not_found_response(message="帖子不存在")
        
        # 验证用户是否存在
        user = MyUser.query.get(user_id)
        if not user:
            return not_found_response(message="用户不存在")
        
        # 检查是否已经收藏
        existing_collect = Collect.query.filter_by(post=post_id, user=user_id).first()
        if existing_collect:
            return bad_request_response(message='用户已经收藏过此帖子')
        
        # 创建收藏记录
        collect_record = Collect(post=post_id, user=user_id)
        db.session.add(collect_record)
        
        db.session.commit()
        
        return success_response(
            data={
                'post_id': post.objectId,
                'user_id': user_id,
                'collect_id': collect_record.objectId,
                'is_collected_by_user': True
            },
            message='收藏成功'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=f'收藏失败: {str(e)}')
