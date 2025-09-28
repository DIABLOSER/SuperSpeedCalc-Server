from flask import Blueprint, request, jsonify
from models import db, Feedback, MyUser
from utils.response import success_response, error_response
from datetime import datetime
import json

feedback_create_bp = Blueprint('feedback_create', __name__)

@feedback_create_bp.route('/create', methods=['POST'])
def create_feedback():
    """创建意见反馈"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['feedback_type', 'title', 'content']
        for field in required_fields:
            if not data.get(field):
                return error_response(f'缺少必填字段: {field}', 400)
        
        # 验证反馈类型
        valid_types = list(Feedback.get_feedback_types().keys())
        if data.get('feedback_type') not in valid_types:
            return error_response(f'无效的反馈类型，支持的类型: {", ".join(valid_types)}', 400)
        
        # 获取用户ID（从请求头或token中获取，这里假设从请求中获取）
        user_id = data.get('user_id')  # 实际应用中应该从JWT token中解析
        
        # 创建反馈对象
        feedback = Feedback(
            user=user_id,  # 可以为空，支持匿名反馈
            feedback_type=data['feedback_type'],
            title=data['title'],
            content=data['content'],
            priority=data.get('priority', 'medium'),
            contact=data.get('contact'),
            app_version=data.get('app_version'),
            os_info=data.get('os_info'),
            is_public=data.get('is_public', False),
            rating=data.get('rating')
        )
        
        # 处理设备信息
        if data.get('device_info'):
            feedback.set_device_info_dict(data['device_info'])
        
        # 处理附件
        if data.get('attachments'):
            feedback.set_attachments_list(data['attachments'])
        
        # 处理标签
        if data.get('tags'):
            feedback.set_tags_list(data['tags'])
        
        # 保存到数据库
        db.session.add(feedback)
        db.session.commit()
        
        # 返回创建的反馈信息
        feedback_data = feedback.to_dict(include_user=True, user_id=user_id)
        
        return success_response({
            'message': '反馈创建成功',
            'feedback': feedback_data
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'创建反馈失败: {str(e)}', 500)

@feedback_create_bp.route('/batch_create', methods=['POST'])
def batch_create_feedback():
    """批量创建意见反馈"""
    try:
        data = request.get_json()
        
        if not isinstance(data.get('feedbacks'), list):
            return error_response('feedbacks字段必须是数组', 400)
        
        feedbacks = []
        user_id = data.get('user_id')
        
        for feedback_data in data['feedbacks']:
            # 验证必填字段
            required_fields = ['feedback_type', 'title', 'content']
            for field in required_fields:
                if not feedback_data.get(field):
                    return error_response(f'反馈缺少必填字段: {field}', 400)
            
            # 验证反馈类型
            valid_types = list(Feedback.get_feedback_types().keys())
            if feedback_data.get('feedback_type') not in valid_types:
                return error_response(f'无效的反馈类型: {feedback_data.get("feedback_type")}', 400)
            
            # 创建反馈对象
            feedback = Feedback(
                user=user_id,
                feedback_type=feedback_data['feedback_type'],
                title=feedback_data['title'],
                content=feedback_data['content'],
                priority=feedback_data.get('priority', 'medium'),
                contact=feedback_data.get('contact'),
                app_version=feedback_data.get('app_version'),
                os_info=feedback_data.get('os_info'),
                is_public=feedback_data.get('is_public', False),
                rating=feedback_data.get('rating')
            )
            
            # 处理设备信息
            if feedback_data.get('device_info'):
                feedback.set_device_info_dict(feedback_data['device_info'])
            
            # 处理附件
            if feedback_data.get('attachments'):
                feedback.set_attachments_list(feedback_data['attachments'])
            
            # 处理标签
            if feedback_data.get('tags'):
                feedback.set_tags_list(feedback_data['tags'])
            
            feedbacks.append(feedback)
        
        # 批量保存
        db.session.add_all(feedbacks)
        db.session.commit()
        
        # 返回创建的反馈信息
        feedbacks_data = [f.to_dict(include_user=True, user_id=user_id) for f in feedbacks]
        
        return success_response({
            'message': f'成功创建{len(feedbacks)}条反馈',
            'feedbacks': feedbacks_data
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'批量创建反馈失败: {str(e)}', 500)
