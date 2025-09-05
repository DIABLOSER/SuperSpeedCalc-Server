#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信支付PEM私钥文件测试脚本
使用方法：python test_wechat_pem.py path/to/apiclient_key.pem
"""

import sys
import os
from cryptography.hazmat.primitives import serialization

def test_pem_file(pem_file_path):
    """测试PEM文件是否可以正常加载"""
    print(f"🔍 测试PEM文件: {pem_file_path}")
    print("=" * 50)
    
    # 1. 检查文件是否存在
    if not os.path.exists(pem_file_path):
        print(f"❌ 文件不存在: {pem_file_path}")
        return False
    
    print(f"✅ 文件存在")
    
    # 2. 检查文件大小
    file_size = os.path.getsize(pem_file_path)
    print(f"📁 文件大小: {file_size} 字节")
    
    if file_size == 0:
        print("❌ 文件为空")
        return False
    
    # 3. 检查文件内容
    try:
        with open(pem_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"📝 文件字符数: {len(content)}")
        
        # 检查开头和结尾
        if content.startswith('-----BEGIN'):
            print("✅ 文件开头格式正确")
        else:
            print("❌ 文件开头格式错误")
            print(f"实际开头: {content[:50]}")
            
        if content.rstrip().endswith('-----'):
            print("✅ 文件结尾格式正确")
        else:
            print("❌ 文件结尾格式错误")
            print(f"实际结尾: {content[-50:]}")
            
    except UnicodeDecodeError as e:
        print(f"❌ 文件编码错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 读取文件错误: {e}")
        return False
    
    # 4. 尝试加载私钥
    try:
        with open(pem_file_path, 'rb') as key_file:
            pem_data = key_file.read()
            
        private_key = serialization.load_pem_private_key(
            pem_data,
            password=None,
        )
        
        print("✅ PEM私钥加载成功！")
        print(f"🔑 私钥类型: {type(private_key).__name__}")
        print(f"🔑 私钥大小: {private_key.key_size if hasattr(private_key, 'key_size') else '未知'}")
        
        return True
        
    except Exception as e:
        print(f"❌ PEM私钥加载失败: {e}")
        
        # 提供具体的修复建议
        error_str = str(e)
        if "InvalidData" in error_str or "InvalidPadding" in error_str:
            print("\n🔧 修复建议:")
            print("1. 检查PEM文件是否完整（开头和结尾标记）")
            print("2. 确保文件编码为UTF-8")
            print("3. 检查Base64内容是否被破坏")
            print("4. 重新从微信商户平台下载私钥文件")
        elif "password" in error_str.lower():
            print("\n🔧 修复建议:")
            print("1. 私钥可能有密码保护，请提供密码")
        else:
            print(f"\n🔧 未知错误，请检查文件格式")
            
        return False

def main():
    if len(sys.argv) != 2:
        print("使用方法: python test_wechat_pem.py <PEM文件路径>")
        print("示例: python test_wechat_pem.py /path/to/apiclient_key.pem")
        sys.exit(1)
    
    pem_file_path = sys.argv[1]
    success = test_pem_file(pem_file_path)
    
    if success:
        print("\n🎉 PEM文件测试通过，可以正常使用！")
        sys.exit(0)
    else:
        print("\n❌ PEM文件测试失败，请按照上述建议修复")
        sys.exit(1)

if __name__ == "__main__":
    main()
