from .base import db, BaseModel

class Image(BaseModel):
    """图片表 - 存储图片信息"""
    __tablename__ = 'image'
    
    # 图片文件名，最大255字符，不可为空
    fileName = db.Column(db.String(255), nullable=False)
    
    # 图片本地路径，最大500字符，不可为空，存储服务器上的文件路径
    path = db.Column(db.String(500), nullable=False)
    
    # 图片访问URL，最大500字符，不可为空，用于前端访问
    url = db.Column(db.String(500), nullable=False)
    
    # 文件大小，整数类型，单位为字节，可为空
    fileSize = db.Column(db.Integer)
    
    # 文件类型，最大50字符，可为空，如：image/jpeg, image/png
    fileType = db.Column(db.String(50))
    
    # 图片宽度，整数类型，可为空，单位像素
    width = db.Column(db.Integer)
    
    # 图片高度，整数类型，可为空，单位像素
    height = db.Column(db.Integer)
    
    # 图片描述，文本类型，可为空，用于图片说明
    description = db.Column(db.Text)
    
    # 外键：关联用户表的objectId，可为空，表示图片的上传者
    user = db.Column(db.String(20), db.ForeignKey('my_user.objectId'))
    
    def __repr__(self):
        return f'<Image {self.fileName}>' 