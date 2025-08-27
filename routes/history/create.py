from flask import request, jsonify
from models import db, History, MyUser
from datetime import datetime

def create_history():
    """创建历史记录"""
    try:
        data = request.get_json()
        
        # 验证必需字段
        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400
        
        title = data.get('title')
        score = data.get('score')
        user = data.get('user')
        
        if not title:
            return jsonify({'error': '标题不能为空'}), 400
        
        if score is None:
            return jsonify({'error': '分数不能为空'}), 400
        
        if not user:
            return jsonify({'error': '用户ID不能为空'}), 400
        
        # 验证用户是否存在
        user_obj = MyUser.query.get(user)
        if not user_obj:
            return jsonify({'error': '用户不存在'}), 404
        
        # 验证score是否为整数
        try:
            score = int(score)
        except (ValueError, TypeError):
            return jsonify({'error': '分数必须是整数'}), 400
        
        # 创建历史记录
        history = History(
            title=title,
            score=score,
            user=user
        )
        
        db.session.add(history)
        db.session.commit()
        
        return jsonify({
            'message': '历史记录创建成功',
            'data': history.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'创建历史记录失败: {str(e)}'}), 500
