#!/usr/bin/env python3
"""
修复所有API文档中的响应格式
将JSON字符串格式转换为JSON对象格式
"""

import os
import re
import json

def fix_json_string_to_object(content):
    """将JSON字符串格式转换为JSON对象格式"""
    
    # 匹配 "data": "{\"key\": \"value\"}" 格式，支持多行和嵌套
    pattern = r'"data":\s*"(\{.*?\})"'
    
    def replace_json_string(match):
        json_str = match.group(1)
        try:
            # 解析JSON字符串
            data_obj = json.loads(json_str)
            # 重新格式化为缩进的JSON对象
            formatted_json = json.dumps(data_obj, ensure_ascii=False, indent=2)
            return f'"data": {formatted_json}'
        except json.JSONDecodeError:
            # 如果解析失败，保持原样
            return match.group(0)
    
    return re.sub(pattern, replace_json_string, content, flags=re.MULTILINE | re.DOTALL)

def fix_file(file_path):
    """修复单个文件"""
    print(f"正在修复: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 统计修复前的JSON字符串数量
        before_count = len(re.findall(r'"data":\s*"(\{.*?\})"', content, flags=re.MULTILINE | re.DOTALL))
        
        # 修复JSON字符串格式
        new_content = fix_json_string_to_object(content)
        
        # 统计修复后的JSON字符串数量
        after_count = len(re.findall(r'"data":\s*"(\{.*?\})"', new_content, flags=re.MULTILINE | re.DOTALL))
        
        # 如果内容有变化，写回文件
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ 已修复: {file_path} (修复了 {before_count - after_count} 个JSON字符串)")
        else:
            print(f"ℹ️  无需修复: {file_path}")
            
    except Exception as e:
        print(f"❌ 修复失败: {file_path} - {str(e)}")

def main():
    """主函数"""
    docs_dir = "docs"
    
    if not os.path.exists(docs_dir):
        print(f"❌ 文档目录不存在: {docs_dir}")
        return
    
    # 获取所有.md文件
    md_files = [f for f in os.listdir(docs_dir) if f.endswith('.md')]
    
    if not md_files:
        print("❌ 没有找到.md文件")
        return
    
    print(f"🔍 找到 {len(md_files)} 个文档文件")
    
    total_fixed = 0
    for md_file in md_files:
        file_path = os.path.join(docs_dir, md_file)
        fix_file(file_path)
    
    print(f"\n🎉 所有文档文件修复完成！")

if __name__ == "__main__":
    main()
