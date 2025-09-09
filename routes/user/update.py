from flask import request, jsonify
from models import db, MyUser
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from utils.response import (
    updated_response, bad_request_response, internal_error_response,
    not_found_response
)

def update_user(object_id):
    """更新用户信息"""
    try:
        user = MyUser.query.get_or_404(object_id)
        data = request.get_json()
        
        # 更新允许的字段（已移除 score 和 email）
        allowed_fields = ['avatar', 'bio', 'isActive', 'experience', 'boluo', 'admin', 'sex', 'mobile', 'username']
        for field in allowed_fields:
            if field in data:
                if field == 'mobile':
                    new_mobile = (data.get('mobile') or '').strip() if isinstance(data.get('mobile'), str) else data.get('mobile')
                    if new_mobile and new_mobile != user.mobile:
                        # 唯一性检查
                        if MyUser.query.filter_by(mobile=new_mobile).first():
                            return bad_request_response(
                                message='Mobile already exists'
                            )
                        setattr(user, 'mobile', new_mobile)
                    elif new_mobile == '':
                        setattr(user, 'mobile', None)
                elif field == 'username':
                    new_username = (data.get('username') or '').strip() if isinstance(data.get('username'), str) else data.get('username')
                    if not new_username:
                        return bad_request_response(
                            message='Username cannot be empty'
                        )
                    if new_username != user.username:
                        if MyUser.query.filter_by(username=new_username).first():
                            return bad_request_response(
                                message='Username already exists'
                            )
                        setattr(user, 'username', new_username)
                else:
                    setattr(user, field, data[field])
        
        # 解析并更新生日（可选，格式 YYYY-MM-DD）
        if 'birthday' in data:
            if data['birthday']:
                try:
                    user.birthday = datetime.strptime(data['birthday'], '%Y-%m-%d').date()
                except ValueError:
                    return bad_request_response(message='Invalid birthday format, expected YYYY-MM-DD')
            else:
                user.birthday = None
        
        # 特殊处理密码
        if 'password' in data:
            user.password = generate_password_hash(data['password'])
        
        user.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return updated_response(
            data=user.to_dict(),
            message="用户信息更新成功"
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message="更新用户信息失败")


def update_user_experience(object_id):
    """更新用户经验值"""
    try:
        user = MyUser.query.get_or_404(object_id)
        data = request.get_json()
        
        exp_change = data.get('exp_change', 0)
        user.experience += exp_change
        
        # 确保经验值不为负数
        if user.experience < 0:
            user.experience = 0
        
        user.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return updated_response(
            data=user.to_dict(),
            message=f'经验值更新成功，增加了 {exp_change} 点'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message="更新用户经验值失败")
        

def update_user_boluo(object_id):
    """更新用户菠萝币"""
    try:
        user = MyUser.query.get_or_404(object_id)
        data = request.get_json()
        
        boluo_change = data.get('boluo_change', 0)
        user.boluo += boluo_change
        
        # 确保菠萝币不为负数
        if user.boluo < 0:
            user.boluo = 0
        
        user.updatedAt = datetime.utcnow()
        db.session.commit()
        
        return updated_response(
            data=user.to_dict(),
            message=f'菠萝币更新成功，增加了 {boluo_change} 个'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message="更新用户菠萝币失败")
        

def update_user_password(object_id):
    """根据用户ID和旧密码更新密码"""
    try:
        user = MyUser.query.get_or_404(object_id)
        data = request.get_json()
        
        # 检查必需的参数
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            return bad_request_response(
                message='Both old_password and new_password are required'
            )
        
        # 验证旧密码是否正确
        if not check_password_hash(user.password, old_password):
            from utils.response import unauthorized_response
            return unauthorized_response(
                message='旧密码不正确'
            )
        
        # 验证新密码长度（可选的安全检查）
        if len(new_password) < 6:
            return bad_request_response(message='新密码至少需要6个字符')
        
        # 更新为新密码
        user.password = generate_password_hash(new_password)
        user.updatedAt = datetime.utcnow()
        
        db.session.commit()
        
        return updated_response(
            data={
                'id': user.id,
                'username': user.username,
                'updatedAt': user.updatedAt.isoformat()
            },
            message='密码更新成功'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message="密码更新失败")
        

def update_password_by_mobile():
    """根据手机号更新密码（客户端已验证短信验证码）"""
    try:
        data = request.get_json()
        
        # 检查必需的参数（支持 mobile 和 phone_number 两种参数名）
        mobile = data.get('mobile') or data.get('phone_number')
        new_password = data.get('new_password')
        
        if not mobile or not new_password:
            return bad_request_response(
                message='手机号和新密码都是必需的'
            )
        
        # 验证手机号格式
        if not mobile.isdigit() or len(mobile) != 11:
            return bad_request_response(
                message='手机号格式不正确'
            )
        
        # 验证新密码长度
        if len(new_password) < 6:
            return bad_request_response(message='新密码至少需要6个字符')
        
        # 查找用户
        user = MyUser.query.filter_by(mobile=mobile).first()
        if not user:
            return not_found_response(
                message='该手机号未注册'
            )
        
        # 更新密码
        user.password = generate_password_hash(new_password)
        user.updatedAt = datetime.utcnow()
        
        db.session.commit()
        
        return updated_response(
            data={
                'id': user.objectId,
                'username': user.username,
                'mobile': user.mobile,
                'updatedAt': user.updatedAt.isoformat()
            },
            message='密码更新成功'
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message="密码重置失败")
        
        