from flask import jsonify
from models import db, Charts

def delete_chart(object_id):
    """删除图表"""
    try:
        chart = Charts.query.get_or_404(object_id)
        db.session.delete(chart)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Chart deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500 