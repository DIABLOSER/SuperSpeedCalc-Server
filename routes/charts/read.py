from flask import request, jsonify
from models import Charts

def get_charts():
    """获取所有图表"""
    try:
        # 支持查询参数
        user = request.args.get('user')
        
        query = Charts.query
        
        if user:
            query = query.filter_by(user=user)
        
        charts = query.all()
        return jsonify({
            'success': True,
            'data': [chart.to_dict() for chart in charts]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def get_chart(object_id):
    """根据 objectId 获取单个图表"""
    try:
        chart = Charts.query.get_or_404(object_id)
        
        return jsonify({
            'success': True,
            'data': chart.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404

def get_leaderboard():
    """获取排行榜（按成绩值排序）"""
    try:
        limit = request.args.get('limit', 10, type=int)
        charts = Charts.query.order_by(Charts.achievement.desc()).limit(limit).all()
        return jsonify({
            'success': True,
            'data': [chart.to_dict() for chart in charts]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500 