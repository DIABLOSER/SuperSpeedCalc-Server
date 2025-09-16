# 微信支付PEM私钥问题修复指南

## 错误分析
```
ValueError: Unable to load PEM file. InvalidData(InvalidPadding)
```

## 检查步骤

### 1. 检查PEM文件格式
确保私钥文件符合以下格式：

```
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...
（Base64编码内容，每行64字符）
...
-----END PRIVATE KEY-----
```

### 2. 常见问题及解决方案

#### ✅ 文件编码问题
- 确保文件保存为 **UTF-8 无BOM** 编码
- 避免使用Windows记事本编辑，推荐使用VSCode或其他专业编辑器

#### ✅ 文件内容完整性
- 检查开头是否为 `-----BEGIN PRIVATE KEY-----` 或 `-----BEGIN RSA PRIVATE KEY-----`
- 检查结尾是否为 `-----END PRIVATE KEY-----` 或 `-----END RSA PRIVATE KEY-----`
- 确保中间没有多余的空行或字符

#### ✅ Base64内容检查
- 中间的内容应该只包含：A-Z, a-z, 0-9, +, /, =
- 每行应该是64个字符（最后一行可以少于64个）
- 不能包含空格、制表符或其他特殊字符

#### ✅ 文件路径检查
```python
import os
pem_file_path = "path/to/your/private_key.pem"
if os.path.exists(pem_file_path):
    print("PEM文件存在")
    with open(pem_file_path, 'r') as f:
        content = f.read()
        print(f"文件大小: {len(content)} 字符")
        print(f"文件开头: {content[:50]}")
else:
    print("PEM文件不存在，请检查路径")
```

### 3. 测试PEM文件是否可用

```python
from cryptography.hazmat.primitives import serialization

def test_pem_file(pem_file_path):
    try:
        with open(pem_file_path, 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,  # 如果有密码，在这里提供
            )
        print("✅ PEM私钥加载成功！")
        return True
    except Exception as e:
        print(f"❌ PEM私钥加载失败: {e}")
        return False

# 使用示例
test_pem_file("path/to/your/private_key.pem")
```

### 4. 微信支付私钥获取方法

1. **登录微信商户平台**
2. **进入账户中心 → API安全**
3. **下载API证书**
4. **解压后找到 `apiclient_key.pem` 文件**

### 5. 代码修复示例

```python
import os
from cryptography.hazmat.primitives import serialization

class WeChatPayConfig:
    def __init__(self):
        # 配置文件路径（使用绝对路径）
        self.private_key_path = os.path.join(
            os.path.dirname(__file__), 
            'certs', 
            'apiclient_key.pem'
        )
        self._private_key = None
    
    def load_private_key(self):
        """加载私钥，增加错误处理"""
        if self._private_key is not None:
            return self._private_key
            
        try:
            # 检查文件是否存在
            if not os.path.exists(self.private_key_path):
                raise FileNotFoundError(f"PEM私钥文件不存在: {self.private_key_path}")
            
            # 读取并加载私钥
            with open(self.private_key_path, 'rb') as key_file:
                pem_data = key_file.read()
                
            self._private_key = serialization.load_pem_private_key(
                pem_data,
                password=None,  # 如果私钥有密码保护，在这里添加
            )
            
            print("✅ 微信支付私钥加载成功")
            return self._private_key
            
        except Exception as e:
            print(f"❌ 加载微信支付私钥失败: {e}")
            # 可以添加更详细的错误信息
            if "InvalidData" in str(e):
                print("提示：请检查PEM文件格式是否正确")
            elif "FileNotFoundError" in str(e):
                print("提示：请检查文件路径是否正确")
            raise
```

### 6. 环境变量配置方案

```python
import os
from cryptography.hazmat.primitives import serialization

# 方法1：使用环境变量存储文件路径
WECHAT_PRIVATE_KEY_PATH = os.environ.get('WECHAT_PRIVATE_KEY_PATH')

# 方法2：使用环境变量直接存储私钥内容（适用于容器部署）
WECHAT_PRIVATE_KEY_CONTENT = os.environ.get('WECHAT_PRIVATE_KEY_CONTENT')

def load_wechat_private_key():
    if WECHAT_PRIVATE_KEY_CONTENT:
        # 从环境变量加载私钥内容
        return serialization.load_pem_private_key(
            WECHAT_PRIVATE_KEY_CONTENT.encode('utf-8'),
            password=None
        )
    elif WECHAT_PRIVATE_KEY_PATH:
        # 从文件路径加载私钥
        with open(WECHAT_PRIVATE_KEY_PATH, 'rb') as key_file:
            return serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
    else:
        raise ValueError("未配置微信支付私钥")
```

## 总结

大多数PEM加载失败的问题都是由于：
1. 文件格式不正确
2. 编码问题
3. 文件路径错误

按照上述步骤逐一检查，通常可以解决问题。如果问题仍然存在，建议重新从微信商户平台下载私钥文件。
