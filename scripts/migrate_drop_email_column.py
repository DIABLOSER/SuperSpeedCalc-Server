#!/usr/bin/env python3
"""
数据库迁移脚本：删除用户表中的email字段
"""

import os
import sys
import sqlite3
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def migrate_drop_email_column():
    """删除用户表中的email字段"""
    
    # 数据库文件路径
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        return False
    
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔄 开始删除用户表中的email字段...")
        
        # 检查email字段是否存在
        cursor.execute("PRAGMA table_info(my_user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'email' not in columns:
            print("ℹ️  email字段不存在，无需删除")
            conn.close()
            return True
        
        print("📋 当前用户表结构:")
        for column in columns:
            print(f"   - {column}")
        
        # 创建备份表（不包含email字段）
        print("🔄 创建新的用户表结构...")
        cursor.execute("""
            CREATE TABLE my_user_new (
                objectId TEXT PRIMARY KEY,
                createdAt DATETIME,
                updatedAt DATETIME,
                username VARCHAR(50) UNIQUE NOT NULL,
                mobile VARCHAR(20) UNIQUE,
                password VARCHAR(255) NOT NULL,
                avatar VARCHAR(255),
                bio TEXT,
                experience INTEGER DEFAULT 0,
                boluo INTEGER DEFAULT 0,
                isActive BOOLEAN DEFAULT 1,
                admin BOOLEAN DEFAULT 0,
                sex INTEGER DEFAULT 1,
                birthday DATE
            )
        """)
        
        # 复制数据（排除email字段）
        print("🔄 复制数据到新表...")
        cursor.execute("""
            INSERT INTO my_user_new (
                objectId, createdAt, updatedAt, username, mobile, password,
                avatar, bio, experience, boluo, isActive, admin, sex, birthday
            )
            SELECT 
                objectId, createdAt, updatedAt, username, mobile, password,
                avatar, bio, experience, boluo, isActive, admin, sex, birthday
            FROM my_user
        """)
        
        # 删除旧表
        print("🔄 删除旧表...")
        cursor.execute("DROP TABLE my_user")
        
        # 重命名新表
        print("🔄 重命名新表...")
        cursor.execute("ALTER TABLE my_user_new RENAME TO my_user")
        
        # 提交更改
        conn.commit()
        
        # 验证新表结构
        cursor.execute("PRAGMA table_info(my_user)")
        new_columns = [column[1] for column in cursor.fetchall()]
        
        print("✅ 迁移完成！新的用户表结构:")
        for column in new_columns:
            print(f"   - {column}")
        
        # 检查数据完整性
        cursor.execute("SELECT COUNT(*) FROM my_user")
        user_count = cursor.fetchone()[0]
        print(f"📊 用户数据完整性检查: {user_count} 个用户记录")
        
        conn.close()
        print("✅ email字段删除成功！")
        return True
        
    except Exception as e:
        print(f"❌ 迁移失败: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("🗃️  数据库迁移：删除用户表email字段")
    print("=" * 50)
    
    # 确认操作
    confirm = input("⚠️  此操作将删除用户表中的email字段，是否继续？(y/N): ")
    if confirm.lower() != 'y':
        print("❌ 操作已取消")
        return
    
    # 执行迁移
    success = migrate_drop_email_column()
    
    if success:
        print("\n🎉 迁移完成！")
        print("📝 注意事项:")
        print("   - 用户表中的email字段已被删除")
        print("   - 所有用户数据已保留（除email字段外）")
        print("   - 请更新相关的API接口和前端代码")
    else:
        print("\n💥 迁移失败！")
        print("请检查错误信息并重试")

if __name__ == "__main__":
    main()
