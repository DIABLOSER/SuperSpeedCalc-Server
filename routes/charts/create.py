from flask import request, jsonify
from models import db, Charts, MyUser

def create_chart():
    """创建新图表"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['title', 'user']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'{field} is required'}), 400
        
        # 验证用户是否存在
        user = MyUser.query.get(data['user'])
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        # 创建新图表
        chart = Charts(
            title=data['title'],
            achievement=data.get('achievement', 0.0),
            user=data['user']
        )
        
        db.session.add(chart)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': chart.to_dict(include_user=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500 