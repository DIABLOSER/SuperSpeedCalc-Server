from flask import request
from utils.response import (
    success_response, internal_error_response,
    not_found_response, bad_request_response
)
from models import db, Posts, MyUser, Likes
from datetime import datetime

def delete_like():
    """取消点赞帖子"""
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
        
        # 查找点赞记录
        like_record = Likes.query.filter_by(post=post_id, user=user_id).first()
        if not like_record:
            return bad_request_response(message='用户未点赞过此帖子')
        
        # 删除点赞记录
        db.session.delete(like_record)
        
        # 同步更新帖子的点赞计数
        post.likeCount = max(0, post.get_actual_like_count() - 1)  # -1 因为记录还未删除，确保不为负数
        post.updatedAt = datetime.utcnow()
        
        db.session.commit()
        
        return success_response(
            data={
                'post_id': post.objectId,
                'likeCount': post.likeCount,
                'user_id': user_id,
                'is_liked_by_user': False
            },
            message='取消点赞成功'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=f'取消点赞失败: {str(e)}')
