from flask import jsonify, request
from utils.response import (
    success_response, paginated_response, internal_error_response,
    not_found_response, bad_request_response, forbidden_response,
    created_response, updated_response, deleted_response
)
from models import db, Image
import os

def delete_image(object_id):
    """删除图片"""
    try:
        image = Image.query.get_or_404(object_id)
        
        # 获取文件路径（用于删除物理文件）
        file_path = image.path
        
        # 删除数据库记录
        db.session.delete(image)
        db.session.commit()
        
        # 尝试删除物理文件
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as file_error:
            # 即使文件删除失败，数据库记录已经删除成功
            print(f"Warning: Failed to delete physical file {file_path}: {file_error}")
        
        return deleted_response(message='Image deleted successfully'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500)

def delete_multiple_images():
    """批量删除图片"""
    try:
        data = request.get_json()
        image_ids = data.get('image_ids', [])
        
        if not image_ids:
            return internal_error_response(message='No image IDs provided', code=400)
        
        # 查找所有要删除的图片
        images = Image.query.filter(Image.objectId.in_(image_ids)).all()
        
        if not images:
            return internal_error_response(message='No images found', code=404)
        
        deleted_count = 0
        file_errors = []
        
        for image in images:
            try:
                # 获取文件路径
                file_path = image.path
                
                # 删除数据库记录
                db.session.delete(image)
                deleted_count += 1
                
                # 尝试删除物理文件
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as file_error:
                    file_errors.append(f"Failed to delete file {file_path}: {file_error}")
                    
            except Exception as e:
                file_errors.append(f"Failed to delete image {image.objectId}: {e}")
        
        # 提交数据库更改
        db.session.commit()
        
        result = {
            'success': True,
            'deleted_count': deleted_count,
            'message': f'{deleted_count} images deleted successfully'
        }
        
        if file_errors:
            result['file_errors'] = file_errors
        
        return success_response(data=result, message=result['message'])
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500)

def clear_all_images():
    """清空所有图片（危险操作）"""
    try:
        # 获取所有图片
        images = Image.query.all()
        
        deleted_count = 0
        file_errors = []
        
        for image in images:
            try:
                # 获取文件路径
                file_path = image.path
                
                # 删除数据库记录
                db.session.delete(image)
                deleted_count += 1
                
                # 尝试删除物理文件
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as file_error:
                    file_errors.append(f"Failed to delete file {file_path}: {file_error}")
                    
            except Exception as e:
                file_errors.append(f"Failed to delete image {image.objectId}: {e}")
        
        # 提交数据库更改
        db.session.commit()
        
        result = {
            'success': True,
            'deleted_count': deleted_count,
            'message': f'All {deleted_count} images deleted successfully'
        }
        
        if file_errors:
            result['file_errors'] = file_errors
        
        return success_response(data=result, message=result['message'])
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message=str(e), code=500) 