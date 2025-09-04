from flask import request, jsonify
from models import db, Reply, MyUser
from datetime import datetime

def update_reply(reply_id):
    """更新评论内容"""
    try:
        reply = Reply.query.get_or_404(reply_id)
        data = request.get_json()
        
        # 权限检查：只有评论作者可以更新评论
        user_id = data.get('user_id')  # 当前用户ID
        if not user_id or user_id != reply.user:
            return jsonify({
                'success': False,
                'error': 'Permission denied. Only the author can update this reply.'
            }), 403
        
        # 检查帖子是否可见（防止在帖子被隐藏后仍能编辑评论）
        if not reply.post_ref.is_visible_to_user(user_id):
            return jsonify({
                'success': False,
                'error': 'Cannot edit reply on invisible or unapproved post'
            }), 403
        
        # 更新内容
        if 'content' in data:
            content = data['content'].strip()
            if not content:
                return jsonify({
                    'success': False,
                    'error': 'Content cannot be empty'
                }), 400
            reply.content = content
        
        # 可选：允许更新接收者（仅限二级评论）
        if 'recipient' in data and reply.is_second_level():
            recipient_id = data['recipient']
            if recipient_id:
                recipient = MyUser.query.get(recipient_id)
                if not recipient:
                    return jsonify({
                        'success': False,
                        'error': 'Recipient user not found'
                    }), 404
                reply.recipient = recipient_id
            else:
                # 清除接收者
                reply.recipient = None
        
        reply.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Reply updated successfully',
            'data': reply.to_dict(include_details=True, include_children=False)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
