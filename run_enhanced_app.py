#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动增强版知识库应用
集成反馈学习功能的Streamlit应用启动器
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """启动增强版知识库应用"""
    # 获取当前脚本所在目录
    current_dir = Path(__file__).parent
    
    # 设置环境变量
    os.environ['PYTHONPATH'] = str(current_dir)
    
    # 构建streamlit命令
    enhanced_app_path = current_dir / "src" / "enhanced_app.py"
    
    if not enhanced_app_path.exists():
        print(f"错误: 找不到应用文件 {enhanced_app_path}")
        return 1
    
    # 启动streamlit应用
    cmd = [
        sys.executable, 
        "-m", "streamlit", 
        "run", 
        str(enhanced_app_path),
        "--server.port=8502",  # 使用不同的端口避免冲突
        "--server.headless=false",
        "--browser.gatherUsageStats=false"
    ]
    
    print("🚀 启动增强版知识库应用...")
    print(f"📂 应用路径: {enhanced_app_path}")
    print(f"🌐 访问地址: http://localhost:8502")
    print("\n" + "="*50)
    print("🧠 智能知识库系统 - 反馈学习版")
    print("="*50)
    print("✨ 新功能:")
    print("  • 用户反馈收集 (👍👎✏️)")
    print("  • 基于反馈的答案优化")
    print("  • 相似问题推荐")
    print("  • 学习效果分析")
    print("  • 反馈数据导出")
    print("="*50 + "\n")
    
    try:
        # 启动应用
        result = subprocess.run(cmd, cwd=current_dir)
        return result.returncode
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
        return 0
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)