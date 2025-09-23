from flask import request
from utils.response import (
    success_response, internal_error_response,
    not_found_response, bad_request_response
)
from models import db, Posts, MyUser, Likes
from datetime import datetime

def create_like():
    """点赞帖子"""
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
        
        # 检查是否已经点赞
        existing_like = Likes.query.filter_by(post=post_id, user=user_id).first()
        if existing_like:
            return bad_request_response(message='用户已经点赞过此帖子')
        
        # 创建点赞记录
        like_record = Likes(post=post_id, user=user_id)
        db.session.add(like_record)
        
        # 同步更新帖子的点赞计数
        post.likeCount = post.get_actual_like_count() + 1  # +1 因为新记录还未提交
        post.updatedAt = datetime.utcnow()
        
        db.session.commit()
        
        return success_response(
            data={
                'post_id': post.objectId,
                'likeCount': post.likeCount,
                'user_id': user_id,
                'like_id': like_record.objectId,
                'is_liked_by_user': True
            },
            message='点赞成功'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=f'点赞失败: {str(e)}')
