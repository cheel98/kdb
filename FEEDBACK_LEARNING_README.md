# 🧠 智能知识库反馈学习系统

## 📋 概述

本系统在原有知识库的基础上，集成了深度学习驱动的用户反馈机制，能够根据用户的反馈持续优化回答质量。通过收集用户的正面、负面和纠正性反馈，系统可以自动学习并改进后续的回答。

## ✨ 核心功能

### 1. 用户反馈收集
- **👍 正面反馈**: 用户对答案满意时提供
- **👎 负面反馈**: 用户对答案不满意时提供
- **✏️ 纠正反馈**: 用户提供正确答案进行纠正
- **📝 文本反馈**: 用户可以添加详细的反馈说明

### 2. 智能答案优化
- **自动学习**: 基于用户纠正自动优化答案
- **置信度评估**: 根据反馈次数和质量计算答案置信度
- **动态切换**: 当优化答案置信度足够高时自动使用
- **版本对比**: 显示原始答案与优化答案的对比

### 3. 相似问题推荐
- **智能匹配**: 基于关键词和语义相似度匹配相关问题
- **经验复用**: 利用历史反馈改进相似问题的回答
- **知识关联**: 建立问题间的关联关系

### 4. 学习效果分析
- **实时统计**: 反馈数量、满意度、改进答案数等指标
- **趋势分析**: 系统学习效果的时间趋势
- **数据导出**: 支持导出学习数据用于进一步分析

## 🚀 快速开始

### 1. 启动增强版应用

```bash
# 方法1: 使用启动脚本
python run_enhanced_app.py

# 方法2: 直接运行
streamlit run src/enhanced_app.py --server.port=8502
```

### 2. 配置反馈学习参数

在侧边栏的"🎯 反馈学习设置"中可以调整：

- **启用反馈学习**: 开启/关闭反馈学习功能
- **置信度阈值**: 使用优化答案的最低置信度 (默认: 0.7)
- **相似度阈值**: 相似问题匹配的最低相似度 (默认: 0.8)

### 3. 使用反馈功能

1. **提问**: 在智能问答界面输入问题
2. **查看答案**: 系统会显示答案，如果有优化版本会特别标注
3. **提供反馈**: 使用反馈按钮提供反馈
   - 点击 👍 表示满意
   - 点击 👎 表示不满意
   - 点击 ✏️ 提供正确答案
4. **查看历史**: 点击"📊 查看反馈历史"查看问题的反馈记录

## 🏗️ 系统架构

### 核心组件

```
智能知识库反馈学习系统
├── feedback_system.py          # 反馈学习核心模块
│   ├── FeedbackRecord         # 反馈记录数据结构
│   ├── FeedbackDatabase       # 反馈数据库管理
│   └── FeedbackLearningSystem # 反馈学习主类
├── enhanced_knowledge_base.py  # 增强知识库
│   └── EnhancedKnowledgeBase  # 集成反馈功能的知识库
├── enhanced_app.py            # 增强版Streamlit应用
└── run_enhanced_app.py        # 应用启动器
```

### 数据流程

```
用户问题 → 知识库检索 → 生成答案 → 检查反馈优化 → 返回最终答案
    ↓
用户反馈 → 反馈存储 → 答案优化 → 置信度更新 → 影响后续回答
```

## 📊 反馈数据结构

### 反馈记录表 (feedback)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| question | TEXT | 用户问题 |
| original_answer | TEXT | 原始答案 |
| user_feedback | TEXT | 反馈类型 (positive/negative/corrected) |
| corrected_answer | TEXT | 纠正后的答案 |
| feedback_text | TEXT | 反馈说明 |
| timestamp | TEXT | 时间戳 |
| question_hash | TEXT | 问题哈希值 |
| source_documents | TEXT | 来源文档 (JSON) |

