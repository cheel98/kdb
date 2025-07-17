#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通义千问配置测试脚本
测试DashScope API连接和基本功能
"""

import os
from dotenv import load_dotenv
import dashscope
from pathlib import Path

# 加载环境变量
load_dotenv()

def test_dashscope_connection():
    """测试DashScope API连接"""
    print("=== 通义千问配置测试 ===")
    
    # 检查API密钥
    api_key = os.getenv('DASHSCOPE_API_KEY')
    if not api_key:
        print("❌ 未找到DASHSCOPE_API_KEY环境变量")
        print("请在.env文件中设置您的DashScope API密钥")
        return False
    
    print(f"✅ API密钥已配置 (前4位: {api_key[:4]}...)")
    
    # 设置API密钥
    dashscope.api_key = api_key
    
    try:
        # 测试文本生成
        from dashscope import Generation
        
        response = Generation.call(
            model='qwen-turbo',
            prompt='你好，请简单介绍一下你自己。',
            max_tokens=100
        )
        
        if response.status_code == 200:
            print("✅ 通义千问文本生成测试成功")
            print(f"回复: {response.output.text[:50]}...")
        else:
            print(f"❌ 文本生成测试失败: {response.message}")
            return False
            
    except Exception as e:
        print(f"❌ 文本生成测试异常: {str(e)}")
        return False
    
    try:
        # 测试文本嵌入
        from dashscope import TextEmbedding
        
        response = TextEmbedding.call(
            model=TextEmbedding.Models.text_embedding_v1,
            input="这是一个测试文本"
        )
        
        if response.status_code == 200:
            print("✅ 通义千问文本嵌入测试成功")
            embeddings = response.output['embeddings'][0]['embedding']
            print(f"嵌入向量维度: {len(embeddings)}")
        else:
            print(f"❌ 文本嵌入测试失败: {response.message}")
            return False
            
    except Exception as e:
        print(f"❌ 文本嵌入测试异常: {str(e)}")
        return False
    
    print("\n🎉 所有测试通过！通义千问配置正确。")
    return True

def test_langchain_integration():
    """测试LangChain集成"""
    print("\n=== LangChain集成测试 ===")
    
    try:
        from langchain_community.embeddings import DashScopeEmbeddings
        from langchain_community.llms import Tongyi
        
        # 测试嵌入模型
        embeddings = DashScopeEmbeddings(
            model="text-embedding-v1",
            dashscope_api_key=os.getenv('DASHSCOPE_API_KEY')
        )
        
        test_text = "这是一个测试文档"
        embedding_result = embeddings.embed_query(test_text)
        
        print(f"✅ LangChain嵌入模型测试成功")
        print(f"嵌入向量维度: {len(embedding_result)}")
        
        # 测试语言模型
        llm = Tongyi(temperature=0)
        response = llm("请用一句话介绍人工智能。")
        
        print(f"✅ LangChain语言模型测试成功")
        print(f"回复: {response[:50]}...")
        
    except Exception as e:
        print(f"❌ LangChain集成测试失败: {str(e)}")
        return False
    
    print("\n🎉 LangChain集成测试通过！")
    return True

def main():
    """主函数"""
    print("通义千问知识库系统配置测试\n")
    
    # 检查当前目录
    current_dir = Path.cwd()
    print(f"当前工作目录: {current_dir}")
    
    # 检查.env文件
    env_file = current_dir / ".env"
    if env_file.exists():
        print("✅ .env文件存在")
    else:
        print("⚠️  .env文件不存在，请创建并配置API密钥")
    
    print()
    
    # 运行测试
    success = True
    
    if not test_dashscope_connection():
        success = False
    
    if not test_langchain_integration():
        success = False
    
    if success:
        print("\n🎉 所有测试通过！系统配置正确，可以开始使用知识库功能。")
        print("\n下一步:")
        print("1. 运行 python build_knowledge_base.py 构建知识库")
        print("2. 运行 streamlit run app.py 启动Web界面")
    else:
        print("\n❌ 部分测试失败，请检查配置。")

if __name__ == "__main__":
    main()