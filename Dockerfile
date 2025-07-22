# 使用Python 3.9作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 生成gRPC代码
RUN python generate_grpc.py

# 创建必要的目录
RUN mkdir -p /app/vector_store /app/resources/docs

# 暴露gRPC端口
EXPOSE 50051

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "from src.grpc_client import KnowledgeServiceClient; client = KnowledgeServiceClient('localhost:50051'); exit(0 if client.health_check() else 1)"

# 启动命令
CMD ["python", "run_grpc_server.py", "--host", "0.0.0.0", "--port", "50051"]