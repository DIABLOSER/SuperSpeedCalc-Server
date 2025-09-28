from flask import Blueprint, request, jsonify
from models import db, Feedback, MyUser
from utils.response import success_response, error_response

feedback_delete_bp = Blueprint('feedback_delete', __name__)

@feedback_delete_bp.route('/<feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):
    """删除反馈"""
    try:
        feedback = Feedback.query.get(feedback_id)
        
        if not feedback:
            return error_response('反馈不存在', 404)
        
        # 获取当前用户ID（实际应用中应该从JWT token中解析）
        current_user_id = request.args.get('current_user_id')
        is_admin = request.args.get('is_admin', 'false').lower() == 'true'
        
        # 检查权限
        if not is_admin and feedback.user != current_user_id:
            return error_response('没有权限删除此反馈', 403)
        
        # 删除反馈
        db.session.delete(feedback)
        db.session.commit()
        
        return success_response({
            'message': '反馈删除成功'
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'删除反馈失败: {str(e)}', 500)

@feedback_delete_bp.route('/batch_delete', methods=['DELETE'])
def batch_delete_feedback():
    """批量删除反馈"""
    try:
        data = request.get_json()
        feedback_ids = data.get('feedback_ids', [])
        
        if not feedback_ids or not isinstance(feedback_ids, list):
            return error_response('缺少反馈ID列表', 400)
        
        # 获取当前用户ID（实际应用中应该从JWT token中解析）
        current_user_id = request.args.get('current_user_id')
        is_admin = request.args.get('is_admin', 'false').lower() == 'true'
        
        deleted_count = 0
        failed_ids = []
        
        for feedback_id in feedback_ids:
            try:
                feedback = Feedback.query.get(feedback_id)
                
                if not feedback:
                    failed_ids.append({'id': feedback_id, 'reason': '反馈不存在'})
                    continue
                
                # 检查权限
                if not is_admin and feedback.user != current_user_id:
                    failed_ids.append({'id': feedback_id, 'reason': '没有权限删除此反馈'})
                    continue
                
                # 删除反馈
                db.session.delete(feedback)
                deleted_count += 1
                
            except Exception as e:
                failed_ids.append({'id': feedback_id, 'reason': str(e)})
        
        # 提交所有删除操作
        db.session.commit()
        
        return success_response({
            'message': f'成功删除{deleted_count}条反馈',
            'deleted_count': deleted_count,
            'failed_count': len(failed_ids),
            'failed_ids': failed_ids
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'批量删除反馈失败: {str(e)}', 500)

@feedback_delete_bp.route('/<feedback_id>/soft_delete', methods=['DELETE'])
def soft_delete_feedback(feedback_id):
    """软删除反馈（标记为已关闭）"""
    try:
        feedback = Feedback.query.get(feedback_id)
        
        if not feedback:
            return error_response('反馈不存在', 404)
        
        # 获取当前用户ID（实际应用中应该从JWT token中解析）
        current_user_id = request.args.get('current_user_id')
        is_admin = request.args.get('is_admin', 'false').lower() == 'true'
        
        # 检查权限
        if not is_admin and feedback.user != current_user_id:
            return error_response('没有权限删除此反馈', 403)
        
        # 软删除：将状态设置为已关闭
        feedback.update_status('closed', current_user_id)
        
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
            'message': '反馈已软删除（状态已设置为已关闭）',
            'feedback': feedback_data
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'软删除反馈失败: {str(e)}', 500)

@feedback_delete_bp.route('/cleanup', methods=['DELETE'])
def cleanup_old_feedback():
    """清理旧反馈（管理员专用）"""
    try:
        # 获取当前用户ID（实际应用中应该从JWT token中解析）
        current_user_id = request.args.get('current_user_id')
        is_admin = request.args.get('is_admin', 'false').lower() == 'true'
        
        # 检查权限（只有管理员可以清理）
        if not is_admin:
            return error_response('只有管理员可以清理反馈', 403)
        
        data = request.get_json()
        days_old = data.get('days_old', 365)  # 默认清理一年前的反馈
        status_filter = data.get('status_filter', 'closed')  # 默认只清理已关闭的反馈
        
        if not isinstance(days_old, int) or days_old < 1:
            return error_response('天数必须是正整数', 400)
        
        # 计算截止日期
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        
        # 查询符合条件的反馈
        old_feedbacks = Feedback.query.filter(
            Feedback.status == status_filter,
            Feedback.createdAt < cutoff_date
        ).all()
        
        deleted_count = len(old_feedbacks)
        
        # 删除旧反馈
        for feedback in old_feedbacks:
            db.session.delete(feedback)
        
        db.session.commit()
        
        return success_response({
            'message': f'成功清理{deleted_count}条{status_filter}状态的旧反馈（{days_old}天前）',
            'deleted_count': deleted_count,
            'days_old': days_old,
            'status_filter': status_filter
        })
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'清理旧反馈失败: {str(e)}', 500)
