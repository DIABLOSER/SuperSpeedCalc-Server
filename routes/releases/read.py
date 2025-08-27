from flask import request, jsonify
from models import AppRelease
from sqlalchemy import desc


def get_releases():
    """获取发布记录列表（可筛选 app_name、environment、status）"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        app_name = request.args.get('app_name')
        environment = request.args.get('environment')
        status = request.args.get('status')

        query = AppRelease.query
        if app_name:
            query = query.filter(AppRelease.app_name == app_name)
        if environment:
            query = query.filter(AppRelease.environment == environment)
        if status:
            query = query.filter(AppRelease.status == status)

        query = query.order_by(desc(AppRelease.createdAt))

        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        items = [x.to_dict() for x in pagination.items]

        return jsonify({
            'message': '获取发布记录成功',
            'data': items,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev,
            }
        }), 200
    except Exception as e:
        return jsonify({'error': f'获取失败: {str(e)}'}), 500


def get_release(object_id):
    try:
        item = AppRelease.query.get(object_id)
        if not item:
            return jsonify({'error': '发布记录不存在'}), 404
        return jsonify({'message': '获取成功', 'data': item.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': f'获取失败: {str(e)}'}), 500


def get_releases_count():
    try:
        app_name = request.args.get('app_name')
        environment = request.args.get('environment')
        status = request.args.get('status')

        query = AppRelease.query
        if app_name:
            query = query.filter(AppRelease.app_name == app_name)
        if environment:
            query = query.filter(AppRelease.environment == environment)
        if status:
            query = query.filter(AppRelease.status == status)

        return jsonify({'message': '获取数量成功', 'data': {'count': query.count()}}), 200
    except Exception as e:
        return jsonify({'error': f'获取失败: {str(e)}'}), 500


