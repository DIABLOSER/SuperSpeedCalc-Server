from flask import request, jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, Posts, MyUser, Likes
from datetime import datetime

def update_post(post_id):
    """更新帖子信息（包括审核状态）"""
    try:
        post = Posts.query.get_or_404(post_id)
        data = request.get_json()
        
        # 移除权限检查，任何人都可以更新帖子
        user_id = data.get('user_id')  # 当前用户ID
        
        # 更新允许的字段
        if 'content' in data:
            content = data['content'].strip()
            if not content:
                return internal_error_response(message='Content cannot be empty', code=400)
            post.content = content
        
        if 'visible' in data:
            post.visible = bool(data['visible'])
        
        if 'images' in data:
            images = data['images']
            if isinstance(images, list):
                post.set_images_list(images)
        
        # 更新审核状态
        if 'audit_state' in data:
            new_audit_state = data['audit_state']
            reason = data.get('reason', '')  # 审核意见
            
            # 验证审核状态
            valid_states = Posts.get_audit_states()
            if new_audit_state not in valid_states:
                return bad_request_response(
                    message=f'Invalid audit state. Valid states: {list(valid_states.keys())}',
                    code=400
                )
            
            old_state = post.audit_state
            post.audit_state = new_audit_state
        
        post.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return updated_response(data=post.to_dict(include_user=True, user_id=user_id), message='Post updated successfully')
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500)


def like_post(post_id):
    """点赞帖子"""
    try:
        post = Posts.query.get_or_404(post_id)
        data = request.get_json()
        
        user_id = data.get('user_id')
        if not user_id:
            return internal_error_response(message='User ID is required', code=400)
        
        # 验证用户存在
        user = MyUser.query.get(user_id)
        if not user:
            return internal_error_response(message='User not found', code=404)
        
        # 移除可见性检查，任何人都可以点赞所有帖子
        
        # 检查是否已经点赞
        existing_like = Likes.query.filter_by(post=post_id, user=user_id).first()
        if existing_like:
            return internal_error_response(message='User has already liked this post', code=400)
        
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
            message='Post liked successfully'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500)

def unlike_post(post_id):
    """取消点赞帖子"""
    try:
        post = Posts.query.get_or_404(post_id)
        data = request.get_json()
        
        user_id = data.get('user_id')
        if not user_id:
            return internal_error_response(message='User ID is required', code=400)
        
        # 验证用户存在
        user = MyUser.query.get(user_id)
        if not user:
            return internal_error_response(message='User not found', code=404)
        
        # 移除可见性检查，任何人都可以点赞所有帖子
        
        # 查找点赞记录
        like_record = Likes.query.filter_by(post=post_id, user=user_id).first()
        if not like_record:
            return internal_error_response(message='User has not liked this post', code=400)
        
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
            message='Post unliked successfully'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500)
