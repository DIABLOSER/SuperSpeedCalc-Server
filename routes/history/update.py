from flask import request, jsonify
from models import db, History

def update_history(object_id):
    """更新历史记录"""
    try:
        history = History.query.get(object_id)
        
        if not history:
            return jsonify({'error': '历史记录不存在'}), 404
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': '请求数据不能为空'}), 400
        
        # 更新字段
        if 'title' in data:
            if not data['title']:
                return jsonify({'error': '标题不能为空'}), 400
            history.title = data['title']
        
        if 'scope' in data:
            try:
                scope = int(data['scope'])
                history.scope = scope
            except (ValueError, TypeError):
                return jsonify({'error': '数值范围必须是整数'}), 400
        
        if 'user_id' in data:
            if not data['user_id']:
                return jsonify({'error': '用户ID不能为空'}), 400
            history.user_id = data['user_id']
        
        db.session.commit()
        
        return jsonify({
            'message': '历史记录更新成功',
            'data': history.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新历史记录失败: {str(e)}'}), 500
