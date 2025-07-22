# 知识库RPC服务

本项目已升级为支持gRPC协议的后端服务，提供智能问答、反馈收集等RPC接口。

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 生成gRPC代码

```bash
python generate_grpc.py
```

### 3. 启动RPC服务器

```bash
# 使用默认配置启动
python run_grpc_server.py

# 自定义端口和线程数
python run_grpc_server.py --port 50051 --workers 10
```

### 4. 测试服务

```bash
# 基本功能测试
python test_grpc_client.py --basic

# 性能测试
python test_grpc_client.py --performance

# 交互式演示
python src/grpc_client.py --demo
```

## 📡 RPC接口说明

### 服务定义

服务名称: `KnowledgeService`
默认端口: `50051`
协议: `gRPC`

### 接口列表

#### 1. Chat - 智能问答
```protobuf
rpc Chat(ChatRequest) returns (ChatResponse);
```
- **功能**: 基于知识库进行智能问答
- **输入**: 问题文本、是否使用反馈优化
- **输出**: 原始答案、优化答案、来源文档、反馈信息

#### 2. SubmitFeedback - 提交反馈
```protobuf
rpc SubmitFeedback(FeedbackRequest) returns (FeedbackResponse);
```
- **功能**: 收集用户对答案的反馈
- **输入**: 问题、原始答案、反馈类型（positive/negative/corrected）、纠正答案
- **输出**: 反馈ID、处理状态

#### 3. GetFeedbackHistory - 获取反馈历史
```protobuf
rpc GetFeedbackHistory(FeedbackHistoryRequest) returns (FeedbackHistoryResponse);
```
- **功能**: 获取特定问题的反馈历史记录
- **输入**: 问题文本
- **输出**: 反馈记录列表

#### 4. GetStats - 获取统计信息
```protobuf
rpc GetStats(StatsRequest) returns (StatsResponse);
```
- **功能**: 获取知识库和反馈系统的统计信息
- **输入**: 空
- **输出**: 知识库统计、反馈统计、系统配置

#### 5. SearchDocuments - 搜索文档
```protobuf
rpc SearchDocuments(SearchRequest) returns (SearchResponse);
```
- **功能**: 在知识库中搜索相关文档
- **输入**: 搜索查询、返回数量
- **输出**: 搜索结果列表（内容、评分、元数据）

#### 6. HealthCheck - 健康检查
```protobuf
rpc HealthCheck(HealthCheckRequest) returns (HealthCheckResponse);
```
- **功能**: 检查服务健康状态
- **输入**: 空
- **输出**: 健康状态、服务版本

## 🐳 Docker部署

### 使用Docker Compose（推荐）

1. 设置环境变量：
```bash
export DASHSCOPE_API_KEY="your_api_key_here"
```

2. 启动服务：
```bash
docker-compose up -d
```

3. 查看服务状态：
```bash
docker-compose ps
docker-compose logs knowledge-base-rpc
```

### 使用Docker

```bash
# 构建镜像
docker build -t knowledge-base-rpc .

# 运行容器
docker run -d \
  --name knowledge-base-rpc \
  -p 50051:50051 \
  -e DASHSCOPE_API_KEY="your_api_key" \
  -v $(pwd)/vector_store:/app/vector_store \
  -v $(pwd)/resources:/app/resources \
  knowledge-base-rpc
```

## 💻 客户端使用示例

### Python客户端

```python
from src.grpc_client import KnowledgeServiceClient

# 创建客户端
client = KnowledgeServiceClient('localhost:50051')

# 健康检查
if client.health_check():
    print("服务正常")

# 发送问题
response = client.chat("什么是API？", use_feedback=True)
if response:
    print(f"答案: {response.final_answer}")
    
    # 提交正面反馈
    feedback_id = client.submit_feedback(
        question="什么是API？",
        original_answer=response.original_answer,
        feedback_type="positive"
    )
    print(f"反馈ID: {feedback_id}")

# 关闭连接
client.close()
```

### 其他语言客户端

可以使用proto文件生成其他语言的客户端代码：

```bash
# Java
protoc --java_out=./java --grpc-java_out=./java proto/knowledge_service.proto

# Go
protoc --go_out=./go --go-grpc_out=./go proto/knowledge_service.proto

# C#
protoc --csharp_out=./csharp --grpc_out=./csharp proto/knowledge_service.proto
```

## 🔧 配置说明

### 环境变量

- `DASHSCOPE_API_KEY`: 通义千问API密钥（必需）
- `PYTHONPATH`: Python路径（Docker中自动设置）

### 配置文件

配置文件位于 `config/config.py`，包含：
- 模型配置（模型名称、参数等）
- 向量存储配置（路径、分块大小等）
- 文档处理配置（支持的文件类型等）

## 📊 监控和日志

### 日志查看

```bash
# Docker环境
docker-compose logs -f knowledge-base-rpc

# 本地环境
# 日志会输出到控制台
```

### 健康检查

```bash
# 使用客户端检查
python src/grpc_client.py --health

# 使用curl（需要grpcurl工具）
grpcurl -plaintext localhost:50051 knowledge_service.KnowledgeService/HealthCheck
```

### 性能监控

```bash
# 运行性能测试
python test_grpc_client.py --performance
```

## 🔒 安全考虑

1. **API密钥保护**: 不要在代码中硬编码API密钥，使用环境变量
2. **网络安全**: 生产环境建议使用TLS加密
3. **访问控制**: 可以添加认证和授权机制
4. **限流**: 建议添加请求限流机制

## 🚀 扩展功能

### 添加TLS支持

```python
# 服务器端
server_credentials = grpc.ssl_server_credentials([
    (private_key, certificate_chain)
])
server.add_secure_port('[::]:50051', server_credentials)

# 客户端
credentials = grpc.ssl_channel_credentials()
channel = grpc.secure_channel('localhost:50051', credentials)
```

### 添加认证

```python
# 使用拦截器添加认证
class AuthInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        # 验证认证信息
        return continuation(handler_call_details)
```

## 🐛 故障排除

### 常见问题

1. **连接失败**
   - 检查服务器是否启动
   - 检查端口是否被占用
   - 检查防火墙设置

2. **知识库未初始化**
   - 确保向量存储文件存在
   - 检查API密钥是否正确
   - 运行知识库构建脚本

3. **依赖包问题**
   - 重新安装依赖: `pip install -r requirements.txt`
   - 检查Python版本兼容性

### 调试模式

```bash
# 启用详细日志
export GRPC_VERBOSITY=DEBUG
export GRPC_TRACE=all
python run_grpc_server.py
```

## 📞 技术支持

如有问题，请：
1. 查看日志文件
2. 运行测试脚本诊断
3. 检查配置文件
4. 提交Issue并附上错误信息

---

**注意**: 首次使用前请确保已正确配置DashScope API密钥并构建了知识库。