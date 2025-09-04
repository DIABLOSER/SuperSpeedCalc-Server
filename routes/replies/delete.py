from flask import request, jsonify
from models import db, Reply, MyUser, Posts
from datetime import datetime

def delete_reply(reply_id):
    """删除评论"""
    try:
        reply = Reply.query.get_or_404(reply_id)
        data = request.get_json() or {}
        
        user_id = data.get('user_id')  # 当前用户ID
        is_admin = data.get('is_admin', False)  # 是否为管理员操作
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'User ID is required'
            }), 400
        
        # 权限检查：作者或管理员可以删除评论
        if user_id == reply.user:
            # 作者删除自己的评论
            delete_reason = 'Deleted by author'
        elif is_admin:
            # 验证管理员权限
            admin_user = MyUser.query.get(user_id)
            if not admin_user or not admin_user.admin:
                return jsonify({
                    'success': False,
                    'error': 'Permission denied. Admin access required.'
                }), 403
            delete_reason = f'Deleted by admin: {admin_user.username}'
        else:
            return jsonify({
                'success': False,
                'error': 'Permission denied. Only the author or admin can delete this reply.'
            }), 403
        
        # 收集要删除的评论信息
        reply_info = {
            'reply_id': reply.objectId,
            'post_id': reply.post,
            'user_id': reply.user,
            'content_preview': reply.content[:50] + '...' if len(reply.content) > 50 else reply.content,
            'level': 1 if reply.is_first_level() else 2,
            'delete_reason': delete_reason,
            'deleted_by': user_id
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
        
        return jsonify({
            'success': True,
            'message': f'Reply deleted successfully. {child_replies_count} child replies also deleted.' if child_replies_count > 0 else 'Reply deleted successfully',
            'data': reply_info
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
