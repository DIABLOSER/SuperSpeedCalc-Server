from flask import jsonify
from models import db, Forum

def delete_forum_post(object_id):
    """删除社区帖子"""
    try:
        post = Forum.query.get_or_404(object_id)
        db.session.delete(post)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Forum post deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500 