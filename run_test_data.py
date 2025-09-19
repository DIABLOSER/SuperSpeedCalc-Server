#!/usr/bin/env python3
"""
执行测试数据插入脚本
"""

import os
import sys
import sqlite3

def execute_sql_file(db_path, sql_file):
    """执行SQL文件"""
    print(f"正在执行 {sql_file}...")
    
    try:
        # 读取SQL文件
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 执行SQL语句
        cursor.executescript(sql_content)
        
        # 提交事务
        conn.commit()
        
        print(f"✅ {sql_file} 执行成功")
        
    except Exception as e:
        print(f"❌ {sql_file} 执行失败: {e}")
        return False
    finally:
        if conn:
            conn.close()
    
    return True

def main():
    """主函数"""
    print("🚀 开始插入测试数据...")
    print("=" * 50)
    
    # 数据库路径
    db_path = "instance/development/app_development.db"
    
    # 检查数据库文件是否存在
    if not os.path.exists(db_path):
        print(f"❌ 数据库文件不存在: {db_path}")
        print("请先运行 'python manage_db.py init' 初始化数据库")
        return
    
    # SQL文件列表
    sql_files = [
        "insert_test_data.sql",
        "insert_test_data_part2.sql", 
        "insert_test_data_part3.sql"
    ]
    
    # 执行所有SQL文件
    success_count = 0
    for sql_file in sql_files:
        if os.path.exists(sql_file):
            if execute_sql_file(db_path, sql_file):
                success_count += 1
        else:
            print(f"⚠️  SQL文件不存在: {sql_file}")
    
    print("=" * 50)
    if success_count == len(sql_files):
        print("🎉 所有测试数据插入完成！")
        
        # 显示数据统计
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # 统计各表记录数
            tables = [
                ('my_user', '用户'),
                ('charts', '图表'),
                ('posts', '帖子'),
                ('history', '历史记录'),
                ('user_relationships', '关注关系'),
                ('replies', '评论'),
                ('likes', '点赞'),
                ('banners', '横幅'),
                ('app_releases', '应用版本'),
                ('image', '图片')
            ]
            
            print("\n📊 数据统计：")
            total_records = 0
            for table, name in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   - {name}: {count} 条")
                total_records += count
            
            print(f"   - 总计: {total_records} 条记录")
            
        except Exception as e:
            print(f"⚠️  统计记录数时出错: {e}")
        finally:
            if conn:
                conn.close()
    else:
        print(f"❌ 只有 {success_count}/{len(sql_files)} 个文件执行成功")
    
    print("=" * 50)

if __name__ == '__main__':
    main()
