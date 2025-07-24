# 邮箱验证功能使用说明

## 功能概述

本系统新增了邮箱验证功能，用于在gRPC服务中实现基于邮箱的对话保存机制。用户需要先提供有效的邮箱地址，系统会验证邮箱格式并生成唯一的用户ID，后续的对话将根据邮箱进行保存和管理。

## 主要特性

- ✅ **邮箱格式验证**: 自动验证邮箱地址的有效性
- 🆔 **用户ID生成**: 基于邮箱生成唯一的用户标识
- 💾 **对话持久化**: 将对话保存到数据库中
- 🔗 **对话关联**: 后续对话自动关联到同一用户
- 📝 **对话管理**: 支持创建、查询、更新和删除对话

## 新增的gRPC接口

### 1. VerifyEmail - 邮箱验证

**请求消息**: `EmailVerificationRequest`
```protobuf
message EmailVerificationRequest {
    string email = 1;  // 邮箱地址
}
```

**响应消息**: `EmailVerificationResponse`
```protobuf
message EmailVerificationResponse {
    bool success = 1;        // 请求是否成功
    bool is_valid = 2;       // 邮箱是否有效
    string user_id = 3;      // 生成的用户ID
    string error_message = 4; // 错误信息
}
```

### 2. ChatWithEmailVerification - 带邮箱验证的聊天

**请求消息**: `EmailChatRequest`
```protobuf
message EmailChatRequest {
    string email = 1;                    // 邮箱地址
    string question = 2;                 // 用户问题
    string conversation_id = 3;          // 对话ID (可选)
    string conversation_title = 4;       // 对话标题 (可选)
    bool use_feedback = 5;               // 是否使用反馈
    bool use_reranking = 6;              // 是否使用重排序
    int32 top_k = 7;                     // 检索文档数量
    float similarity_threshold = 8;       // 相似度阈值
    int32 max_history_turns = 9;         // 最大历史轮数
}
```

**响应消息**: 使用现有的 `ChatResponse`

## 使用方法

### 1. 命令行使用

#### 验证邮箱
```bash
python src/rpc/grpc_client.py --verify-email test@example.com
```

#### 带邮箱验证的聊天
```bash
python src/rpc/grpc_client.py --email test@example.com --question "什么是人工智能？"
```

#### 交互式演示
```bash
python src/rpc/grpc_client.py --demo
```
在交互式演示中，选择模式2（邮箱验证聊天）来体验完整功能。

### 2. Python代码使用

```python
from rpc.grpc_client import KnowledgeServiceClient

# 创建客户端
client = KnowledgeServiceClient()

# 验证邮箱
email_response = client.verify_email("test@example.com")
if email_response and email_response.is_valid:
    print(f"邮箱有效，用户ID: {email_response.user_id}")

# 带邮箱验证的聊天
response = client.chat_with_email(
    email="test@example.com",
    question="什么是人工智能？",
    conversation_title="AI讨论"
)

if response and response.success:
    print(f"回答: {response.final_answer}")
    
    # 获取对话ID用于后续对话
    if response.feedback_info and 'conversation_id' in response.feedback_info:
        conversation_id = response.feedback_info['conversation_id']
        
        # 后续对话
        follow_up = client.chat_with_email(
            email="test@example.com",
            question="请详细解释一下",
            conversation_id=conversation_id
        )

client.close()
```

## 工作流程

1. **邮箱验证阶段**:
   - 用户提供邮箱地址
   - 系统验证邮箱格式（使用正则表达式）
   - 生成基于邮箱的唯一用户ID（使用SHA-256哈希）

2. **对话创建阶段**:
   - 如果提供了对话ID，验证对话是否属于该用户
   - 如果没有对话ID，创建新的对话
   - 将用户ID关联到对话

3. **对话保存阶段**:
   - 将用户问题和AI回答保存到数据库
   - 维护对话的上下文和历史记录
   - 支持多轮对话的连续性

## 数据库变更

对话表（Conversation）中的 `user_id` 字段现在用于存储基于邮箱生成的用户标识，确保每个邮箱对应唯一的用户ID。

## 测试

运行测试脚本验证功能：
```bash
python test_email_feature.py
```

测试脚本会验证：
- 邮箱格式验证功能
- 带邮箱验证的聊天功能
- 多轮对话的连续性

## 注意事项

1. **邮箱格式**: 系统使用标准的邮箱正则表达式进行验证
2. **用户ID生成**: 基于邮箱的SHA-256哈希，确保唯一性和一致性
3. **对话隔离**: 不同邮箱的对话完全隔离，互不影响
4. **向后兼容**: 原有的聊天功能保持不变，新功能为可选增强

## 错误处理

- 无效邮箱格式会返回相应的错误信息
- 对话ID不匹配会创建新对话
- 网络错误和服务器错误都有相应的异常处理

## 安全考虑

- 邮箱地址经过哈希处理生成用户ID，不直接存储原始邮箱
- 对话数据与用户ID关联，确保数据隔离
- 输入验证防止注入攻击