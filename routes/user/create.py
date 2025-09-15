from flask import request, jsonify
from models import db, MyUser
from werkzeug.security import generate_password_hash
from datetime import datetime
from utils.response import (
    created_response, bad_request_response, internal_error_response,
    success_response
)


# 用户信息类
class UserInfo:
    #在这里配置默认值
    avatar = "https://example.com/avatar.jpg"
    bio = "这个人很懒，什么都没留下"
    experience = 0
    boluo = 0
    isActive = True
    admin = False
    sex = 1
    birthday = None
    
    
# 生成用户名：形容词+名词+时间戳后6位
def generate_android_style_username():
    """
    按安卓端逻辑生成用户名：形容词+名词+时间戳后6位
    
    Returns:
        str: 由形容词、名词和时间戳后6位组成的用户名字符串
    """
    # 预定义形容词列表
    adjectives = [
        "快乐", "可爱", "安静", "勇敢", "活力", "调皮", "酷酷", "温柔", "机智", "慵懒"
    ]
    # 预定义名词列表
    nouns = [
        "小熊", "小猫", "星星", "云朵", "花朵", "风铃", "叶子", "火箭", "雪糕", "糖果"
    ]
    import time, random
    # 随机选择形容词和名词
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    # 获取当前时间戳的后6位作为唯一标识
    timestamp_part = str(int(time.time() * 1000) % 1000000).zfill(6)
    return f"{adjective}{noun}{timestamp_part}"

# 创建用户
def create_user():
    """创建新用户（后台管理用，支持完整字段）"""
    try:
        data = request.get_json()
        
        # 验证必填字段：username、password、mobile
        required_fields = ['username', 'password', 'mobile']
        for field in required_fields:
            if field not in data:
                return bad_request_response(
                    message=f'{field} is required',
                    data={'field': field}
                )
        
        mobile_value = (data.get('mobile') or '').strip() if isinstance(data.get('mobile'), str) else data.get('mobile')
        if not mobile_value:
            return bad_request_response(
                message='Mobile is required',
                # error_code='MISSING_MOBILE'
            )
        
        # 检查用户名是否已存在
        if MyUser.query.filter_by(username=data['username']).first():
            return bad_request_response(
                message='Username already exists',
                # error_code='DUPLICATE_USERNAME'
            )
        
        # 检查手机号是否已存在
        if mobile_value:
            if MyUser.query.filter_by(mobile=mobile_value).first():
                return bad_request_response(
                    message='Mobile already exists',
                    # error_code='DUPLICATE_MOBILE'
                )
        
        # 解析生日（可选，格式 YYYY-MM-DD）
        birthday_value = None
        if 'birthday' in data and data['birthday']:
            try:
                birthday_value = datetime.strptime(data['birthday'], '%Y-%m-%d').date()
            except ValueError:
                return bad_request_response(
                    message='Invalid birthday format, expected YYYY-MM-DD',
                    # error_code='INVALID_DATE_FORMAT',
                    # details={'field': 'birthday', 'expected_format': 'YYYY-MM-DD'}
                )
        
        # 创建新用户
        user = MyUser(
            username=data['username'],
            password=generate_password_hash(data['password']),
            avatar=data.get('avatar'),
            bio=data.get('bio'),
            experience=data.get('experience', 0),
            boluo=data.get('boluo', 0),
            isActive=data.get('isActive', True),
            admin=data.get('admin', False),
            sex=data.get('sex', 1),
            birthday=birthday_value,
            mobile=mobile_value
        )
        
        db.session.add(user)
        db.session.commit()
        
        return created_response(
            data=user.to_dict(),
            message="用户创建成功"
        )
        
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message="创建用户失败")

def register_user():
    """注册新用户（客户端/安卓端用，仅需邮箱或手机号 + 密码）"""
    try:
        data = request.get_json() or {}
        password = data.get('password')
        if not password:
            return bad_request_response(
                message='Password is required',
                # error_code='MISSING_PASSWORD'
            )
        
        mobile_value = (data.get('mobile') or '').strip() if isinstance(data.get('mobile'), str) else data.get('mobile')
        if not mobile_value:
            return bad_request_response(
                message='Mobile is required',
                # error_code='MISSING_MOBILE'
            )
    
        # 唯一性检查
        if MyUser.query.filter_by(mobile=mobile_value).first():
            return bad_request_response(
                message='Mobile already exists',
                # error_code='DUPLICATE_MOBILE'
            )
        
        # 生成用户名（安卓端逻辑）
        base_username = generate_android_style_username()
        
        # 保证唯一：若冲突则添加随机后缀重试
        username_candidate = base_username
        if MyUser.query.filter_by(username=username_candidate).first():
            import random, string
            for _ in range(10):
                suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
                username_candidate = f"{base_username}_{suffix}"
                if not MyUser.query.filter_by(username=username_candidate).first():
                    break
        
        user = MyUser(
            username=username_candidate,
            mobile=mobile_value,
            password=generate_password_hash(password),
            avatar=UserInfo.avatar,
            bio=UserInfo.bio,
            experience=UserInfo.experience,
            boluo=UserInfo.boluo,
            isActive=UserInfo.isActive,
            admin=UserInfo.admin,
            sex=UserInfo.sex,
            birthday=UserInfo.birthday
        )
        db.session.add(user)
        db.session.commit()
        
        return created_response(
            data=user.to_dict(),
            message="用户注册成功"
        )
    except Exception as e:
        db.session.rollback()
        return internal_error_response(message="用户注册失败")

def login():
    """用户登录"""
    try:
        from werkzeug.security import check_password_hash
        
        data = request.get_json() or {}
        mobile = (data.get('mobile') or '').strip() if isinstance(data.get('mobile'), str) else data.get('mobile')
        password = data.get('password')
        
        if not password:
            return bad_request_response(
                message='Password is required',
                # error_code='MISSING_PASSWORD'
            )
        if not mobile:
            return bad_request_response(
                message='Mobile is required',
                # error_code='MISSING_MOBILE'
            )
        
        user = MyUser.query.filter_by(mobile=mobile).first()
        
        if user and check_password_hash(user.password, password):
            return success_response(
                data=user.to_dict(),
                message='登录成功'
            )
        else:
            from utils.response import unauthorized_response
            return unauthorized_response(
                message='用户名或密码错误'
            )
            
    except Exception as e:
        return internal_error_response(message="登录失败")
        