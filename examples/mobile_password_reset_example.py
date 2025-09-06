#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手机号密码重置使用示例
演示如何使用手机号重置密码功能
"""

import requests
import json

# 服务器配置
BASE_URL = "http://localhost:8000"

def mobile_password_reset_example():
    """手机号密码重置示例"""
    print("🔐 手机号密码重置示例")
    print("-" * 40)
    
    # 步骤1：发送短信验证码（客户端处理）
    print("步骤1：发送短信验证码")
    sms_data = {
        "phone": "13800138000"  # 请替换为真实手机号
    }
    
    try:
        sms_response = requests.post(
            f"{BASE_URL}/sms/send",
            json=sms_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"短信发送结果: {json.dumps(sms_response.json(), ensure_ascii=False, indent=2)}")
        
        if sms_response.status_code == 200:
            print("✅ 短信验证码发送成功")
        else:
            print("❌ 短信验证码发送失败")
            return False
            
    except Exception as e:
        print(f"❌ 短信发送异常: {str(e)}")
        return False
    
    # 步骤2：验证短信验证码（客户端处理）
    print(f"\n步骤2：验证短信验证码")
    verify_data = {
        "phone": "13800138000",
        "code": "123456"  # 请替换为真实验证码
    }
    
    try:
        verify_response = requests.post(
            f"{BASE_URL}/sms/verify",
            json=verify_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"验证结果: {json.dumps(verify_response.json(), ensure_ascii=False, indent=2)}")
        
        if verify_response.status_code == 200:
            print("✅ 短信验证码验证成功")
        else:
            print("❌ 短信验证码验证失败")
            return False
            
    except Exception as e:
        print(f"❌ 验证异常: {str(e)}")
        return False
    
    # 步骤3：重置密码
    print(f"\n步骤3：重置密码")
    reset_data = {
        "mobile": "13800138000",
        "new_password": "new_secure_password_123"
    }
    
    try:
        reset_response = requests.post(
            f"{BASE_URL}/users/reset-password",
            json=reset_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"重置结果: {json.dumps(reset_response.json(), ensure_ascii=False, indent=2)}")
        
        if reset_response.status_code == 200:
            result = reset_response.json()
            if result.get('success'):
                print("✅ 密码重置成功")
                
                # 显示用户信息
                user_data = result.get('data', {})
                print(f"\n📋 用户信息:")
                print(f"  用户ID: {user_data.get('objectId')}")
                print(f"  用户名: {user_data.get('username')}")
                print(f"  手机号: {user_data.get('mobile')}")
                print(f"  邮箱: {user_data.get('email')}")
                print(f"  经验值: {user_data.get('experience')}")
                print(f"  菠萝币: {user_data.get('boluo')}")
                print(f"  更新时间: {user_data.get('updatedAt')}")
                
                return True
            else:
                print(f"❌ 密码重置失败: {result.get('error')}")
                return False
        else:
            print("❌ 密码重置请求失败")
            return False
            
    except Exception as e:
        print(f"❌ 重置异常: {str(e)}")
        return False

def test_invalid_scenarios():
    """测试各种无效场景"""
    print("\n🧪 测试无效场景")
    print("-" * 40)
    
    # 测试无效手机号
    print("1. 测试无效手机号")
    invalid_mobile_data = {
        "mobile": "123",
        "new_password": "newpass123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/users/reset-password",
            json=invalid_mobile_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 400:
            print("   ✅ 无效手机号正确返回400错误")
        else:
            print("   ❌ 无效手机号测试失败")
            
    except Exception as e:
        print(f"   ❌ 测试异常: {str(e)}")
    
    # 测试密码过短
    print("\n2. 测试密码过短")
    short_password_data = {
        "mobile": "13800138000",
        "new_password": "123"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/users/reset-password",
            json=short_password_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 400:
            print("   ✅ 密码过短正确返回400错误")
        else:
            print("   ❌ 密码过短测试失败")
            
    except Exception as e:
        print(f"   ❌ 测试异常: {str(e)}")
    
    # 测试缺少参数
    print("\n3. 测试缺少参数")
    missing_data = {}
    
    try:
        response = requests.post(
            f"{BASE_URL}/users/reset-password",
            json=missing_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 400:
            print("   ✅ 缺少参数正确返回400错误")
        else:
            print("   ❌ 缺少参数测试失败")
            
    except Exception as e:
        print(f"   ❌ 测试异常: {str(e)}")

def main():
    """主函数"""
    print("🚀 手机号密码重置功能使用示例")
    print("=" * 60)
    
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
    
    print("=" * 60)
    
    # 运行示例
    print("\n请选择要运行的示例：")
    print("1. 完整密码重置流程示例")
    print("2. 无效场景测试")
    print("3. 退出")
    
    while True:
        choice = input("\n请输入选择 (1-3): ").strip()
        
        if choice == "1":
            mobile_password_reset_example()
        elif choice == "2":
            test_invalid_scenarios()
        elif choice == "3":
            print("👋 再见！")
            break
        else:
            print("❌ 无效选择，请输入 1-3")

if __name__ == "__main__":
    main()