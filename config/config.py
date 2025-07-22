#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块
统一管理环境变量配置，避免重复读取
"""

import os
from dataclasses import dataclass, field
from typing import Optional, List
from dotenv import load_dotenv
from pathlib import Path

# 加载环境变量
load_dotenv()

@dataclass
class DashScopeConfig:
    """通义千问配置"""
    api_key: str
    model_name: str = "qwen-turbo"
    embedding_model: str = "text-embedding-v1"
    temperature: float = 0.0
    max_tokens: int = 2000
    top_p: float = 0.8
    
    def __post_init__(self):
        """验证配置"""
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY 环境变量未设置")
        
        if self.temperature < 0 or self.temperature > 1:
            raise ValueError("temperature 必须在 0-1 之间")
        
        if self.top_p < 0 or self.top_p > 1:
            raise ValueError("top_p 必须在 0-1 之间")

@dataclass
class VectorStoreConfig:
    """向量存储配置"""
    store_path: str = "./vector_store"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    search_k: int = 4
    search_type: str = "similarity"
    
    def __post_init__(self):
        """验证配置"""
        if self.chunk_size <= 0:
            raise ValueError("chunk_size 必须大于 0")
        
        if self.chunk_overlap < 0:
            raise ValueError("chunk_overlap 不能为负数")
        
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("chunk_overlap 必须小于 chunk_size")
        
        if self.search_k <= 0:
            raise ValueError("search_k 必须大于 0")
        
        if self.search_type not in ["similarity", "mmr"]:
            raise ValueError("search_type 必须是 'similarity' 或 'mmr'")

@dataclass
class DocumentConfig:
    """文档配置"""
    docs_path: str = "./docs"
    supported_extensions: List[str] = field(default_factory=lambda: [".md", ".txt", ".rst"])
    encoding: str = "utf-8"
    recursive: bool = True
    
    def __post_init__(self):
        """验证配置（仅警告，不抛出异常）"""
        docs_path = Path(self.docs_path)
        if not docs_path.exists():
            print(f"⚠️  警告: 文档路径不存在: {self.docs_path}")
            print(f"   如需使用知识库功能，请确保该路径存在并包含文档文件")
        elif not docs_path.is_dir():
            print(f"⚠️  警告: 文档路径不是目录: {self.docs_path}")

@dataclass
class StreamlitConfig:
    """Streamlit配置"""
    host: str = "localhost"
    port: int = 8501
    debug: bool = False
    
    def __post_init__(self):
        """验证配置"""
        if self.port < 1 or self.port > 65535:
            raise ValueError("端口号必须在 1-65535 之间")

@dataclass
class GrpcConfig:
    """gRPC服务配置"""
    host: str = "0.0.0.0"
    port: int = 50051
    max_workers: int = 10
    enable_reflection: bool = False
    enable_health_check: bool = True
    
    def __post_init__(self):
        """验证配置"""
        if self.port < 1 or self.port > 65535:
            raise ValueError("gRPC端口号必须在 1-65535 之间")
        
        if self.max_workers <= 0:
            raise ValueError("max_workers 必须大于 0")
        
        # 验证主机地址格式
        if not self.host:
            raise ValueError("gRPC主机地址不能为空")

@dataclass
class LoggingConfig:
    """日志配置"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = None
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    
    def __post_init__(self):
        """验证配置"""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.level.upper() not in valid_levels:
            raise ValueError(f"日志级别必须是: {', '.join(valid_levels)}")
        
        if self.max_file_size <= 0:
            raise ValueError("max_file_size 必须大于 0")
        
        if self.backup_count < 0:
            raise ValueError("backup_count 不能为负数")

