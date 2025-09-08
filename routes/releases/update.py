from flask import request, jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, AppRelease


def update_release(object_id):
    try:
        item = AppRelease.query.get(object_id)
        if not item:
            return jsonify({'error': '发布记录不存在'}), 404

        data = request.get_json() or {}

        if 'app_name' in data and data['app_name'] is not None:
            item.app_name = str(data['app_name']).strip()
        if 'version_name' in data and data['version_name'] is not None:
            item.version_name = str(data['version_name']).strip()
        if 'version_code' in data and data['version_code'] is not None:
            try:
                item.version_code = int(data['version_code'])
            except Exception:
                return jsonify({'error': 'version_code 必须是整数'}), 400
        if 'changelog' in data:
            item.changelog = data['changelog']
        if 'download_url' in data:
            item.download_url = data['download_url']
        if 'environment' in data and data['environment']:
            item.environment = data['environment']
        if 'status' in data and data['status']:
            item.status = data['status']
        if 'is_update' in data:
            item.is_update = bool(data['is_update'])
        if 'force_update' in data:
            item.force_update = bool(data['force_update'])

        db.session.commit()

        return jsonify({'message': '更新成功', 'data': item.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'更新失败: {str(e)}'}), 500


