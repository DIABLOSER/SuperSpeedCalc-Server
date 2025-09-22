# 数据库迁移说明

## 概述
本文档记录了SuperSpeedCalc-Server项目的数据库结构变更和迁移脚本。

## 迁移历史

### 1. 修改replies表post字段为可空
**迁移文件**: `scripts/migrate_make_post_nullable_in_replies.py`
**执行时间**: 2025-09-22
**影响范围**: replies表

#### 变更内容
- 将replies表的post字段从 `nullable=False` 改为 `nullable=True`
- 支持帖子删除后评论数据独立存在
- 保持数据完整性和历史记录

#### 设计理念
- **数据完整性**: 删除帖子时，相关评论数据被保留
- **评论独立性**: 评论可以独立存在，即使关联的帖子不存在
- **历史记录保留**: 确保用户的历史评论记录不会丢失
- **数据恢复支持**: 如果帖子被误删，评论数据仍然可以恢复
- **审计功能**: 支持数据审计和追踪功能

#### 技术实现
```sql
-- 原结构
post VARCHAR(20) NOT NULL

-- 新结构  
post VARCHAR(20) NULL
```

#### 迁移过程
1. 创建新表 `replies_new`
2. 复制现有数据到新表
3. 删除原表 `replies`
4. 重命名新表为 `replies`
5. 重新创建索引

#### 数据验证
- 迁移前：18条评论记录
- 迁移后：18条评论记录（数据完整性保持）
- 所有外键关系正常

#### 影响评估
- **正面影响**:
  - 支持软删除模式
  - 提高数据安全性
  - 支持数据恢复
  - 改善用户体验

- **注意事项**:
  - 查询评论时需要处理post字段为null的情况
  - 统计功能需要考虑孤立评论
  - 前端显示需要适配

## 迁移脚本使用说明

### 执行迁移
```bash
# 进入项目目录
cd SuperSpeedCalc-Server

# 执行迁移脚本
python scripts/migrate_make_post_nullable_in_replies.py
```

### 回滚方案
如果需要回滚，可以执行以下步骤：
1. 备份当前数据库
2. 将post字段为null的评论删除或重新关联
3. 修改字段约束为NOT NULL
4. 重新创建索引

### 验证迁移结果
```python
# 检查表结构
import sqlite3
conn = sqlite3.connect('instance/database.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(replies)")
columns = cursor.fetchall()
for col in columns:
    print(f"{col[1]} - {col[2]} - nullable: {not col[3]}")

# 检查数据完整性
cursor.execute("SELECT COUNT(*) FROM replies")
count = cursor.fetchone()[0]
print(f"评论总数: {count}")

# 检查孤立评论
cursor.execute("SELECT COUNT(*) FROM replies WHERE post IS NULL")
orphaned = cursor.fetchone()[0]
print(f"孤立评论数: {orphaned}")
```

## 最佳实践

### 1. 迁移前准备
- 备份数据库
- 在测试环境验证
- 准备回滚方案
- 通知相关开发人员

### 2. 迁移执行
- 在维护窗口期执行
- 监控迁移过程
- 验证数据完整性
- 测试相关功能

### 3. 迁移后验证
- 检查数据完整性
- 测试相关接口
- 验证业务逻辑
- 更新文档

## 未来迁移计划

### 待实施的迁移
1. **用户表优化**: 添加更多用户字段
2. **帖子表扩展**: 支持更多内容类型
3. **评论表增强**: 支持更多评论类型
4. **索引优化**: 提升查询性能

### 迁移原则
- 保持向后兼容性
- 最小化数据丢失
- 支持回滚操作
- 充分测试验证

## 联系信息
如有迁移相关问题，请联系开发团队。
