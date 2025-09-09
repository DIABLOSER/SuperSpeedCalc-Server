"""
简化的API响应工具类
提供统一的响应格式：成功响应和失败响应
"""

from flask import jsonify


def success_response(data=None, message="操作成功", code=200):
    """
    成功响应
    
    Args:
        data: 响应数据
        message: 响应消息
        code: HTTP状态码
    
    Returns:
        tuple: (jsonify对象, HTTP状态码)
    """
    return jsonify({
        "code": code,
        "message": message,
        "data": data
    }), code


def error_response(message="操作失败", code=400):
    """
    失败响应
    
    Args:
        message: 错误消息
        code: HTTP状态码
    
    Returns:
        tuple: (jsonify对象, HTTP状态码)
    """
    return jsonify({
        "code": code,
        "message": message
    }), code


# 为了兼容现有代码，提供一些别名函数
def created_response(data=None, message="创建成功", code=201):
    """创建成功响应"""
    return success_response(data=data, message=message, code=code)


def bad_request_response(message="请求参数错误", code=400):
    """客户端错误响应"""
    return error_response(message=message, code=code)


def not_found_response(message="资源未找到", code=404):
    """资源未找到响应"""
    return error_response(message=message, code=code)


def unauthorized_response(message="未授权访问", code=401):
    """未授权响应"""
    return error_response(message=message, code=code)


def internal_error_response(message="服务器内部错误", code=500):
    """服务器错误响应"""
    return error_response(message=message, code=code)


def paginated_response(items, pagination, message="获取数据成功", code=200):
    """
    分页响应
    
    Args:
        items: 数据列表
        pagination: 分页信息
        message: 响应消息
        code: HTTP状态码
    
    Returns:
        tuple: (jsonify对象, HTTP状态码)
    """
    data = {
        "items": items,
        "pagination": pagination
    }
    return success_response(data=data, message=message, code=code)


# 兼容性函数 - 为了保持现有代码的兼容性
def updated_response(data=None, message="更新成功", code=200):
    """更新成功响应"""
    return success_response(data=data, message=message, code=code)


def deleted_response(data=None, message="删除成功", code=200):
    """删除成功响应"""
    return success_response(data=data, message=message, code=code)


def forbidden_response(message="禁止访问", code=403):
    """禁止访问响应"""
    return error_response(message=message, code=code)
