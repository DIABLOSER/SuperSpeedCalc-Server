from flask import request, jsonify
from models import Charts

def get_charts():
    """获取所有图表"""
    try:
        # 支持查询参数
        user = request.args.get('user')
        # 分页参数
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=20, type=int)
        page = max(page or 1, 1)
        per_page = min(max(per_page or 20, 1), 100)
        # 排序参数
        sort_by = request.args.get('sort_by')
        order = (request.args.get('order') or 'desc').lower()
        allowed_fields = {
            'objectId': Charts.objectId,
            'title': Charts.title,
            'achievement': Charts.achievement,
            'user': Charts.user,
            'createdAt': Charts.createdAt,
            'updatedAt': Charts.updatedAt,
        }
        
        query = Charts.query
        
        if user:
            query = query.filter_by(user=user)
        
        # 排序
        if sort_by in allowed_fields:
            col = allowed_fields[sort_by]
            query = query.order_by(col.desc() if order == 'desc' else col.asc())
        else:
            # 默认按创建时间倒序
            query = query.order_by(Charts.createdAt.desc())
        
        # 分页
        items = query.limit(per_page).offset((page - 1) * per_page).all()
        total = query.count()
        pages = (total + per_page - 1) // per_page if per_page else 1
        
        return jsonify({
            'success': True,
            'data': [chart.to_dict() for chart in items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': pages
            }
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