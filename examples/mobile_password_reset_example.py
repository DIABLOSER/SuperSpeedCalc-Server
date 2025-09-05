#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据手机号重置密码接口使用示例
"""

import requests
import json

def reset_password_by_mobile_example():
    """根据手机号重置密码示例"""
    
    # 服务器地址
    base_url = "http://localhost:8000"
    
    # 接口地址
    url = f"{base_url}/users/reset-password"
    
    # 请求头
    headers = {
        "Content-Type": "application/json"
    }
    
    # 请求数据
    data = {
        "mobile": "13800138000",      # 用户手机号
        "new_password": "newpass123"  # 新密码
    }
    
    print("📱 根据手机号重置密码示例")
    print("=" * 40)
    print(f"🔗 接口地址: {url}")
    print(f"📋 请求数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
    
    try:
        # 发送POST请求
        response = requests.post(url, json=data, headers=headers)
        
        # 解析响应
        result = response.json()
        
        print(f"📥 响应状态码: {response.status_code}")
        print(f"📄 响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        if response.status_code == 200 and result.get('success'):
            print("✅ 密码重置成功!")
            user_info = result.get('data', {})
            print(f"👤 用户ID: {user_info.get('id')}")
            print(f"👤 用户名: {user_info.get('username')}")
            print(f"📱 手机号: {user_info.get('mobile')}")
            print(f"🕒 更新时间: {user_info.get('updatedAt')}")
        else:
            print(f"❌ 密码重置失败: {result.get('error')}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败，请确保服务器正在运行")
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")

def curl_example():
    """cURL命令示例"""
    
    print("\n🔧 cURL命令示例")
    print("=" * 40)
    
    curl_command = '''curl -X POST "http://localhost:8000/users/reset-password" \\
  -H "Content-Type: application/json" \\
  -d '{
    "mobile": "13800138000",
    "new_password": "newpass123"
  }' '''
    
    print(curl_command)

def javascript_example():
    """JavaScript示例"""
    
    print("\n🌐 JavaScript示例")
    print("=" * 40)
    
    js_code = '''
// 使用fetch API
async function resetPasswordByMobile(mobile, newPassword) {
    try {
        const response = await fetch('/users/reset-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mobile: mobile,
                new_password: newPassword
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            console.log('密码重置成功:', result.data);
            return result;
        } else {
            console.error('密码重置失败:', result.error);
            throw new Error(result.error);
        }
    } catch (error) {
        console.error('请求失败:', error);
        throw error;
    }
}

// 使用示例
resetPasswordByMobile('13800138000', 'newpass123')
    .then(result => {
        console.log('重置成功:', result);
    })
    .catch(error => {
        console.error('重置失败:', error);
    });
'''
    
    print(js_code)

def api_documentation():
    """API文档"""
    
    print("\n📚 API文档")
    print("=" * 40)
    
    doc = """
接口名称: 根据手机号重置密码
接口地址: POST /users/reset-password
接口描述: 通过手机号重置用户密码（客户端已验证短信验证码）

请求参数:
{
    "mobile": "13800138000",      // 必填，用户手机号，11位数字
    "new_password": "newpass123"  // 必填，新密码，至少6个字符
}

响应格式:
成功响应 (200):
{
    "success": true,
    "message": "密码更新成功",
    "data": {
        "id": "用户ID",
        "username": "用户名",
        "mobile": "手机号",
        "updatedAt": "更新时间"
    }
}

失败响应 (400/404/500):
{
    "success": false,
    "error": "错误信息"
}

错误码说明:
- 400: 参数错误（缺少参数、格式错误、密码长度不足等）
- 404: 手机号未注册
- 500: 服务器内部错误

使用流程:
1. 用户输入手机号
2. 客户端调用短信发送接口发送验证码
3. 用户输入收到的验证码，客户端验证
4. 验证通过后，用户输入新密码
5. 调用此接口重置密码
6. 根据响应结果提示用户
"""
    
    print(doc)

if __name__ == "__main__":
    print("🚀 根据手机号重置密码接口示例")
    print("=" * 60)
    
    # Python示例
    reset_password_by_mobile_example()
    
    # cURL示例
    curl_example()
    
    # JavaScript示例
    javascript_example()
    
    # API文档
    api_documentation()
    
    print("\n" + "=" * 60)
    print("🏁 示例完成")
