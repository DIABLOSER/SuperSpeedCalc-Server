from flask import request, jsonify
from models import db, MyUser
from werkzeug.security import generate_password_hash
from datetime import datetime

def update_user(object_id):
    """更新用户信息"""
    try:
        user = MyUser.query.get_or_404(object_id)
        data = request.get_json()
        
        # 更新允许的字段
        allowed_fields = ['nickname', 'avatar', 'bio', 'isActive', 'score', 'experence', 'boluo']
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])
        
        # 特殊处理密码
        if 'password' in data:
            user.password = generate_password_hash(data['password'])
        
        user.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def update_user_score(object_id):
    """更新用户积分"""
    try:
        user = MyUser.query.get_or_404(object_id)
        data = request.get_json()
        
        score_change = data.get('score_change', 0)
        user.score += score_change
        
        # 确保积分不为负数
        if user.score < 0:
            user.score = 0
        
        user.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': user.to_dict(),
            'message': f'Score updated by {score_change}'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def update_user_experence(object_id):
    """更新用户经验值"""
    try:
        user = MyUser.query.get_or_404(object_id)
        data = request.get_json()
        
        exp_change = data.get('exp_change', 0)
        user.experence += exp_change
        
        # 确保经验值不为负数
        if user.experence < 0:
            user.experence = 0
        
        user.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': user.to_dict(),
            'message': f'Experience updated by {exp_change}'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def update_user_boluo(object_id):
    """更新用户菠萝币"""
    try:
        user = MyUser.query.get_or_404(object_id)
        data = request.get_json()
        
        boluo_change = data.get('boluo_change', 0)
        user.boluo += boluo_change
        
        # 确保菠萝币不为负数
        if user.boluo < 0:
            user.boluo = 0
        
        user.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': user.to_dict(),
            'message': f'Boluo updated by {boluo_change}'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500 