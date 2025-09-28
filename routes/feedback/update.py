from flask import Blueprint, request, jsonify
from models import db, Feedback, MyUser
from utils.response import success_response, error_response
from datetime import datetime
import json

feedback_update_bp = Blueprint('feedback_update', __name__)

@feedback_update_bp.route('/<feedback_id>', methods=['PUT'])
def update_feedback(feedback_id):
    """更新反馈信息"""
    try:
        feedback = Feedback.query.get(feedback_id)
        
        if not feedback:
            return error_response('反馈不存在', 404)
        
        data = request.get_json()
        
        # 获取当前用户ID（实际应用中应该从JWT token中解析）
        current_user_id = request.args.get('current_user_id')
        is_admin = request.args.get('is_admin', 'false').lower() == 'true'
        
        # 检查权限
        if not is_admin and not feedback.can_be_edited_by_user(current_user_id):
            return error_response('没有权限编辑此反馈', 403)
        
        # 更新字段
        if 'title' in data:
            feedback.title = data['title']
        
        if 'content' in data:
            feedback.content = data['content']
        
        if 'feedback_type' in data:
            # 验证反馈类型
            valid_types = list(Feedback.get_feedback_types().keys())
            if data['feedback_type'] not in valid_types:
                return error_response(f'无效的反馈类型，支持的类型: {", ".join(valid_types)}', 400)
            feedback.feedback_type = data['feedback_type']
        
        if 'contact' in data:
            feedback.contact = data['contact']
        
        if 'app_version' in data:
            feedback.app_version = data['app_version']
        
        if 'os_info' in data:
            feedback.os_info = data['os_info']
        
        if 'rating' in data:
            rating = data['rating']
            if rating is not None and (not isinstance(rating, int) or rating < 1 or rating > 5):
                return error_response('评分必须是1-5之间的整数', 400)
            feedback.rating = rating
        
        if 'is_public' in data:
            feedback.is_public = bool(data['is_public'])
        
        # 处理设备信息
        if 'device_info' in data:
            feedback.set_device_info_dict(data['device_info'])
        
        # 处理附件
        if 'attachments' in data:
            feedback.set_attachments_list(data['attachments'])
        
        # 处理标签
        if 'tags' in data:
            feedback.set_tags_list(data['tags'])
        
        # 管理员专用字段
        if is_admin:
            if 'status' in data:
                feedback.update_status(data['status'], current_user_id)
            
            if 'priority' in data:
                feedback.update_priority(data['priority'])
            
            if 'admin_reply' in data:
                feedback.set_admin_reply(data['admin_reply'], current_user_id)
        
        # 保存更改
        db.session.commit()
        
        # 返回更新后的反馈信息
        feedback_data = feedback.to_dict(
            include_user=True, 
            include_admin=True,
            user_id=current_user_id,
            is_admin=is_admin
        )
        
        return success_response({
            'message': '反馈更新成功',
            'feedback': feedback_data
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'更新反馈失败: {str(e)}', 500)

@feedback_update_bp.route('/<feedback_id>/status', methods=['PUT'])
def update_feedback_status(feedback_id):
    """更新反馈状态（管理员专用）"""
    try:
        feedback = Feedback.query.get(feedback_id)
        
        if not feedback:
            return error_response('反馈不存在', 404)
        
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return error_response('缺少状态参数', 400)
        
        # 验证状态
        valid_statuses = list(Feedback.get_statuses().keys())
        if new_status not in valid_statuses:
            return error_response(f'无效的状态，支持的状态: {", ".join(valid_statuses)}', 400)
        
        # 获取当前用户ID（实际应用中应该从JWT token中解析）
        current_user_id = request.args.get('current_user_id')
        is_admin = request.args.get('is_admin', 'false').lower() == 'true'
        
        # 检查权限（只有管理员可以更新状态）
        if not is_admin:
            return error_response('只有管理员可以更新反馈状态', 403)
        
        # 更新状态
        feedback.update_status(new_status, current_user_id)
        
        # 保存更改
        db.session.commit()
        
        # 返回更新后的反馈信息
        feedback_data = feedback.to_dict(
            include_user=True, 
            include_admin=True,
            user_id=current_user_id,
            is_admin=is_admin
        )
        
        return success_response({
            'message': f'反馈状态已更新为: {Feedback.get_statuses().get(new_status, new_status)}',
            'feedback': feedback_data
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'更新反馈状态失败: {str(e)}', 500)

@feedback_update_bp.route('/<feedback_id>/priority', methods=['PUT'])
def update_feedback_priority(feedback_id):
    """更新反馈优先级（管理员专用）"""
    try:
        feedback = Feedback.query.get(feedback_id)
        
        if not feedback:
            return error_response('反馈不存在', 404)
        
        data = request.get_json()
        new_priority = data.get('priority')
        
        if not new_priority:
            return error_response('缺少优先级参数', 400)
        
        # 验证优先级
        valid_priorities = list(Feedback.get_priorities().keys())
        if new_priority not in valid_priorities:
            return error_response(f'无效的优先级，支持的优先级: {", ".join(valid_priorities)}', 400)
        
        # 获取当前用户ID（实际应用中应该从JWT token中解析）
        current_user_id = request.args.get('current_user_id')
        is_admin = request.args.get('is_admin', 'false').lower() == 'true'
        
        # 检查权限（只有管理员可以更新优先级）
        if not is_admin:
            return error_response('只有管理员可以更新反馈优先级', 403)
        
        # 更新优先级
        feedback.update_priority(new_priority)
        
        # 保存更改
        db.session.commit()
        
        # 返回更新后的反馈信息
        feedback_data = feedback.to_dict(
            include_user=True, 
            include_admin=True,
            user_id=current_user_id,
            is_admin=is_admin
        )
        
        return success_response({
            'message': f'反馈优先级已更新为: {Feedback.get_priorities().get(new_priority, new_priority)}',
            'feedback': feedback_data
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'更新反馈优先级失败: {str(e)}', 500)

@feedback_update_bp.route('/<feedback_id>/reply', methods=['POST'])
def reply_to_feedback(feedback_id):
    """管理员回复反馈"""
    try:
        feedback = Feedback.query.get(feedback_id)
        
        if not feedback:
            return error_response('反馈不存在', 404)
        
        data = request.get_json()
        reply_content = data.get('reply')
        
        if not reply_content:
            return error_response('缺少回复内容', 400)
        
        # 获取当前用户ID（实际应用中应该从JWT token中解析）
        current_user_id = request.args.get('current_user_id')
        is_admin = request.args.get('is_admin', 'false').lower() == 'true'
        
        # 检查权限（只有管理员可以回复）
        if not is_admin:
            return error_response('只有管理员可以回复反馈', 403)
        
        # 设置管理员回复
        feedback.set_admin_reply(reply_content, current_user_id)
        
        # 保存更改
        db.session.commit()
        
        # 返回更新后的反馈信息
        feedback_data = feedback.to_dict(
            include_user=True, 
            include_admin=True,
            user_id=current_user_id,
            is_admin=is_admin
        )
        
        return success_response({
            'message': '回复已添加',
            'feedback': feedback_data
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'回复反馈失败: {str(e)}', 500)

@feedback_update_bp.route('/<feedback_id>/attachments', methods=['POST'])
def add_attachment(feedback_id):
    """添加附件到反馈"""
    try:
        feedback = Feedback.query.get(feedback_id)
        
        if not feedback:
            return error_response('反馈不存在', 404)
        
        data = request.get_json()
        attachment_url = data.get('attachment_url')
        
        if not attachment_url:
            return error_response('缺少附件URL', 400)
        
        # 获取当前用户ID（实际应用中应该从JWT token中解析）
        current_user_id = request.args.get('current_user_id')
        is_admin = request.args.get('is_admin', 'false').lower() == 'true'
        
        # 检查权限
        if not is_admin and not feedback.can_be_edited_by_user(current_user_id):
            return error_response('没有权限编辑此反馈', 403)
        
        # 添加附件
        feedback.add_attachment(attachment_url)
        
        # 保存更改
        db.session.commit()
        
        # 返回更新后的反馈信息
        feedback_data = feedback.to_dict(
            include_user=True, 
            include_admin=True,
            user_id=current_user_id,
            is_admin=is_admin
        )
        
        return success_response({
            'message': '附件已添加',
            'feedback': feedback_data
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'添加附件失败: {str(e)}', 500)

@feedback_update_bp.route('/<feedback_id>/attachments', methods=['DELETE'])
def remove_attachment(feedback_id):
    """从反馈中移除附件"""
    try:
        feedback = Feedback.query.get(feedback_id)
        
        if not feedback:
            return error_response('反馈不存在', 404)
        
        data = request.get_json()
        attachment_url = data.get('attachment_url')
        
        if not attachment_url:
            return error_response('缺少附件URL', 400)
        
        # 获取当前用户ID（实际应用中应该从JWT token中解析）
        current_user_id = request.args.get('current_user_id')
        is_admin = request.args.get('is_admin', 'false').lower() == 'true'
        
        # 检查权限
        if not is_admin and not feedback.can_be_edited_by_user(current_user_id):
            return error_response('没有权限编辑此反馈', 403)
        
        # 移除附件
        feedback.remove_attachment(attachment_url)
        
        # 保存更改
        db.session.commit()
        
        # 返回更新后的反馈信息
        feedback_data = feedback.to_dict(
            include_user=True, 
            include_admin=True,
            user_id=current_user_id,
            is_admin=is_admin
        )
        
        return success_response({
            'message': '附件已移除',
            'feedback': feedback_data
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'移除附件失败: {str(e)}', 500)
