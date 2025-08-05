from flask import request, jsonify
from models import db, Forum
from datetime import datetime

def update_forum_post(object_id):
    """更新社区帖子"""
    try:
        post = Forum.query.get_or_404(object_id)
        data = request.get_json()
        
        # 更新允许的字段
        allowed_fields = ['content', 'category', 'tags', 'public', 'images', 'isPinned', 'isClosed']
        for field in allowed_fields:
            if field in data:
                setattr(post, field, data[field])
        
        post.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': post.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def like_forum_post(object_id):
    """给社区帖子点赞"""
    try:
        post = Forum.query.get_or_404(object_id)
        post.likeCount += 1
        post.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': post.to_dict(),
            'message': 'Post liked successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500 