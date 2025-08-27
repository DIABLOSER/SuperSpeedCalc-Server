from flask import jsonify
from models import db, AppRelease


def delete_release(object_id):
    try:
        item = AppRelease.query.get(object_id)
        if not item:
            return jsonify({'error': '发布记录不存在'}), 404

        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': '删除成功'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'删除失败: {str(e)}'}), 500


