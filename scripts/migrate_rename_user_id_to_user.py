#!/usr/bin/env python3
"""
数据库迁移脚本：将history表中的user_id字段重命名为user
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db

def migrate_rename_user_id_to_user():
    """将history表中的user_id字段重命名为user"""
    app = create_app()
    with app.app_context():
        try:
            print("🔄 开始迁移：将history表中的user_id字段重命名为user...")
            
            # 检查history表是否存在
            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            if 'history' not in existing_tables:
                print("❌ history表不存在，跳过迁移")
                return
            
            # 检查字段是否存在
            columns = [col['name'] for col in inspector.get_columns('history')]
            
            if 'user_id' in columns and 'user' not in columns:
                # 重命名字段
                with db.engine.connect() as conn:
                    conn.execute(db.text("ALTER TABLE history RENAME COLUMN user_id TO user"))
                    conn.commit()
                print("✅ 字段重命名成功: user_id -> user")
            elif 'user' in columns:
                print("✅ user字段已存在，跳过重命名")
            else:
                print("❌ user_id字段不存在，无法重命名")
                return
            
            print("🎉 迁移完成!")
            
        except Exception as e:
            print(f"❌ 迁移失败: {str(e)}")
            raise

if __name__ == '__main__':
    migrate_rename_user_id_to_user()
