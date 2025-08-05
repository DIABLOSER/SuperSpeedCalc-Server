from .base import db, BaseModel

class Charts(BaseModel):
    """排行榜表 - 存储用户创建的图表信息"""
    __tablename__ = 'charts'
    
    # 标题，最大100字符，不可为空，用于显示图表名称
    title = db.Column(db.String(100), nullable=False)
    
    # 成绩值，浮点数类型，默认0.0，用于记录用户的成就分数
    achievement = db.Column(db.Float, default=0.0)
    
    # 外键：关联用户表的objectId，不可为空，表示图表的创建者
    user = db.Column(db.String(20), db.ForeignKey('my_user.objectId'), nullable=False)
    
    def __repr__(self):
        return f'<Charts {self.title}>' 