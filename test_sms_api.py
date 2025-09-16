#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SMS API 测试脚本
测试发送短信验证码、验证短信验证码接口和手机号密码重置接口
"""

import requests
import json
import time

# 服务器配置
BASE_URL = "http://localhost:8000"
SMS_SEND_URL = f"{BASE_URL}/sms/send"
SMS_VERIFY_URL = f"{BASE_URL}/sms/verify"
PASSWORD_RESET_URL = f"{BASE_URL}/users/reset-password"

def test_send_sms():
    """测试发送短信验证码"""
    print("🧪 测试发送短信验证码接口...")
    
    # 测试数据
    test_data = {
        "phone": "13800138000"  # 请替换为真实的手机号进行测试
    }
    
    try:
        response = requests.post(
            SMS_SEND_URL,
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 200:
            print("✅ 发送短信验证码接口测试成功")
            return True
        else:
            print("❌ 发送短信验证码接口测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 发送短信验证码接口测试异常: {str(e)}")
        return False

def test_verify_sms():
    """测试验证短信验证码"""
    print("\n🧪 测试验证短信验证码接口...")
    
    # 测试数据
    test_data = {
        "phone": "13800138000",  # 请替换为真实的手机号进行测试
        "code": "123456"  # 请替换为真实的验证码进行测试
    }
    
    try:
        response = requests.post(
            SMS_VERIFY_URL,
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 200:
            print("✅ 验证短信验证码接口测试成功")
            return True
        else:
            print("❌ 验证短信验证码接口测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 验证短信验证码接口测试异常: {str(e)}")
        return False

def test_invalid_phone():
    """测试无效手机号"""
    print("\n🧪 测试无效手机号...")
    
    test_data = {
        "phone": "123"  # 无效手机号
    }
    
    try:
        response = requests.post(
            SMS_SEND_URL,
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 400:
            print("✅ 无效手机号测试成功（正确返回400错误）")
            return True
        else:
            print("❌ 无效手机号测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 无效手机号测试异常: {str(e)}")
        return False

def test_missing_parameters():
    """测试缺少参数"""
    print("\n🧪 测试缺少参数...")
    
    test_data = {}  # 缺少phone参数
    
    try:
        response = requests.post(
            SMS_SEND_URL,
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 400:
            print("✅ 缺少参数测试成功（正确返回400错误）")
            return True
        else:
            print("❌ 缺少参数测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 缺少参数测试异常: {str(e)}")
        return False

def test_password_reset():
    """测试手机号密码重置接口"""
    print("\n🧪 测试手机号密码重置接口...")
    
    # 测试数据
    test_data = {
        "mobile": "13800138000",      # 请替换为真实的手机号进行测试
        "new_password": "newpass123"  # 新密码
    }
    
    try:
        response = requests.post(
            PASSWORD_RESET_URL,
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 200:
            print("✅ 手机号密码重置接口测试成功")
            return True
        else:
            print("❌ 手机号密码重置接口测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 手机号密码重置接口测试异常: {str(e)}")
        return False

def test_password_reset_validation():
    """测试手机号密码重置参数验证"""
    print("\n🧪 测试手机号密码重置参数验证...")
    
    # 测试用例
    test_cases = [
        {
            "name": "缺少手机号",
            "data": {"new_password": "newpass123"},
            "expected_status": 400
        },
        {
            "name": "缺少新密码",
            "data": {"mobile": "13800138000"},
            "expected_status": 400
        },
        {
            "name": "手机号格式错误",
            "data": {"mobile": "1380013800", "new_password": "newpass123"},
            "expected_status": 400
        },
        {
            "name": "密码太短",
            "data": {"mobile": "13800138000", "new_password": "123"},
            "expected_status": 400
        }
    ]
    
    passed = 0
    total = len(test_cases)
    
    for test_case in test_cases:
        print(f"\n📋 测试: {test_case['name']}")
        try:
            response = requests.post(
                PASSWORD_RESET_URL,
                json=test_case['data'],
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"状态码: {response.status_code}")
            print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
            
            if response.status_code == test_case['expected_status']:
                print(f"✅ {test_case['name']}测试成功")
                passed += 1
            else:
                print(f"❌ {test_case['name']}测试失败")
                
        except Exception as e:
            print(f"❌ {test_case['name']}测试异常: {str(e)}")
    
    print(f"\n📊 参数验证测试结果: {passed}/{total} 通过")
    return passed == total

def main():
    """主测试函数"""
    print("🚀 开始SMS API和密码重置测试...")
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
        print("请确保服务器正在运行 (python app.py)")
        return
    
    print("=" * 50)
    
    # 运行测试
    tests = [
        ("发送短信验证码", test_send_sms),
        ("验证短信验证码", test_verify_sms),
        ("无效手机号", test_invalid_phone),
        ("缺少参数", test_missing_parameters),
        ("手机号密码重置", test_password_reset),
        ("密码重置参数验证", test_password_reset_validation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 运行测试: {test_name}")
        if test_func():
            passed += 1
        time.sleep(1)  # 避免请求过于频繁
    
    print("\n" + "=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print("⚠️  部分测试失败，请检查配置和实现")
    
    print("\n💡 使用说明:")
    print("1. 确保服务器正在运行 (python app.py)")
    print("2. 确保Bmob配置正确")
    print("3. 使用真实的手机号进行测试")
    print("4. 密码重置接口需要客户端先验证短信验证码")
    print("5. 完整的密码重置流程:")
    print("   - 发送短信验证码 -> 验证短信验证码 -> 重置密码")

if __name__ == "__main__":
    main()
