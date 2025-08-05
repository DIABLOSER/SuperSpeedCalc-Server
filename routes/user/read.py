from flask import jsonify
from models import MyUser

def get_users():
    """获取所有用户"""
    try:
        users = MyUser.query.all()
        return jsonify({
            'success': True,
            'data': [user.to_dict() for user in users]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def get_user(object_id):
    """根据 objectId 获取单个用户"""
    try:
        user = MyUser.query.get_or_404(object_id)
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404 