from flask import request, jsonify
from models import db, Charts
from datetime import datetime

def update_chart(object_id):
    """更新图表信息"""
    try:
        chart = Charts.query.get_or_404(object_id)
        data = request.get_json()
        
        # 更新允许的字段
        allowed_fields = ['title', 'achievement']
        for field in allowed_fields:
            if field in data:
                setattr(chart, field, data[field])
        
        chart.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': chart.to_dict(include_user=True)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def update_achievement(object_id):
    """更新图表成绩值"""
    try:
        chart = Charts.query.get_or_404(object_id)
        data = request.get_json()
        
        if 'achievement' not in data:
            return jsonify({'success': False, 'error': 'achievement is required'}), 400
        
        try:
            achievement = float(data['achievement'])
        except (ValueError, TypeError):
            return jsonify({'success': False, 'error': 'achievement must be a number'}), 400
        
        chart.achievement = achievement
        chart.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': chart.to_dict(include_user=True),
            'message': 'Achievement updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500 