#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SMS 短信服务使用示例
演示如何调用发送短信验证码和验证短信验证码接口
"""

import requests
import json

# 服务器配置
BASE_URL = "http://localhost:8000"

def send_sms_example():
    """发送短信验证码示例"""
    print("📱 发送短信验证码示例")
    print("-" * 30)
    
    url = f"{BASE_URL}/sms/send"
    data = {
        "phone": "13800138000"  # 请替换为真实手机号
    }
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        
        print(f"请求URL: {url}")
        print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        print(f"响应状态: {response.status_code}")
        print(f"响应数据: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        if result.get('success'):
            print("✅ 短信验证码发送成功！")
            return True
        else:
            print(f"❌ 短信验证码发送失败: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        return False

def verify_sms_example():
    """验证短信验证码示例"""
    print("\n🔐 验证短信验证码示例")
    print("-" * 30)
    
    url = f"{BASE_URL}/sms/verify"
    data = {
        "phone": "13800138000",  # 请替换为真实手机号
        "code": "123456"         # 请替换为真实验证码
    }
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        
        print(f"请求URL: {url}")
        print(f"请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
        print(f"响应状态: {response.status_code}")
        print(f"响应数据: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        if result.get('success'):
            print("✅ 短信验证码验证成功！")
            return True
        else:
            print(f"❌ 短信验证码验证失败: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        return False

def complete_flow_example():
    """完整流程示例：发送验证码 -> 验证验证码"""
    print("🔄 完整短信验证流程示例")
    print("=" * 50)
    
    phone = "13800138000"  # 请替换为真实手机号
    
    # 步骤1：发送验证码
    print("步骤1：发送短信验证码")
    send_success = send_sms_example()
    
    if not send_success:
        print("❌ 发送验证码失败，流程终止")
        return
    
    # 步骤2：等待用户输入验证码
    print(f"\n步骤2：请在手机上查看验证码，然后输入")
    code = input("请输入收到的验证码: ").strip()
    
    if not code:
        print("❌ 未输入验证码，流程终止")
        return
    
    # 步骤3：验证验证码
    print(f"\n步骤3：验证短信验证码")
    verify_data = {
        "phone": phone,
        "code": code
    }
    
    url = f"{BASE_URL}/sms/verify"
    try:
        response = requests.post(url, json=verify_data)
        result = response.json()
        
        print(f"验证结果: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        if result.get('success'):
            print("🎉 完整验证流程成功！")
        else:
            print(f"❌ 验证失败: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ 验证请求异常: {str(e)}")

def main():
    """主函数"""
    print("🚀 SMS 短信服务使用示例")
    print("=" * 50)
    
    # 检查服务器是否运行
    try:
        health_response = requests.get(f"{BASE_URL}/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ 服务器运行正常")
        else:
            print("❌ 服务器健康检查失败")
            return
    except Exception as e:
        print(f"❌ 无法连接到服务器: {str(e)}")
        print("请确保服务器正在运行 (python3 app.py)")
        return
    
    print("\n请选择要运行的示例：")
    print("1. 发送短信验证码示例")
    print("2. 验证短信验证码示例")
    print("3. 完整验证流程示例")
    print("4. 退出")
    
    while True:
        choice = input("\n请输入选择 (1-4): ").strip()
        
        if choice == "1":
            send_sms_example()
        elif choice == "2":
            verify_sms_example()
        elif choice == "3":
            complete_flow_example()
        elif choice == "4":
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请输入 1-4")

if __name__ == "__main__":
    main()
