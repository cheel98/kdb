#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库系统统一入口

功能:
- 启动RPC服务
- 启动Web UI界面(可选)
- 提供统一的命令行参数
"""

import os
import sys
import argparse
import threading
import subprocess
from pathlib import Path
import time

# 设置控制台编码为UTF-8（Windows兼容性）
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

# 获取项目根目录
project_root = Path(__file__).parent

# 添加项目根目录到Python路径
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 添加src目录到Python路径
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# 导入配置模块
try:
    from config.config import get_config
except ImportError:
    print("❌ 导入配置模块失败")
    sys.exit(1)

def check_api_key():
    """检查API密钥"""
    try:
        config = get_config()
        if not config.dashscope.api_key:
            print("❌ 未找到DashScope API密钥")
            print("请设置环境变量 DASHSCOPE_API_KEY 或在 .env 文件中配置")
            return False
        
        print(f"✅ API密钥已配置 (前4位: {config.dashscope.api_key[:4]}...)")
        return True
    except Exception as e:
        print(f"❌ 配置检查失败: {e}")
        return False

def start_rpc_server(host='0.0.0.0', port=50051, workers=10):
    """启动RPC服务器"""
    print("\n🚀 启动知识库gRPC服务器...")
    print(f"🌐 监听地址: {host}:{port}")
    print(f"🔧 工作线程: {workers}")
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
        # 导入并启动服务器
        from src.rpc.grpc_server import serve
        
        # 启动服务器（在当前线程中）
        serve(port=port, max_workers=workers)
        return True
    except ImportError as e:
        print(f"❌ 导入模块失败: {e}")
        print("请确保已安装所有依赖包: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ 启动RPC服务器失败: {e}")
        return False

def start_web_ui(app_type="standard", port=8501):
    """启动Web UI"""
    if app_type == "enhanced":
        app_path = project_root / "src" / "app" / "enhanced_app.py"
        ui_port = 8502  # 增强版使用不同端口
    else:
        app_path = project_root / "src" / "app" / "app.py"
        ui_port = port
    
    if not app_path.exists():
        print(f"❌ 找不到应用文件: {app_path}")
        return False
    
    # 构建streamlit命令
    cmd = [
        sys.executable, 
        "-m", "streamlit", 
        "run", 
        str(app_path),
        f"--server.port={ui_port}",
        "--server.headless=false",
        "--browser.gatherUsageStats=false"
    ]
    
    app_type_name = "增强版" if app_type == "enhanced" else "标准版"
    print(f"\n🚀 启动{app_type_name}知识库Web UI...")
    print(f"📂 应用路径: {app_path}")
    print(f"🌐 访问地址: http://localhost:{ui_port}")
    
    try:
        # 启动应用（创建子进程）
        process = subprocess.Popen(
            cmd, 
            cwd=project_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        
        # 等待服务器启动
        time.sleep(3)
        
        if process.poll() is None:
            print(f"✅ Web UI启动成功")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Web UI启动失败")
            print(f"错误信息: {stderr}")
            return None
    except Exception as e:
        print(f"❌ 启动Web UI失败: {e}")
        return None

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='知识库系统统一入口')
    parser.add_argument('--rpc-port', type=int, default=50051, help='RPC服务端口 (默认: 50051)')
    parser.add_argument('--rpc-host', default='0.0.0.0', help='RPC服务监听地址 (默认: 0.0.0.0)')
    parser.add_argument('--workers', type=int, default=10, help='RPC服务工作线程数 (默认: 10)')
    parser.add_argument('--web-ui', action='store_true', help='是否启动Web UI')
    parser.add_argument('--web-port', type=int, default=8501, help='Web UI端口 (默认: 8501)')
    parser.add_argument('--enhanced', action='store_true', help='使用增强版Web UI (带反馈学习功能)')
    
    args = parser.parse_args()
    
    print("🎯 知识库系统统一入口")
    print("=" * 50)
    
    # 检查API密钥
    if not check_api_key():
        return 1
    
    # 启动Web UI（如果需要）
    web_process = None
    if args.web_ui:
        app_type = "enhanced" if args.enhanced else "standard"
        web_process = start_web_ui(app_type, args.web_port)
        if web_process is None:
            print("⚠️ Web UI启动失败，但将继续启动RPC服务")
    
    # 启动RPC服务器
    try:
        start_rpc_server(args.rpc_host, args.rpc_port, args.workers)
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    finally:
        # 确保Web UI进程被终止
        if web_process and web_process.poll() is None:
            web_process.terminate()
            print("✅ Web UI已停止")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())