#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gRPC代码生成脚本
从proto文件生成Python gRPC代码
"""

import os
import subprocess
import sys
from pathlib import Path

# 设置控制台编码为UTF-8（Windows兼容性）
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

def generate_grpc_code():
    """生成gRPC Python代码"""
    # 获取当前脚本目录
    current_dir = Path(__file__).parent
    proto_dir = current_dir / "proto"
    output_dir = current_dir / "grpc_generated"
    
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # proto文件路径
    proto_file = proto_dir / "knowledge_service.proto"
    
    if not proto_file.exists():
        print(f"错误: proto文件不存在 {proto_file}")
        return False
    
    # 生成gRPC代码的命令
    cmd = [
        sys.executable, "-m", "grpc_tools.protoc",
        f"--proto_path={proto_dir}",
        f"--python_out={output_dir}",
        f"--grpc_python_out={output_dir}",
        str(proto_file)
    ]
    
    print("🔧 生成gRPC Python代码...")
    print(f"📂 Proto文件: {proto_file}")
    print(f"📁 输出目录: {output_dir}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ gRPC代码生成成功!")
        
        # 创建__init__.py文件
        init_file = output_dir / "__init__.py"
        init_content = """# gRPC generated code

# 导出生成的模块
from . import knowledge_service_pb2
from . import knowledge_service_pb2_grpc

__all__ = ['knowledge_service_pb2', 'knowledge_service_pb2_grpc']
"""
        init_file.write_text(init_content)
        
        # 修复grpc文件中的导入问题
        grpc_file = output_dir / "knowledge_service_pb2_grpc.py"
        if grpc_file.exists():
            content = grpc_file.read_text(encoding='utf-8')
            # 将绝对导入改为相对导入
            content = content.replace(
                "import knowledge_service_pb2 as knowledge__service__pb2",
                "from . import knowledge_service_pb2 as knowledge__service__pb2"
            )
            grpc_file.write_text(content, encoding='utf-8')
            print("🔧 修复了gRPC文件中的导入问题")
        
        # 列出生成的文件
        generated_files = list(output_dir.glob("*.py"))
        print("📄 生成的文件:")
        for file in generated_files:
            print(f"  - {file.name}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 生成失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        return False

if __name__ == "__main__":
    success = generate_grpc_code()
    sys.exit(0 if success else 1)