from flask import jsonify, request
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, MyUser, UserRelationship
from sqlalchemy import or_

def get_user_followers(user_id):
    """获取用户的粉丝列表"""
    try:
        # 检查用户是否存在
        user = MyUser.query.get_or_404(user_id)
        
        # 分页参数
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 20, 1), 100)
        
        # 获取关注此用户的用户列表
        query = MyUser.query.join(
            UserRelationship, MyUser.objectId == UserRelationship.follower
        ).filter(UserRelationship.followed == user_id)
        
        total = query.count()
        followers = query.limit(per_page).offset((page - 1) * per_page).all()
        pages = (total + per_page - 1) // per_page if per_page else 1
        
        return jsonify({
            'success': True,
            'data': {
                'user': {
                    'objectId': user.objectId,
                    'username': user.username,
                    'avatar': user.avatar
                },
                'followers': [
                    {
                        'objectId': follower.objectId,
                        'username': follower.username,
                        'avatar': follower.avatar,
                        'bio': follower.bio
                    }
                    for follower in followers
                ],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages
                }
            }
        })
        
    except Exception as e:
        return internal_error_response(message=str(e), code=500)

def get_user_following(user_id):
    """获取用户关注的用户列表"""
    try:
        # 检查用户是否存在
        user = MyUser.query.get_or_404(user_id)
        
        # 分页参数
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 20, 1), 100)
        
        # 获取此用户关注的用户列表
        query = MyUser.query.join(
            UserRelationship, MyUser.objectId == UserRelationship.followed
        ).filter(UserRelationship.follower == user_id)
        
        total = query.count()
        following = query.limit(per_page).offset((page - 1) * per_page).all()
        pages = (total + per_page - 1) // per_page if per_page else 1
        
        return jsonify({
            'success': True,
            'data': {
                'user': {
                    'objectId': user.objectId,
                    'username': user.username,
                    'avatar': user.avatar
                },
                'following': [
                    {
                        'objectId': followed.objectId,
                        'username': followed.username,
                        'avatar': followed.avatar,
                        'bio': followed.bio
                    }
                    for followed in following
                ],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages
                }
            }
        })
        
    except Exception as e:
        return internal_error_response(message=str(e), code=500)

def check_follow_relationship(user_id, target_user_id):
    """检查用户之间的关注关系"""
    try:
        # 检查用户是否存在
        user = MyUser.query.get_or_404(user_id)
        target_user = MyUser.query.get_or_404(target_user_id)
        
        # 检查是否关注
        is_following = user.is_following(target_user_id)
        is_followed_by = target_user.is_following(user_id)
        
        return jsonify({
            'success': True,
            'data': {
                'user': {
                    'objectId': user.objectId,
                    'username': user.username
                },
                'target_user': {
                    'objectId': target_user.objectId,
                    'username': target_user.username
                },
                'relationship': {
                    'is_following': is_following,  # 当前用户是否关注目标用户
                    'is_followed_by': is_followed_by,  # 当前用户是否被目标用户关注
                    'mutual': is_following and is_followed_by  # 是否互相关注
                }
            }
        })
        
    except Exception as e:
        return internal_error_response(message=str(e), code=500)

def get_mutual_followers(user_id):
    """获取用户的互关列表（相互关注的用户）"""
    try:
        # 检查用户是否存在
        user = MyUser.query.get_or_404(user_id)
        
        # 分页参数
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 20, 1), 100)
        
        # 查询互关用户
        # 方法：查找同时满足以下条件的用户：
        # 1. 用户关注的人（UserRelationship.follower == user_id）
        # 2. 同时这些人也关注该用户（存在反向关系）
        
        # 使用子查询的方式
        # 首先获取用户关注的所有用户ID
        following_subquery = db.session.query(UserRelationship.followed).filter(
            UserRelationship.follower == user_id
        ).subquery()
        
        # 然后在这些用户中找出也关注该用户的用户
        mutual_query = MyUser.query.join(
            UserRelationship, MyUser.objectId == UserRelationship.follower
        ).filter(
            UserRelationship.followed == user_id,  # 这些用户关注当前用户
            MyUser.objectId.in_(following_subquery)  # 且当前用户也关注这些用户
        )
        
        total = mutual_query.count()
        mutual_users = mutual_query.limit(per_page).offset((page - 1) * per_page).all()
        pages = (total + per_page - 1) // per_page if per_page else 1
        
        return jsonify({
            'success': True,
            'data': {
                'user': {
                    'objectId': user.objectId,
                    'username': user.username,
                    'avatar': user.avatar
                },
                'mutual_followers': [
                    {
                        'objectId': mutual_user.objectId,
                        'username': mutual_user.username,
                        'avatar': mutual_user.avatar,
                        'bio': mutual_user.bio,
                        'experience': mutual_user.experience
                    }
                    for mutual_user in mutual_users
                ],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages
                },
                'stats': {
                    'mutual_count': total,
                    'followers_count': user.get_followers_count(),
                    'following_count': user.get_following_count()
                }
            }
        })
        
    except Exception as e:
        return internal_error_response(message=str(e), code=500)
