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
            'data': chart.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def update_achievement(object_id):
    """更新图表成绩值"""
    try:
        chart = Charts.query.get_or_404(object_id)
        data = request.get_json()
        
        achievement_change = data.get('achievement_change', 0.0)
        chart.achievement += achievement_change
        
        # 确保成绩值不为负数
        if chart.achievement < 0:
            chart.achievement = 0.0
        
        chart.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': chart.to_dict(),
            'message': f'Achievement updated by {achievement_change}'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500 