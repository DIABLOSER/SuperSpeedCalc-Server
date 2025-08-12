from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import string
import random

# 创建数据库实例
db = SQLAlchemy()

def generate_object_id():
    """生成类似 d88702553a 的 objectId"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

class BaseModel(db.Model):
    """基础模型，包含公共字段"""
    __abstract__ = True
    
    # 主键ID，自动生成10位随机字符串，类似 d88702553a 格式
    objectId = db.Column(db.String(20), primary_key=True, default=generate_object_id)
    
    # 记录创建时间，自动设置为当前UTC时间，不可为空
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # 记录更新时间，创建时设置为当前时间，每次更新时自动更新
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        """将模型转换为字典"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, (datetime, date)):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value
        return result 