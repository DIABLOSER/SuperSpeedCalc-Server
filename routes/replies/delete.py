from flask import request, jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, Reply, MyUser, Posts
from datetime import datetime

def delete_reply(reply_id):
    """删除评论"""
    try:
        reply = Reply.query.get_or_404(reply_id)
        
        # 收集要删除的评论信息
        reply_info = {
            'reply_id': reply.objectId,
            'post_id': reply.post,
            'user_id': reply.user,
            'content_preview': reply.content[:50] + '...' if len(reply.content) > 50 else reply.content,
            'level': 1 if reply.is_first_level() else 2
        }
        
        # 如果删除的是一级评论，需要同时删除所有子回复
        child_replies_count = 0
        if reply.is_first_level():
            child_replies = Reply.query.filter_by(parent=reply.objectId).all()
            child_replies_count = len(child_replies)
            
            # 删除所有子回复
            for child_reply in child_replies:
                db.session.delete(child_reply)
            
            reply_info['child_replies_deleted'] = child_replies_count
        
        # 获取帖子信息用于更新计数
        post = Posts.query.get(reply.post)
        
        # 删除评论
        db.session.delete(reply)
        
        # 同步更新帖子的评论计数
        if post:
            # 计算要减少的评论数：当前评论 + 子回复数
            total_deleted = 1 + child_replies_count
            post.replyCount = max(0, post.replyCount - total_deleted)
            post.updatedAt = datetime.utcnow()
        
        db.session.commit()
        
        return success_response(
            data=reply_info,
            message=f'Reply deleted successfully. {child_replies_count} child replies also deleted.' if child_replies_count > 0 else 'Reply deleted successfully'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500)
