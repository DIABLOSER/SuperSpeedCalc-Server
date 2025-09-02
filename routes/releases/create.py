from flask import request, jsonify
from models import db, AppRelease


def create_release():
    """创建应用发布记录"""
    try:
        data = request.get_json() or {}

        required_fields = ['app_name', 'version_name', 'version_code']
        for field in required_fields:
            if data.get(field) in [None, '']:
                return jsonify({'error': f'{field} 不能为空'}), 400

        # 校验类型
        try:
            version_code = int(data.get('version_code'))
        except Exception:
            return jsonify({'error': 'version_code 必须是整数'}), 400

        release = AppRelease(
            app_name=str(data.get('app_name')).strip(),
            version_name=str(data.get('version_name')).strip(),
            version_code=version_code,
            changelog=data.get('changelog'),
            download_url=data.get('download_url'),
            environment=(data.get('environment') or 'production'),
            status=(data.get('status') or 'published'),
            is_update=bool(data.get('is_update', False)),
            force_update=bool(data.get('force_update', False)),
        )

        db.session.add(release)
        db.session.commit()

        return jsonify({'message': '发布记录创建成功', 'data': release.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'创建失败: {str(e)}'}), 500

        


