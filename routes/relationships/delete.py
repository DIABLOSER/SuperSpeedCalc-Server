from flask import request
from utils.response import (
    success_response, internal_error_response,
    not_found_response, bad_request_response
)
from models import db, MyUser, UserRelationship

def unfollow_user():
    """用户取消关注另一个用户 - 新的路由设计"""
    try:
        # 从请求体获取参数
        data = request.get_json() or {}
        user_id = data.get('user_id')
        target_user_id = data.get('target_user_id')
        
        if not user_id or not target_user_id:
            return bad_request_response(message='user_id and target_user_id are required')
        
        # 检查用户是否存在
        user = MyUser.query.get(user_id)
        if not user:
            return not_found_response(message="关注者用户不存在")
            
        target_user = MyUser.query.get(target_user_id)
        if not target_user:
            return not_found_response(message="被关注者用户不存在")
        
        # 检查是否尝试取消关注自己
        if user_id == target_user_id:
            return bad_request_response(message='Cannot unfollow yourself')
        
        # 查找关注关系
        relationship = UserRelationship.query.filter_by(
            follower=user_id,
            followed=target_user_id
        ).first()
        
        if not relationship:
            return bad_request_response(message='Not following this user')
        
        # 删除关注关系
        db.session.delete(relationship)
        db.session.commit()
        
        return success_response(
            data={
                'follower': {
                    'objectId': user.objectId,
                    'username': user.username
                },
                'unfollowed': {
                    'objectId': target_user.objectId,
                    'username': target_user.username
                }
            },
            message=f'{user.username} has unfollowed {target_user.username}'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500)
