from flask import request, jsonify
from models import db, MyUser
from werkzeug.security import generate_password_hash

def create_user():
    """创建新用户"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'{field} is required'}), 400
        
        # 检查用户名和邮箱是否已存在
        if MyUser.query.filter_by(username=data['username']).first():
            return jsonify({'success': False, 'error': 'Username already exists'}), 400
        
        if MyUser.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'error': 'Email already exists'}), 400
        
        # 创建新用户
        user = MyUser(
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            nickname=data.get('nickname'),
            avatar=data.get('avatar'),
            bio=data.get('bio'),
            score=data.get('score', 0),
            experence=data.get('experence', 0),
            boluo=data.get('boluo', 0.0)
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def login():
    """用户登录"""
    try:
        from werkzeug.security import check_password_hash
        from datetime import datetime
        
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'error': 'Username and password are required'}), 400
        
        user = MyUser.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            user.lastLogin = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                'success': True,
                'data': user.to_dict(),
                'message': 'Login successful'
            })
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500 