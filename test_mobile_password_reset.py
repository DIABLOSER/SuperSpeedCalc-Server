#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手机号密码重置功能测试脚本
测试重置密码API的返回格式是否与注册成功返回格式一致
"""

import requests
import json
import time

# 服务器配置
BASE_URL = "http://localhost:8000"

def test_mobile_password_reset():
    """测试手机号密码重置功能"""
    print("🧪 测试手机号密码重置功能...")
    print("-" * 50)
    
    # 测试数据
    test_data = {
        "mobile": "13800138000",  # 请替换为真实的已注册手机号
        "new_password": "newpass123456"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/users/reset-password",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ 手机号密码重置成功")
                
                # 检查返回格式
                data = result.get('data', {})
                required_fields = ['objectId', 'username', 'email', 'mobile', 'avatar', 'bio', 
                                 'experience', 'boluo', 'isActive', 'admin', 'sex', 'birthday', 
                                 'createdAt', 'updatedAt']
                
                print("\n📋 检查返回数据格式:")
                missing_fields = []
                for field in required_fields:
                    if field in data:
                        print(f"  ✅ {field}: {data[field]}")
                    else:
                        print(f"  ❌ {field}: 缺失")
                        missing_fields.append(field)
                
                if not missing_fields:
                    print("\n🎉 返回格式完整，与注册成功返回格式一致！")
                else:
                    print(f"\n⚠️  缺失字段: {missing_fields}")
                
                return True
            else:
                print(f"❌ 密码重置失败: {result.get('error')}")
                return False
        else:
            print("❌ 请求失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {str(e)}")
        return False

def test_invalid_mobile():
    """测试无效手机号"""
    print("\n🧪 测试无效手机号...")
    print("-" * 30)
    
    test_data = {
        "mobile": "123",  # 无效手机号
        "new_password": "newpass123456"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/users/reset-password",
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
        print(f"❌ 测试异常: {str(e)}")
        return False

def test_short_password():
    """测试密码过短"""
    print("\n🧪 测试密码过短...")
    print("-" * 30)
    
    test_data = {
        "mobile": "13800138000",
        "new_password": "123"  # 密码过短
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/users/reset-password",
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        if response.status_code == 400:
            print("✅ 密码过短测试成功（正确返回400错误）")
            return True
        else:
            print("❌ 密码过短测试失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试异常: {str(e)}")
        return False

def test_missing_parameters():
    """测试缺少参数"""
    print("\n🧪 测试缺少参数...")
    print("-" * 30)
    
    test_data = {}  # 缺少必需参数
    
    try:
        response = requests.post(
            f"{BASE_URL}/users/reset-password",
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
        print(f"❌ 测试异常: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始手机号密码重置功能测试...")
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
    
    # 运行测试
    tests = [
        ("手机号密码重置", test_mobile_password_reset),
        ("无效手机号", test_invalid_mobile),
        ("密码过短", test_short_password),
        ("缺少参数", test_missing_parameters)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 运行测试: {test_name}")
        if test_func():
            passed += 1
        time.sleep(1)  # 避免请求过于频繁
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！")
    else:
        print("⚠️  部分测试失败，请检查配置和实现")

if __name__ == "__main__":
    main()
