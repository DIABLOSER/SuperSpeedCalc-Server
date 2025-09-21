from flask import request, jsonify, current_app
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from werkzeug.utils import secure_filename
from models import db, Image
import os
import uuid
from datetime import datetime

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}

def allowed_file(filename):
    """检查文件扩展名是否被允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(original_filename):
    """生成唯一的文件名"""
    # 获取文件扩展名
    ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    # 生成唯一文件名：时间戳 + UUID + 原始扩展名
    unique_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    return f"{unique_name}.{ext}" if ext else unique_name

def save_uploaded_file(file, upload_folder='uploads/images'):
    """保存上传的文件"""
    if not file or file.filename == '':
        raise ValueError('No file selected')
    
    if not allowed_file(file.filename):
        raise ValueError('File type not allowed')
    
    # 确保上传目录存在
    os.makedirs(upload_folder, exist_ok=True)
    
    # 生成安全的文件名
    original_filename = secure_filename(file.filename)
    unique_filename = generate_unique_filename(original_filename)
    
    # 保存文件
    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)
    
    # 生成URL（与应用静态路由匹配）
    file_url = f"/uploads/images/{unique_filename}"
    
    return {
        'fileName': unique_filename,
        'path': file_path,
        'url': file_url,
        'fileSize': os.path.getsize(file_path)
    }

def create_image():
    """创建新图片记录（JSON方式）"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['fileName', 'path', 'url']
        for field in required_fields:
            if field not in data:
                return bad_request_response(
                    message=f'{field} is required',
                    # error_code='MISSING_REQUIRED_FIELD',
                    # details={'field': field}
                )
        
        # 创建新图片记录
        image = Image(
            fileName=data['fileName'],
            path=data['path'],
            url=data['url'],
            fileSize=data.get('fileSize')
        )
        
        db.session.add(image)
        db.session.commit()
        
        return success_response(data=image.to_dict(), code=201)
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500)

def upload_single_image():
    """上传单个图片文件"""
    try:
        # 检查是否有文件上传
        if 'file' not in request.files:
            return internal_error_response(message='No file uploaded', code=400)
        
        file = request.files['file']
        
        # 保存文件
        file_info = save_uploaded_file(file)
        
        # 创建数据库记录
        image = Image(
            fileName=file_info['fileName'],
            path=file_info['path'],
            url=file_info['url'],
            fileSize=file_info['fileSize']
        )
        
        db.session.add(image)
        db.session.commit()
        
        return success_response(
            data=image.to_dict(),
            message='Image uploaded successfully',
            code=201
        )
        
    except ValueError as e:
        return internal_error_response(message=str(e), code=400)
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500)

def upload_multiple_images():
    """批量上传图片文件"""
    try:
        # 检查是否有文件上传
        if 'files' not in request.files:
            return internal_error_response(message='No files uploaded', code=400)
        
        files = request.files.getlist('files')
        
        if not files or all(file.filename == '' for file in files):
            return internal_error_response(message='No files selected', code=400)
        
        uploaded_images = []
        errors = []
        
        for i, file in enumerate(files):
            try:
                if file.filename == '':
                    continue
                    
                # 保存文件
                file_info = save_uploaded_file(file)
                
                # 创建数据库记录
                image = Image(
                    fileName=file_info['fileName'],
                    path=file_info['path'],
                    url=file_info['url'],
                    fileSize=file_info['fileSize']
                )
                
                db.session.add(image)
                uploaded_images.append(image)
                
            except Exception as e:
                errors.append(f"File {i+1} ({file.filename}): {str(e)}")
        
        # 提交所有成功的上传
        if uploaded_images:
            db.session.commit()
        
        result = {
            'items': [img.to_dict() for img in uploaded_images],
            'uploaded_count': len(uploaded_images),
            'total_files': len(files)
        }
        
        if errors:
            result['errors'] = errors
            message = f"Uploaded {len(uploaded_images)} files successfully, {len(errors)} files failed"
        else:
            message = f"All {len(uploaded_images)} files uploaded successfully"
        
        return created_response(data=result, message=message)
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500) 