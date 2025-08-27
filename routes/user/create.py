from flask import request, jsonify
from models import db, MyUser
from werkzeug.security import generate_password_hash
from datetime import datetime


# 用户信息类
class UserInfo:
    #在这里配置默认值
    avatar = "https://example.com/avatar.jpg"
    bio = "这个人很懒，什么都没留下"
    score = 0
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

def create_user():
    """创建新用户（后台管理用，支持完整字段）"""
    try:
        data = request.get_json()
        
        # 验证必填字段：username、password，且 email 或 mobile 至少提供一个
        required_fields = ['username', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'{field} is required'}), 400
        
        email_value = (data.get('email') or '').strip() if isinstance(data.get('email'), str) else data.get('email')
        mobile_value = (data.get('mobile') or '').strip() if isinstance(data.get('mobile'), str) else data.get('mobile')
        if not email_value and not mobile_value:
            return jsonify({'success': False, 'error': 'Either email or mobile is required'}), 400
        
        # 检查用户名是否已存在
        if MyUser.query.filter_by(username=data['username']).first():
            return jsonify({'success': False, 'error': 'Username already exists'}), 400
        
        # 可选：检查邮箱是否已存在
        if email_value:
            if MyUser.query.filter_by(email=email_value).first():
                return jsonify({'success': False, 'error': 'Email already exists'}), 400
        
        # 可选：检查手机号是否已存在
        if mobile_value:
            if MyUser.query.filter_by(mobile=mobile_value).first():
                return jsonify({'success': False, 'error': 'Mobile already exists'}), 400
        
        # 解析生日（可选，格式 YYYY-MM-DD）
        birthday_value = None
        if 'birthday' in data and data['birthday']:
            try:
                birthday_value = datetime.strptime(data['birthday'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'success': False, 'error': 'Invalid birthday format, expected YYYY-MM-DD'}), 400
        
        # 创建新用户
        user = MyUser(
            username=data['username'],
            email=email_value,
            password=generate_password_hash(data['password']),
            avatar=data.get('avatar'),
            bio=data.get('bio'),
            score=data.get('score', 0),
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
        
        return jsonify({
            'success': True,
            'data': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def register_user():
    """注册新用户（客户端/安卓端用，仅需邮箱或手机号 + 密码；可选提供 username）"""
    try:
        data = request.get_json() or {}
        password = data.get('password')
        if not password:
            return jsonify({'success': False, 'error': 'Password is required'}), 400
        
        email_value = (data.get('email') or '').strip() if isinstance(data.get('email'), str) else data.get('email')
        mobile_value = (data.get('mobile') or '').strip() if isinstance(data.get('mobile'), str) else data.get('mobile')
        if not email_value and not mobile_value:
            return jsonify({'success': False, 'error': 'Either email or mobile is required'}), 400
        
        # 唯一性检查
        if email_value and MyUser.query.filter_by(email=email_value).first():
            return jsonify({'success': False, 'error': 'Email already exists'}), 400
        if mobile_value and MyUser.query.filter_by(mobile=mobile_value).first():
            return jsonify({'success': False, 'error': 'Mobile already exists'}), 400
        
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
            email=email_value,
            mobile=mobile_value,
            password=generate_password_hash(password),
            avatar=UserInfo.avatar,
            bio=UserInfo.bio,
            score=UserInfo.score,
            experience=UserInfo.experience,
            boluo=UserInfo.boluo,
            isActive=UserInfo.isActive,
            admin=UserInfo.admin,
            sex=UserInfo.sex,
            birthday=UserInfo.birthday
        )
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'success': True, 'data': user.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def login():
    """用户登录"""
    try:
        from werkzeug.security import check_password_hash
        
        data = request.get_json() or {}
        email = (data.get('email') or '').strip() if isinstance(data.get('email'), str) else data.get('email')
        mobile = (data.get('mobile') or '').strip() if isinstance(data.get('mobile'), str) else data.get('mobile')
        password = data.get('password')
        
        if not password:
            return jsonify({'success': False, 'error': 'Password is required'}), 400
        if not email and not mobile:
            return jsonify({'success': False, 'error': 'Email or mobile is required'}), 400
        
        user = None
        if email:
            user = MyUser.query.filter_by(email=email).first()
        elif mobile:
            user = MyUser.query.filter_by(mobile=mobile).first()
        
        if user and check_password_hash(user.password, password):
            return jsonify({
                'success': True,
                'data': user.to_dict(),
                'message': 'Login successful'
            })
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500 