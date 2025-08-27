from .base import db, BaseModel


class AppRelease(BaseModel):
    """应用发布版本表"""
    __tablename__ = 'app_releases'

    # 应用名称
    app_name = db.Column(db.String(100), nullable=False)

    # 版本号（展示用，如 1.2.3）
    version_name = db.Column(db.String(50), nullable=False)

    # 版本代码（整数，自增或手动维护）
    version_code = db.Column(db.Integer, nullable=False)

    # 更新内容
    changelog = db.Column(db.Text)

    # 下载链接
    download_url = db.Column(db.String(255))

    # 发布环境（例如 development / production / staging 等）
    environment = db.Column(db.String(50), nullable=False, default='production')

    # 发布状态（例如 draft/published/deprecated）
    status = db.Column(db.String(50), nullable=False, default='published')

    # 是否更新（客户端是否需要提示更新）
    is_update = db.Column(db.Boolean, default=False)

    # 是否强制更新
    force_update = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<AppRelease {self.app_name} {self.version_name} ({self.version_code})>"