class Config:
    """全局配置管理器"""
    
    def __init__(self):
        """初始化配置"""
        self._load_config()
    
    def _load_config(self):
        """加载所有配置"""
        try:
            # 通义千问配置
            self.dashscope = DashScopeConfig(
                api_key=os.getenv('DASHSCOPE_API_KEY', ''),
                model_name=os.getenv('QWEN_MODEL_NAME', 'qwen-turbo'),
                embedding_model=os.getenv('QWEN_EMBEDDING_MODEL', 'text-embedding-v1'),
                temperature=float(os.getenv('QWEN_TEMPERATURE', '0.0')),
                max_tokens=int(os.getenv('QWEN_MAX_TOKENS', '2000')),
                top_p=float(os.getenv('QWEN_TOP_P', '0.8'))
            )
            
            # 向量存储配置
            self.vector_store = VectorStoreConfig(
                store_path=os.getenv('VECTOR_STORE_PATH', './vector_store'),
                chunk_size=int(os.getenv('CHUNK_SIZE', '1000')),
                chunk_overlap=int(os.getenv('CHUNK_OVERLAP', '200')),
                search_k=int(os.getenv('SEARCH_K', '4')),
                search_type=os.getenv('SEARCH_TYPE', 'similarity')
            )
            
            # 文档配置
            self.document = DocumentConfig(
                docs_path=os.getenv('DOCS_PATH', './docs'),
                encoding=os.getenv('DOCS_ENCODING', 'utf-8'),
                recursive=os.getenv('DOCS_RECURSIVE', 'true').lower() == 'true'
            )
            
            # Streamlit配置
            self.streamlit = StreamlitConfig(
                host=os.getenv('STREAMLIT_HOST', 'localhost'),
                port=int(os.getenv('STREAMLIT_PORT', '8501')),
                debug=os.getenv('STREAMLIT_DEBUG', 'false').lower() == 'true'
            )
            
            # gRPC配置
            self.grpc = GrpcConfig(
                host=os.getenv('GRPC_HOST', '0.0.0.0'),
                port=int(os.getenv('GRPC_PORT', '50051')),
                max_workers=int(os.getenv('GRPC_MAX_WORKERS', '10')),
                enable_reflection=os.getenv('GRPC_ENABLE_REFLECTION', 'false').lower() == 'true',
                enable_health_check=os.getenv('GRPC_ENABLE_HEALTH_CHECK', 'true').lower() == 'true'
            )
            
            # 日志配置
            self.logging = LoggingConfig(
                level=os.getenv('LOG_LEVEL', 'INFO'),
                format=os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
                file_path=os.getenv('LOG_FILE_PATH'),
                max_file_size=int(os.getenv('LOG_MAX_FILE_SIZE', str(10 * 1024 * 1024))),
                backup_count=int(os.getenv('LOG_BACKUP_COUNT', '5'))
            )
            
        except ValueError as e:
            raise ValueError(f"配置加载失败: {e}")
        except Exception as e:
            raise RuntimeError(f"配置初始化异常: {e}")
    
    def reload(self):
        """重新加载配置"""
        load_dotenv(override=True)
        self._load_config()
    
    def validate(self) -> bool:
        """验证所有配置"""
        try:
            # 检查API密钥
            if not self.dashscope.api_key:
                return False
            
            # 检查文档路径
            if not Path(self.document.docs_path).exists():
                return False
            
            # 检查向量存储路径的父目录
            vector_parent = Path(self.vector_store.store_path).parent
            if not vector_parent.exists():
                vector_parent.mkdir(parents=True, exist_ok=True)
            
            return True
            
        except Exception:
            return False
    
    def get_env_info(self) -> dict:
        """获取环境信息"""
        return {
            "python_version": os.sys.version,
            "working_directory": os.getcwd(),
            "env_file_exists": Path(".env").exists(),
            "docs_path_exists": Path(self.document.docs_path).exists(),
            "vector_store_path": self.vector_store.store_path,
            "api_key_configured": bool(self.dashscope.api_key)
        }
    
    def __str__(self) -> str:
        """字符串表示"""
        return f"""配置信息:
- DashScope模型: {self.dashscope.model_name}
- 嵌入模型: {self.dashscope.embedding_model}
- 文档路径: {self.document.docs_path}
- 向量存储: {self.vector_store.store_path}
- 分块大小: {self.vector_store.chunk_size}
- 搜索数量: {self.vector_store.search_k}
- gRPC服务: {self.grpc.host}:{self.grpc.port}
- gRPC工作线程: {self.grpc.max_workers}
- 日志级别: {self.logging.level}"""

# 全局配置实例
config = Config()

# 便捷访问函数
def get_config() -> Config:
    """获取全局配置实例"""
    return config

def reload_config():
    """重新加载配置"""
    global config
    config.reload()

def validate_config() -> bool:
    """验证配置"""
    return config.validate()

