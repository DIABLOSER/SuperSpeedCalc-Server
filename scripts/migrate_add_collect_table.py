#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库迁移脚本：添加收藏表
创建时间: 2024
描述: 添加用户收藏帖子的功能表
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, Collect

def migrate_add_collect_table():
    """添加收藏表"""
    app = create_app('development')
    with app.app_context():
        try:
            # 创建收藏表
            db.create_all()
            print("✅ 收藏表创建成功")
            
            # 验证表是否创建成功
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            if inspector.has_table('collect'):
                print("✅ 收藏表验证成功")
            else:
                print("❌ 收藏表创建失败")
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ 迁移失败: {str(e)}")
            return False

if __name__ == '__main__':
    print("开始执行收藏表迁移...")
    success = migrate_add_collect_table()
    
    if success:
        print("🎉 收藏表迁移完成！")
    else:
        print("💥 收藏表迁移失败！")
        sys.exit(1)
