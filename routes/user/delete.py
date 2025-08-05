from flask import jsonify
from models import db, MyUser

def delete_user(object_id):
    """删除用户"""
    try:
        user = MyUser.query.get_or_404(object_id)
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500 