from .base import db, BaseModel


class AppRelease(BaseModel):
    """应用发布版本表"""
    __tablename__ = 'app_releases'

    # 应用名称
    title = db.Column(db.String(100), nullable=False)

    # 版本号（展示用，如 1.2.3）
    version_name = db.Column(db.String(50), nullable=False)

    # 版本代码（整数，自增或手动维护例如版本1.2.3则版本号为123）
    version_code = db.Column(db.Integer, nullable=False)

    # 更新内容
    content = db.Column(db.Text)

    # 下载链接
    download_url = db.Column(db.String(255))

    # 发布环境（例如 测试，taptap，正式）
    environment = db.Column(db.Text)


    #是否测试（测试版本，不对外发布）
    is_test = db.Column(db.Boolean, default=False)

    # 是否更新（客户端是否需要提示更新）
    is_update = db.Column(db.Boolean, default=False)

    # 是否强制更新
    force_update = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<AppRelease {self.title} {self.version_name} ({self.version_code})>"


