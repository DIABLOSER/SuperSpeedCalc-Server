from .base import db, BaseModel
from .user import MyUser
from .chart import Charts
from .forum import Forum
from .image import Image

# 导出所有模型，方便其他文件导入
__all__ = ['db', 'BaseModel', 'MyUser', 'Charts', 'Forum', 'Image'] 