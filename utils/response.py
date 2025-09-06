"""
统一API响应格式工具
提供标准化的API响应格式，确保所有接口返回数据的一致性
使用智能的 code、message、data 格式：
- 基础只有三个字段：code、message、data
- 成功时：data 包含所有返回数据（JSON字符串格式）
- 错误时：data 为 null
- 其他信息（如分页、元数据等）都包含在 data 中
"""

from flask import jsonify
from typing import Any, Dict, Optional, Union, List
import json


class APIResponse:
    """API响应类，提供统一的响应格式"""
    
    @staticmethod
    def success(
        data: Any = None,
        message: str = "操作成功",
        code: int = 200
    ) -> tuple:
        """
        成功响应
        
        Args:
            data: 响应数据
            message: 响应消息
            code: HTTP状态码
            
        Returns:
            tuple: (jsonify对象, HTTP状态码)
        """
        # 将data转换为JSON字符串
        data_str = None
        if data is not None:
            try:
                data_str = json.dumps(data, ensure_ascii=False)
            except (TypeError, ValueError) as e:
                # 如果无法序列化，则使用字符串表示
                data_str = str(data)
        
        response = {
            "code": code,
            "message": message,
            "data": data_str
        }
            
        return jsonify(response), code
    
    @staticmethod
    def error(
        message: str = "操作失败",
        code: int = 400
    ) -> tuple:
        """
        错误响应
        
        Args:
            message: 错误消息
            code: HTTP状态码
            
        Returns:
            tuple: (jsonify对象, HTTP状态码)
        """
        response = {
            "code": code,
            "message": message,
            "data": None
        }
            
        return jsonify(response), code
    
    @staticmethod
    def created(
        data: Any = None,
        message: str = "创建成功"
    ) -> tuple:
        """
        创建成功响应 (201)
        
        Args:
            data: 响应数据
            message: 响应消息
            
        Returns:
            tuple: (jsonify对象, 201)
        """
        return APIResponse.success(data=data, message=message, code=201)
    
    @staticmethod
    def updated(
        data: Any = None,
        message: str = "更新成功"
    ) -> tuple:
        """
        更新成功响应 (200)
        
        Args:
            data: 响应数据
            message: 响应消息
            
        Returns:
            tuple: (jsonify对象, 200)
        """
        return APIResponse.success(data=data, message=message, code=200)
    
    @staticmethod
    def deleted(
        message: str = "删除成功"
    ) -> tuple:
        """
        删除成功响应 (200)
        
        Args:
            message: 响应消息
            
        Returns:
            tuple: (jsonify对象, 200)
        """
        return APIResponse.success(data=None, message=message, code=200)
    
    @staticmethod
    def not_found(
        message: str = "资源不存在"
    ) -> tuple:
        """
        资源不存在响应 (404)
        
        Args:
            message: 错误消息
            
        Returns:
            tuple: (jsonify对象, 404)
        """
        return APIResponse.error(message=message, code=404)
    
    @staticmethod
    def bad_request(
        message: str = "请求参数错误"
    ) -> tuple:
        """
        请求参数错误响应 (400)
        
        Args:
            message: 错误消息
            
        Returns:
            tuple: (jsonify对象, 400)
        """
        return APIResponse.error(message=message, code=400)
    
    @staticmethod
    def unauthorized(
        message: str = "未授权访问"
    ) -> tuple:
        """
        未授权响应 (401)
        
        Args:
            message: 错误消息
            
        Returns:
            tuple: (jsonify对象, 401)
        """
        return APIResponse.error(message=message, code=401)
    
    @staticmethod
    def forbidden(
        message: str = "禁止访问"
    ) -> tuple:
        """
        禁止访问响应 (403)
        
        Args:
            message: 错误消息
            
        Returns:
            tuple: (jsonify对象, 403)
        """
        return APIResponse.error(message=message, code=403)
    
    @staticmethod
    def internal_error(
        message: str = "服务器内部错误"
    ) -> tuple:
        """
        服务器内部错误响应 (500)
        
        Args:
            message: 错误消息
            
        Returns:
            tuple: (jsonify对象, 500)
        """
        return APIResponse.error(message=message, code=500)
    
    @staticmethod
    def paginated(
        data: List[Any],
        page: int,
        per_page: int,
        total: int,
        message: str = "获取成功"
    ) -> tuple:
        """
        分页响应
        
        Args:
            data: 数据列表
            page: 当前页码
            per_page: 每页数量
            total: 总数量
            message: 响应消息
            
        Returns:
            tuple: (jsonify对象, 200)
        """
        pages = (total + per_page - 1) // per_page if per_page else 1
        
        pagination_data = {
            "list": data,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": pages,
                "has_next": page < pages,
                "has_prev": page > 1
            }
        }
        
        return APIResponse.success(
            data=pagination_data,
            message=message
        )


# 便捷函数，直接导入使用
def success_response(data=None, message="操作成功", code=200):
    """成功响应便捷函数"""
    return APIResponse.success(data, message, code)


def error_response(message="操作失败", code=400):
    """错误响应便捷函数"""
    return APIResponse.error(message, code)


def created_response(data=None, message="创建成功"):
    """创建成功响应便捷函数"""
    return APIResponse.created(data, message)


def updated_response(data=None, message="更新成功"):
    """更新成功响应便捷函数"""
    return APIResponse.updated(data, message)


def deleted_response(message="删除成功"):
    """删除成功响应便捷函数"""
    return APIResponse.deleted(message)


def not_found_response(message="资源不存在"):
    """资源不存在响应便捷函数"""
    return APIResponse.not_found(message)


def bad_request_response(message="请求参数错误"):
    """请求参数错误响应便捷函数"""
    return APIResponse.bad_request(message)


def unauthorized_response(message="未授权访问"):
    """未授权响应便捷函数"""
    return APIResponse.unauthorized(message)


def forbidden_response(message="禁止访问"):
    """禁止访问响应便捷函数"""
    return APIResponse.forbidden(message)


def internal_error_response(message="服务器内部错误"):
    """服务器内部错误响应便捷函数"""
    return APIResponse.internal_error(message)


def paginated_response(data, page, per_page, total, message="获取成功"):
    """分页响应便捷函数"""
    return APIResponse.paginated(data, page, per_page, total, message)
