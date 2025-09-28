#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库迁移脚本：添加意见反馈表
创建时间：2024年
功能：创建feedback表，用于存储用户反馈信息
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, Feedback

def migrate_add_feedback_table():
    """添加意见反馈表"""
    app = create_app()
    
    with app.app_context():
        try:
            print("开始创建意见反馈表...")
            
            # 创建feedback表
            db.create_all()
            
            print("✅ 意见反馈表创建成功！")
            print("📋 表结构信息：")
            print("   - 表名: feedback")
            print("   - 主键: objectId (10位随机字符串)")
            print("   - 时间字段: createdAt, updatedAt")
            print("   - 用户关联: user (外键到my_user.objectId)")
            print("   - 反馈类型: feedback_type (bug/feature/complaint/praise/other)")
            print("   - 标题: title (最大200字符)")
            print("   - 内容: content (文本)")
            print("   - 状态: status (pending/processing/resolved/closed)")
            print("   - 优先级: priority (low/medium/high/urgent)")
            print("   - 联系方式: contact (最大100字符)")
            print("   - 设备信息: device_info (JSON)")
            print("   - 应用版本: app_version (最大50字符)")
            print("   - 操作系统: os_info (最大100字符)")
            print("   - 附件: attachments (JSON数组)")
            print("   - 管理员回复: admin_reply (文本)")
            print("   - 管理员回复时间: admin_reply_at (时间)")
            print("   - 处理管理员: admin_user (外键到my_user.objectId)")
            print("   - 评分: rating (1-5分)")
            print("   - 是否公开: is_public (布尔)")
            print("   - 标签: tags (JSON数组)")
            
            print("\n🎯 功能特性：")
            print("   - 支持匿名反馈（user字段可为空）")
            print("   - 多种反馈类型分类")
            print("   - 完整的状态管理流程")
            print("   - 优先级管理")
            print("   - 设备信息收集")
            print("   - 附件上传支持")
            print("   - 管理员回复功能")
            print("   - 用户评分系统")
            print("   - 标签分类管理")
            print("   - 权限控制（查看/编辑）")
            print("   - 统计信息支持")
            
            print("\n📊 可用的反馈类型：")
            for key, value in Feedback.get_feedback_types().items():
                print(f"   - {key}: {value}")
            
            print("\n📈 可用的状态：")
            for key, value in Feedback.get_statuses().items():
                print(f"   - {key}: {value}")
            
            print("\n⚡ 可用的优先级：")
            for key, value in Feedback.get_priorities().items():
                print(f"   - {key}: {value}")
            
            print("\n✅ 迁移完成！意见反馈表已成功创建。")
            
        except Exception as e:
            print(f"❌ 迁移失败: {str(e)}")
            return False
    
    return True

if __name__ == '__main__':
    print("🚀 开始执行意见反馈表迁移...")
    success = migrate_add_feedback_table()
    
    if success:
        print("\n🎉 迁移成功完成！")
        print("💡 提示：现在可以使用Feedback模型进行意见反馈功能开发。")
    else:
        print("\n💥 迁移失败，请检查错误信息。")
        sys.exit(1)
