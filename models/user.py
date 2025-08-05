from .base import db, BaseModel

class MyUser(BaseModel):
    """用户表 - 存储系统用户信息"""
    __tablename__ = 'my_user'
    
    # 用户名，最大50字符，唯一且不可为空，用于登录和显示
    username = db.Column(db.String(50), unique=True, nullable=False)
    
    # 邮箱地址，最大100字符，唯一且不可为空，用于登录和通知
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    # 用户密码，最大255字符，不可为空，存储加密后的密码
    password = db.Column(db.String(255), nullable=False)
    
    # 用户昵称，最大50字符，可为空，用于显示用户友好名称
    nickname = db.Column(db.String(50))
    
    # 用户头像地址，最大255字符，可为空
    avatar = db.Column(db.String(255))
    
    # 用户个人简介，文本类型，可为空，用于个人资料展示
    bio = db.Column(db.Text)
    
    # 用户积分，整数类型，默认0，用于记录用户的积分数量
    score = db.Column(db.Integer, default=0)
    
    # 用户经验值，整数类型，默认0，用于记录用户的经验积累
    experence = db.Column(db.Integer, default=0)
    
    # 菠萝数量，浮点数类型，默认0.0，用于记录用户的菠萝币或特殊货币
    boluo = db.Column(db.Float, default=0.0)
    
    # 用户状态，布尔类型，默认True，表示账户是否处于激活状态
    isActive = db.Column(db.Boolean, default=True)
    
    # 最后登录时间，可为空，记录用户最近一次登录的时间
    lastLogin = db.Column(db.DateTime)
    
    # 关系定义：用户拥有的图表列表，级联删除（删除用户时删除其所有图表）
    charts = db.relationship('Charts', backref='user_ref', lazy=True, cascade='all, delete-orphan')
    
    # 关系定义：用户发布的论坛帖子列表，级联删除（删除用户时删除其所有帖子）
    forum_posts = db.relationship('Forum', backref='user_ref', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<MyUser {self.username}>' 