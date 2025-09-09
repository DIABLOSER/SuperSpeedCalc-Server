from flask import jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, MyUser, UserRelationship
from datetime import datetime

def follow_user(user_id, target_user_id):
    """用户关注另一个用户"""
    try:
        # 检查用户是否存在
        user = MyUser.query.get_or_404(user_id)
        target_user = MyUser.query.get_or_404(target_user_id)
        
        # 检查是否尝试关注自己
        if user_id == target_user_id:
            return internal_error_response(message='Cannot follow yourself'
            , code=400)
        
        # 检查是否已经关注
        existing_relationship = UserRelationship.query.filter_by(
            follower=user_id,
            followed=target_user_id
        ).first()
        
        if existing_relationship:
            return internal_error_response(message='Already following this user'
            , code=400)
        
        # 创建关注关系
        relationship = UserRelationship(
            follower=user_id,
            followed=target_user_id
        )
        
        db.session.add(relationship)
        db.session.commit()
        
        return success_response(
            data={
                'follower': {
                    'objectId': user.objectId,
                    'username': user.username
                },
                'followed': {
                    'objectId': target_user.objectId,
                    'username': target_user.username
                },
                'relationship_id': relationship.objectId,
                'createdAt': relationship.createdAt.isoformat()
            },
            message=f'{user.username} is now following {target_user.username}'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500)
