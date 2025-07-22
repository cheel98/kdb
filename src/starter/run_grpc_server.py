#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动知识库gRPC服务器
提供RPC接口的后端服务
"""

import os
import sys
import argparse
from pathlib import Path

# 设置控制台编码为UTF-8（Windows兼容性）
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

def main():
    """启动gRPC服务器"""
    print("🚀 启动知识库gRPC服务器...")
    # 获取当前脚本所在目录
    current_dir = Path(__file__).parent
    
    # 设置环境变量
    os.environ['PYTHONPATH'] = str(current_dir)
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='知识库gRPC服务器')
    parser.add_argument('--port', type=int, default=50051, help='服务端口 (默认: 50051)')
    parser.add_argument('--workers', type=int, default=10, help='最大工作线程数 (默认: 10)')
    parser.add_argument('--host', default='0.0.0.0', help='监听地址 (默认: 0.0.0.0)')
    
    args = parser.parse_args()
    
    print("🚀 启动知识库gRPC服务器...")
    print(f"📂 工作目录: {current_dir}")
    print(f"🌐 监听地址: {args.host}:{args.port}")
    print(f"🔧 工作线程: {args.workers}")
    print("\n" + "="*60)
    print("🧠 智能知识库RPC服务")
    print("="*60)
    print("📡 提供的RPC接口:")
    print("  • Chat - 智能问答")
    print("  • SubmitFeedback - 反馈收集")
    print("  • GetFeedbackHistory - 反馈历史")
    print("  • GetStats - 系统统计")
    print("  • SearchDocuments - 文档搜索")
    print("  • HealthCheck - 健康检查")
    print("="*60 + "\n")
    
    try:
        # 获取项目根目录并设置路径
        project_root = current_dir.parent.parent
        sys.path.insert(0, str(project_root))
        
        # 导入并启动服务器
        from src.rpc.grpc_server import serve
        
        # 启动服务器
        serve(port=args.port, max_workers=args.workers)
        
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
        return 0
    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        print("请确保已安装所有依赖包: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)