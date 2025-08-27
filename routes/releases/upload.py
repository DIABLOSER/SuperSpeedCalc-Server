from flask import request, jsonify
from werkzeug.utils import secure_filename
from models import db, AppRelease
import os
import uuid
from datetime import datetime


ALLOWED_APK_EXTENSIONS = {"apk"}


def allowed_apk(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_APK_EXTENSIONS


def generate_unique_filename(original_filename):
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    unique_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    return f"{unique_name}.{ext}" if ext else unique_name


def upload_apk():
    """上传 APK 文件；可选绑定到指定发布记录（release_id）并回写 download_url"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400

        if not allowed_apk(file.filename):
            return jsonify({'success': False, 'error': 'File type not allowed, only .apk'}), 400

        upload_folder = 'uploads/apk'
        os.makedirs(upload_folder, exist_ok=True)

        original_filename = secure_filename(file.filename)
        unique_filename = generate_unique_filename(original_filename)
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)

        file_url = f"/uploads/apk/{unique_filename}"

        # 可选：绑定到发布记录
        release_id = request.form.get('release_id') or request.args.get('release_id')
        release_dict = None
        if release_id:
            release = AppRelease.query.get(release_id)
            if not release:
                return jsonify({'success': False, 'error': 'Release not found'}), 404
            release.download_url = file_url
            db.session.commit()
            release_dict = release.to_dict()

        result = {
            'success': True,
            'data': {
                'fileName': unique_filename,
                'path': file_path,
                'url': file_url,
                'fileSize': os.path.getsize(file_path)
            },
            'message': 'APK uploaded successfully'
        }
        if release_dict:
            result['release'] = release_dict

        return jsonify(result), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


