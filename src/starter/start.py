#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库系统启动脚本

这个脚本提供了一个简单的命令行界面来管理和使用知识库系统。
"""

import subprocess
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径以导入config模块
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 添加src目录到Python路径以便正确导入模块
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config.config import get_config, validate_config

def check_requirements():
    """检查依赖是否已安装"""
    try:
        import langchain
        import streamlit
        import faiss
        # 移除openai导入，项目使用的是通义千问
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

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

def build_knowledge_base():
    """构建知识库"""
    print("🔨 开始构建知识库...")
    try:
        from build_knowledge_base import KnowledgeBaseBuilder
        builder = KnowledgeBaseBuilder()
        builder.build()
        print("✅ 知识库构建完成！")
        return True
    except Exception as e:
        print(f"❌ 构建知识库失败: {e}")
        return False

def start_web_app():
    """启动Web应用"""
    print("🌐 启动Web应用...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Web应用已停止")
    except Exception as e:
        print(f"❌ 启动Web应用失败: {e}")

def test_knowledge_base():
    """测试知识库"""
    print("🧪 测试知识库...")
    try:
        from knowledge_base import KnowledgeBase
        kb = KnowledgeBase()
        kb.load_vector_store()
        
        # 获取统计信息
        stats = kb.get_stats()
        print(f"📊 知识库统计: {stats}")
        
        # 测试搜索
        test_query = "API"
        results = kb.search_documents(test_query, k=3)
        print(f"🔍 搜索'{test_query}'找到 {len(results)} 个结果")
        
        print("✅ 知识库测试通过！")
        return True
    except Exception as e:
        print(f"❌ 知识库测试失败: {e}")
        return False

def show_menu():
    """显示主菜单"""
    print("\n" + "="*50)
    print("📚 本地知识库系统")
    print("="*50)
    print("1. 🔨 构建知识库")
    print("2. 🧪 测试知识库")
    print("3. 🌐 启动Web应用")
    print("4. 📋 检查系统状态")
    print("5. 🚪 退出")
    print("="*50)

def check_system_status():
    """检查系统状态"""
    print("\n📋 系统状态检查:")
    print("-" * 30)
    
    # 检查依赖
    if check_requirements():
        print("✅ 依赖包已安装")
    
    # 检查API密钥
    if check_api_key():
        print("✅ API密钥已配置")
    
    # 检查向量存储
    vector_store_path = Path("./vector_store")
    if vector_store_path.exists():
        print("✅ 向量存储已存在")
    else:
        print("⚠️  向量存储不存在，需要构建知识库")
    
    # 检查文档目录
    docs_path = Path("./docs")
    if docs_path.exists():
        md_files = list(docs_path.glob("**/*.md"))
        print(f"✅ 文档目录存在，包含 {len(md_files)} 个Markdown文件")
    else:
        print("❌ 文档目录不存在")

def main():
    """主函数"""
    while True:
        show_menu()
        
        try:
            choice = input("\n请选择操作 (1-5): ").strip()
            
            if choice == "1":
                if not check_requirements() or not check_api_key():
                    continue
                build_knowledge_base()
                
            elif choice == "2":
                if not check_requirements() or not check_api_key():
                    continue
                test_knowledge_base()
                
            elif choice == "3":
                if not check_requirements():
                    continue
                start_web_app()
                
            elif choice == "4":
                check_system_status()
                
            elif choice == "5":
                print("👋 再见！")
                break
                
            else:
                print("❌ 无效选择，请输入1-5")
                
        except KeyboardInterrupt:
            print("\n\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")
        
        input("\n按Enter键继续...")

if __name__ == "__main__":
    main()