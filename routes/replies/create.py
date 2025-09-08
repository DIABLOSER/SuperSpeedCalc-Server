from flask import request, jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, Reply, Posts, MyUser
from datetime import datetime

def create_reply():
    """创建新评论或回复"""
    try:
        data = request.get_json()
        
        # 检查必需的参数
        post_id = data.get('post')
        user_id = data.get('user')
        content = data.get('content')
        parent_id = data.get('parent')  # 可选，用于二级评论
        recipient_id = data.get('recipient')  # 可选，用于指定接收者
        
        if not post_id or not user_id or not content:
            return internal_error_response(
                message='Post ID, user ID and content are required',
                code=400
            )
        
        # 验证帖子是否存在
        post = Posts.query.get(post_id)
        if not post:
            return internal_error_response(message='Post not found'
            , code=404)
        
        # 验证用户是否存在
        user = MyUser.query.get(user_id)
        if not user:
            return internal_error_response(message='User not found'
            , code=404)
        
        # 检查帖子是否可见和可评论
        if not post.is_visible_to_user(user_id):
            return internal_error_response(message='Post not visible or not approved'
            , code=403)
        
        # 检查内容长度
        content = content.strip()
        if len(content) == 0:
            return internal_error_response(message='Content cannot be empty'
            , code=400)
        
        # 如果是二级评论，验证父评论
        if parent_id:
            parent_reply = Reply.query.get(parent_id)
            if not parent_reply:
                return internal_error_response(message='Parent reply not found'
                , code=404)
            
            # 确保父评论是一级评论
            if not parent_reply.is_first_level():
                return internal_error_response(message='Can only reply to first level comments'
                , code=400)
            
            # 确保父评论属于同一帖子
            if parent_reply.post != post_id:
                return internal_error_response(message='Parent reply does not belong to this post'
                , code=400)
            
            # 如果没有指定接收者，默认为父评论的作者
            if not recipient_id:
                recipient_id = parent_reply.user
        
        # 验证接收者（如果指定）
        if recipient_id:
            recipient = MyUser.query.get(recipient_id)
            if not recipient:
                return internal_error_response(message='Recipient user not found'
                , code=404)
        
        # 创建评论
        reply = Reply(
            post=post_id,
            user=user_id,
            content=content,
            parent=parent_id,
            recipient=recipient_id
        )
        
        db.session.add(reply)
        
        # 同步更新帖子的评论计数
        post.replyCount = post.get_actual_reply_count() + 1
        post.updatedAt = datetime.utcnow()
        
        db.session.commit()
        
        # 返回创建的评论信息
        reply_data = reply.to_dict(include_details=True, include_children=False)
        
        return jsonify({
            'success': True,
            'message': f'{"Reply" if parent_id else "Comment"} created successfully',
            'data': reply_data
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500)
