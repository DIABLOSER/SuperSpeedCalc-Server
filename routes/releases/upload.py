from flask import request, jsonify
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from werkzeug.utils import secure_filename
from models import db, AppRelease
import os
from datetime import datetime


ALLOWED_APK_EXTENSIONS = {"apk"}


def allowed_apk(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_APK_EXTENSIONS


def generate_unique_filename(original_filename):
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    # 使用 Unix 毫秒时间戳作为完整文件名，确保唯一且可排序
    timestamp_ms = int(datetime.now().timestamp() * 1000)
    unique_name = str(timestamp_ms)
    return f"{unique_name}.{ext}" if ext else unique_name


def upload_apk():
    """上传 APK 文件；可选绑定到指定发布记录（release_id）并回写 download_url"""
    try:
        if 'file' not in request.files:
            return internal_error_response(message='No file uploaded', code=400)

        file = request.files['file']
        if file.filename == '':
            return internal_error_response(message='No file selected', code=400)

        if not allowed_apk(file.filename):
            return internal_error_response(message='File type not allowed, only .apk', code=400)

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
                return internal_error_response(message='Release not found', code=404)
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

        return created_response(data=result, message=result['message'])
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500)


