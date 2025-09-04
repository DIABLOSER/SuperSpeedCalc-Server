from .base import db, BaseModel

class MyUser(BaseModel):
    """用户表 - 存储系统用户信息"""
    __tablename__ = 'my_user'
    
    # 用户名，最大50字符，唯一且不可为空，用于登录和显示
    username = db.Column(db.String(50), unique=True, nullable=False)
    
    # 邮箱地址，最大100字符，唯一，可为空，用于登录和通知
    email = db.Column(db.String(100), unique=True, nullable=True)
    
    # 手机号，最大20字符，唯一且可为空
    mobile = db.Column(db.String(20), unique=True)
    
    # 用户密码，最大255字符，不可为空，存储加密后的密码
    password = db.Column(db.String(255), nullable=False)
    
    # 用户头像地址，最大255字符，可为空
    avatar = db.Column(db.String(255))
    
    # 用户个人简介，文本类型，可为空，用于个人资料展示
    bio = db.Column(db.Text)
    
    
    
    # 用户经验值，整数类型，默认0，用于记录用户的经验积累
    experience = db.Column(db.Integer, default=0)
    
    # 菠萝数量，整数类型，默认0，用于记录用户的菠萝币或特殊货币
    boluo = db.Column(db.Integer, default=0)
    
    # 用户状态，布尔类型，默认True，表示账户是否处于激活状态
    isActive = db.Column(db.Boolean, default=True)
    
    # 新增：是否管理员，布尔类型，默认False
    admin = db.Column(db.Boolean, default=False)
    
    # 新增：性别，1 表示男，0 表示女，默认 1
    sex = db.Column(db.Integer, default=1)
    
    # 新增：生日，日期类型，可为空（格式建议 YYYY-MM-DD）
    birthday = db.Column(db.Date)
    
    # 关系定义：用户拥有的图表列表，级联删除（删除用户时删除其所有图表）
    charts = db.relationship('Charts', backref='user_ref', lazy=True, cascade='all, delete-orphan')
    
    # 关系定义：用户发布的论坛帖子列表，级联删除（删除用户时删除其所有帖子）
    forum_posts = db.relationship('Forum', backref='user_ref', lazy=True, cascade='all, delete-orphan')
    
    # 关系定义：用户的历史记录列表，级联删除（删除用户时删除其所有历史记录）
    histories = db.relationship('History', backref='user_ref', lazy=True, cascade='all, delete-orphan')
    
    def get_followers(self):
        """获取关注此用户的用户列表"""
        from .relationship import UserRelationship
        return db.session.query(MyUser).join(
            UserRelationship, MyUser.objectId == UserRelationship.follower
        ).filter(UserRelationship.followed == self.objectId).all()
    
    def get_following(self):
        """获取此用户关注的用户列表"""
        from .relationship import UserRelationship
        return db.session.query(MyUser).join(
            UserRelationship, MyUser.objectId == UserRelationship.followed
        ).filter(UserRelationship.follower == self.objectId).all()
    
    def is_following(self, user_id):
        """检查是否关注某个用户"""
        from .relationship import UserRelationship
        return UserRelationship.query.filter_by(
            follower=self.objectId,
            followed=user_id
        ).first() is not None
    
    def get_followers_count(self):
        """获取粉丝数量"""
        from .relationship import UserRelationship
        return UserRelationship.query.filter_by(followed=self.objectId).count()
    
    def get_following_count(self):
        """获取关注数量"""
        from .relationship import UserRelationship
        return UserRelationship.query.filter_by(follower=self.objectId).count()
    
    def to_dict(self, include_stats=False):
        """重写to_dict方法，可选择包含关注统计信息"""
        result = super().to_dict()
        # 移除敏感信息
        if 'password' in result:
            del result['password']
        
        # 如果需要包含统计信息
        if include_stats:
            result['followers_count'] = self.get_followers_count()
            result['following_count'] = self.get_following_count()
        
        return result
    
    def __repr__(self):
        return f'<MyUser {self.username}>' 