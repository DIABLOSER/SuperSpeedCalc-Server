import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from config import config
from models import db

def create_app(config_name='default'):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 允许路由末尾斜杠差异，不做 308 重定向
    app.url_map.strict_slashes = False
    
    # 初始化扩展
    db.init_app(app)
    CORS(app)
    
    # 注册蓝图 - 使用新的模块化结构
    from routes import user_bp, charts_bp, forum_bp, image_bp, history_bp
    
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(charts_bp, url_prefix='/api/charts')
    app.register_blueprint(forum_bp, url_prefix='/api/forum')
    app.register_blueprint(image_bp, url_prefix='/api/images')
    app.register_blueprint(history_bp, url_prefix='/api/history')
    
    # 静态文件：uploads/images 与兼容的 /static/images 映射
    uploads_dir = os.path.join(app.root_path, 'uploads', 'images')
    os.makedirs(uploads_dir, exist_ok=True)

    @app.route('/uploads/images/<path:filename>')
    def serve_uploaded_image(filename):
        return send_from_directory(uploads_dir, filename)

    @app.route('/static/images/<path:filename>')
    def serve_legacy_static_image(filename):
        return send_from_directory(uploads_dir, filename)
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    # 健康检查端点
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'SuperSpeedCalc Server is running'
        })
    
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
        from models import MyUser, Charts, Forum, Image, History
        
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
    app.run(host='0.0.0.0', port=5003, debug=True) 