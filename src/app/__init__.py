#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库系统核心模块

这个包包含了知识库系统的核心功能：
- 配置管理 (config)
- 知识库操作 (knowledge_base)
- 知识库构建 (build_knowledge_base)
- 启动脚本 (starter)
"""

__version__ = "1.0.0"
__author__ = "Knowledge Base Team"

# 导入核心模块
try:
    from .config.config import get_config, reload_config, validate_config
    from .knowledge_base import KnowledgeBase
    from .build_knowledge_base import KnowledgeBaseBuilder
except ImportError:
    # 如果相对导入失败，使用绝对导入
    pass

__all__ = [
    'get_config',
    'reload_config', 
    'validate_config',
    'KnowledgeBase',
    'KnowledgeBaseBuilder'
]