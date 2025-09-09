from flask import jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, MyUser, UserRelationship

def unfollow_user(user_id, target_user_id):
    """用户取消关注另一个用户"""
    try:
        # 检查用户是否存在
        user = MyUser.query.get_or_404(user_id)
        target_user = MyUser.query.get_or_404(target_user_id)
        
        # 检查是否尝试取消关注自己
        if user_id == target_user_id:
            return internal_error_response(message='Cannot unfollow yourself'
            , code=400)
        
        # 查找关注关系
        relationship = UserRelationship.query.filter_by(
            follower=user_id,
            followed=target_user_id
        ).first()
        
        if not relationship:
            return internal_error_response(message='Not following this user'
            , code=400)
        
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
