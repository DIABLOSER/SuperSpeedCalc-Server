from .base import db, BaseModel

class History(BaseModel):
    """历史记录表 - 存储用户的历史记录信息"""
    __tablename__ = 'history'
    
    # 标题，最大200字符，不可为空，用于描述历史记录的内容
    title = db.Column(db.String(200), nullable=False)
    
    # 数值范围，整数类型，可以为正数或负数，不可为空，用于记录相关的数值
    scope = db.Column(db.Integer, nullable=False)
    
    # 用户ID，外键关联到my_user表的objectId，不可为空
    user_id = db.Column(db.String(20), db.ForeignKey('my_user.objectId'), nullable=False)
    
    # 关系定义：关联的用户对象
    user = db.relationship('MyUser', backref='histories')
    
    def __repr__(self):
        return f'<History {self.title}>'
