import os
import logging
from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from config import config
from models import db

def configure_logging(app):
    """配置详细日志"""
    if not app.debug and not app.testing:
        # 生产环境：只记录到文件
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = logging.FileHandler('logs/app.log')
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('应用启动')
    else:
        # 开发环境：同时输出到控制台和文件
        # 控制台日志
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        app.logger.addHandler(console_handler)
        
        # 文件日志
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = logging.FileHandler('logs/app.log')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(file_formatter)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.DEBUG)
        app.logger.info('应用启动 (开发模式)')

def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 配置详细日志
    configure_logging(app)
    
    # 允许路由末尾斜杠差异，不做 308 重定向
    app.url_map.strict_slashes = False
    
    # 初始化扩展
    db.init_app(app)
    
    # CORS 配置 - 仅在本地开发环境启用，部署到服务器时禁用
    if app.config.get('DEBUG', False) and app.config.get('ENV') != 'production':
        CORS(app)
    
    # 添加请求日志中间件
    @app.before_request
    def log_request_info():
        app.logger.info(f'请求: {request.method} {request.url}')
        app.logger.info(f'请求头: {dict(request.headers)}')
        if request.is_json:
            app.logger.info(f'请求体: {request.get_json()}')
        elif request.form:
            app.logger.info(f'表单数据: {dict(request.form)}')
    
    @app.after_request
    def log_response_info(response):
        app.logger.info(f'响应状态: {response.status_code}')
        app.logger.info(f'响应头: {dict(response.headers)}')
        return response
    
    # 注册蓝图 - 使用新的模块化结构
    from routes import user_bp, charts_bp, image_bp, history_bp, releases_bp, posts_bp, replies_bp, banners_bp, likes_bp
    from routes.sms import sms_bp
    from routes.relationships import relationships_bp
    from routes.collect import collect_bp
    from routes.feedback import feedback_bp
    
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(charts_bp, url_prefix='/charts')
    app.register_blueprint(image_bp, url_prefix='/images')
    app.register_blueprint(history_bp, url_prefix='/history')
    app.register_blueprint(releases_bp, url_prefix='/releases')
    app.register_blueprint(relationships_bp, url_prefix='/relationships')  # 新的关注关系路由
    app.register_blueprint(posts_bp, url_prefix='/posts')
    app.register_blueprint(replies_bp, url_prefix='/replies')
    app.register_blueprint(banners_bp, url_prefix='/banners')
    app.register_blueprint(likes_bp, url_prefix='/likes')
    app.register_blueprint(collect_bp, url_prefix='/collect')
    app.register_blueprint(feedback_bp)  # 反馈路由，URL前缀已在蓝图中定义
    app.register_blueprint(sms_bp, url_prefix='/sms')
    
    # 静态文件：uploads/images 与 /uploads/apk
    uploads_dir = os.path.join(app.root_path, 'uploads', 'images')
    os.makedirs(uploads_dir, exist_ok=True)
    uploads_apk_dir = os.path.join(app.root_path, 'uploads', 'apk')
    os.makedirs(uploads_apk_dir, exist_ok=True)

    @app.route('/uploads/images/<path:filename>')
    def serve_uploaded_image(filename):
        return send_from_directory(uploads_dir, filename)

    @app.route('/static/images/<path:filename>')
    def serve_legacy_static_image(filename):
        return send_from_directory(uploads_dir, filename)

    @app.route('/uploads/apk/<path:filename>')
    def serve_uploaded_apk(filename):
        return send_from_directory(uploads_apk_dir, filename)
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        from utils.response import error_response
        return error_response(message='Not found', code=404)
    
    @app.errorhandler(500)
    def internal_error(error):
        from utils.response import error_response
        return error_response(message='Internal server error', code=500)
    
    # 健康检查端点
    @app.route('/health')
    def health_check():
        from utils.response import success_response
        return success_response(
            data={'status': 'healthy'},
            message='SuperSpeedCalc Server is running'
        )
    
    return app

def check_database_exists(app):
    """检查数据库文件是否存在"""
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    if db_uri.startswith('sqlite:///'):
        # 处理SQLite数据库路径
        db_path = db_uri.replace('sqlite:///', '')
        if not os.path.isabs(db_path):  # 相对路径
            db_path = os.path.join(app.instance_path, db_path)
        return os.path.exists(db_path), db_path
    else:
        # 非SQLite数据库，无法简单检查文件
        return False, None

def init_db(app, force=False):
    """智能初始化数据库"""
    with app.app_context():
        # 导入所有模型以确保它们被注册
        from models import MyUser, Charts, Image, History, AppRelease, UserRelationship, Posts, Likes, Reply, Banner, Feedback
        
        db_exists, db_path = check_database_exists(app)
        
        if force:
            print("🔄 强制重新创建数据库...")
            db.drop_all()
            db.create_all()
            print("✅ 数据库已重新创建!")
        elif db_exists:
            print(f"✅ 数据库已存在: {db_path}")
            # 检查表是否完整，如果有新表会自动创建
            db.create_all()
            print("✅ 已验证所有表结构完整")
        else:
            print(f"🆕 创建新数据库: {db_path}")
            # 确保instance目录存在
            if db_path:
                os.makedirs(os.path.dirname(db_path), exist_ok=True)
            db.create_all()
            print("✅ 数据库和表创建成功!")

def init_db_force(app):
    """强制重新创建数据库（危险操作，会删除所有数据）"""
    print("⚠️  警告: 这将删除所有现有数据!")
    confirm = input("确定要继续吗? (yes/no): ")
    if confirm.lower() == 'yes':
        init_db(app, force=True)
    else:
        print("❌ 操作已取消")

if __name__ == '__main__':
    import sys
    
    app = create_app('development')
    
    # 检查命令行参数
    if '--init-db' in sys.argv:
        print("🔧 正在初始化数据库...")
        init_db(app)
        print("✅ 数据库初始化完成")
        sys.exit(0)
    elif '--reset-db' in sys.argv:
        print("🔧 正在重置数据库...")
        init_db_force(app)
        sys.exit(0)
    
    # 正常启动时只检查数据库是否存在，不强制创建
    db_exists, db_path = check_database_exists(app)
    if not db_exists:
        print("⚠️  未找到数据库文件!")
        print("💡 使用 'python app.py --init-db' 来初始化数据库")
        print("🚀 继续启动服务器...")
    else:
        print(f"✅ 数据库文件存在: {db_path}")
    
    # 启动应用
    print("🚀 启动 SuperSpeedCalc Server...")
    app.run(host='0.0.0.0', port=8000, debug=True) 