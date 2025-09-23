from flask import request
from utils.response import (
    success_response, internal_error_response,
    not_found_response, bad_request_response
)
from models import db, Posts, MyUser, Likes
from datetime import datetime

def toggle_like():
    """切换点赞状态（点赞/取消点赞）"""
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
        
        # 检查当前点赞状态
        existing_like = Likes.query.filter_by(post=post_id, user=user_id).first()
        
        if existing_like:
            # 如果已点赞，则取消点赞
            db.session.delete(existing_like)
            post.likeCount = max(0, post.get_actual_like_count() - 1)
            action = "取消点赞"
            is_liked = False
        else:
            # 如果未点赞，则点赞
            like_record = Likes(post=post_id, user=user_id)
            db.session.add(like_record)
            post.likeCount = post.get_actual_like_count() + 1
            action = "点赞"
            is_liked = True
        
        post.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return success_response(
            data={
                'post_id': post.objectId,
                'likeCount': post.likeCount,
                'user_id': user_id,
                'is_liked_by_user': is_liked,
                'action': action
            },
            message=f'{action}成功'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=f'切换点赞状态失败: {str(e)}')
