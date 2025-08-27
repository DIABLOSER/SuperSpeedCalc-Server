#!/usr/bin/env python3
"""
数据库迁移脚本：添加 app_releases 表
运行方式：python scripts/migrate_add_releases_table.py
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, AppRelease


def migrate_add_releases_table():
    app = create_app()
    with app.app_context():
        try:
            print("🔄 开始迁移：添加 app_releases 表...")

            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            if 'app_releases' in existing_tables:
                print("✅ app_releases 表已存在，跳过创建")
                return

            AppRelease.__table__.create(db.engine)
            print("✅ app_releases 表创建成功!")
            print("🎉 迁移完成!")
        except Exception as e:
            print(f"❌ 迁移失败: {e}")
            raise


if __name__ == '__main__':
    migrate_add_releases_table()