### 答案改进表 (answer_improvements)

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| question_hash | TEXT | 问题哈希值 |
| improved_answer | TEXT | 改进后的答案 |
| confidence_score | REAL | 置信度分数 |
| feedback_count | INTEGER | 反馈次数 |
| last_updated | TEXT | 最后更新时间 |

## 🔧 API 使用示例

### 基本使用

```python
from src.enhanced_knowledge_base import EnhancedKnowledgeBase

# 创建增强知识库实例
kb = EnhancedKnowledgeBase()
kb.load_vector_store()

# 提问（自动使用反馈优化）
result = kb.ask_question_with_feedback("什么是人工智能？")
print(f"答案: {result['final_answer']}")
print(f"是否优化: {result['feedback_info']['is_improved']}")

# 收集用户反馈
feedback_id = kb.collect_user_feedback(
    question="什么是人工智能？",
    original_answer=result['original_answer'],
    feedback_type="corrected",
    corrected_answer="人工智能是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。",
    feedback_text="原答案太简单，需要更详细的解释"
)

# 获取统计信息
stats = kb.get_feedback_stats()
print(f"满意度: {stats['satisfaction_rate']:.1f}%")
```

### 高级配置

```python
# 更新反馈学习设置
kb.update_feedback_settings(
    enable_feedback=True,
    confidence_threshold=0.8,  # 提高置信度要求
    similarity_threshold=0.7   # 降低相似度要求
)

# 搜索带反馈上下文的文档
results = kb.search_with_feedback_context("机器学习", k=5)
for result in results:
    if result['feedback_context']['has_similar_feedback']:
        print(f"发现相似问题反馈: {result['metadata']['source']}")

# 导出学习数据
export_result = kb.export_learning_data("./exports")
print(f"数据已导出: {export_result['export_timestamp']}")
```

## 📈 学习效果监控

### 关键指标

1. **满意度率**: 正面反馈 / 总反馈数
2. **改进覆盖率**: 有改进答案的问题 / 总问题数
3. **平均置信度**: 所有改进答案的平均置信度
4. **反馈活跃度**: 单位时间内的反馈数量

### 监控面板

在"📈 学习分析"标签页中可以查看：
- 实时统计数据
- 反馈分布图表
- 系统配置信息
- 学习趋势分析

## 🔒 数据安全与隐私

- **本地存储**: 所有反馈数据存储在本地SQLite数据库
- **数据加密**: 敏感信息使用哈希处理
- **访问控制**: 仅授权用户可以访问反馈数据
- **数据备份**: 支持定期导出备份

## 🛠️ 故障排除

### 常见问题

1. **反馈功能不工作**
   - 检查是否启用了反馈学习
   - 确认数据库文件权限
   - 查看日志错误信息

2. **优化答案不显示**
   - 检查置信度阈值设置
   - 确认是否有足够的纠正反馈
   - 验证问题哈希匹配

3. **相似问题匹配不准确**
   - 调整相似度阈值
   - 检查问题关键词
   - 考虑使用更高级的相似度算法

### 日志调试

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 查看详细的反馈处理日志
kb = EnhancedKnowledgeBase()
# ... 执行操作
```

## 🔮 未来改进方向

1. **深度学习集成**
   - 使用Transformer模型进行语义相似度计算
   - 集成强化学习优化反馈权重
   - 实现自动答案生成和优化

2. **多模态支持**
   - 支持图片、视频等多媒体反馈
   - 语音反馈识别和处理
   - 情感分析增强反馈理解

3. **协作学习**
   - 多用户反馈聚合
   - 专家权重系统
   - 社区驱动的知识改进

4. **智能推荐**
   - 主动推荐需要反馈的问题
   - 个性化答案优化
   - 预测性问题建议

## 📞 技术支持

如果您在使用过程中遇到问题，请：

1. 查看本文档的故障排除部分
2. 检查系统日志文件
3. 导出反馈数据进行分析
4. 联系技术支持团队

---

**版本**: 1.0.0  
**更新日期**: 2024年12月  
**兼容性**: Python 3.8+, Streamlit 1.28+