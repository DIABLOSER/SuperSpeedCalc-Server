#!/usr/bin/env python3
"""
SuperSpeedCalc Server 启动脚本
"""

import os
import sys
from app import create_app, init_db

def check_dependencies():
    """检查必要的依赖是否已安装"""
    try:
        import flask
        import flask_sqlalchemy
        import flask_cors
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def main():
    """主函数"""
    print("🚀 SuperSpeedCalc Server 启动脚本")
    print("=" * 40)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 设置环境变量
    os.environ.setdefault('FLASK_ENV', 'development')
    
    # 创建应用
    app = create_app('development')
    
    # 初始化数据库
    print("📦 初始化数据库...")
    init_db(app)
    
    print("\n🌟 服务器启动中...")
    print("📍 访问地址: http://localhost:5000")
    print("🔍 健康检查: http://localhost:5000/health")
    print("📚 API 文档请查看 README.md")
    print("\n按 Ctrl+C 停止服务器")
    print("=" * 40)
    
    # 启动服务器
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")

if __name__ == '__main__':
    main() 