#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库演示脚本

这个脚本展示了基于docs目录构建的本地知识库的基本功能。
"""

import os
import json
from pathlib import Path
import re

def load_all_documents(docs_path="./docs"):
    """加载所有markdown文档"""
    docs_path = Path(docs_path)
    documents = []
    
    if not docs_path.exists():
        print(f"❌ 文档目录不存在: {docs_path}")
        return documents
    
    print(f"📚 正在扫描文档目录: {docs_path}")
    
    # 递归查找所有.md文件
    md_files = list(docs_path.glob("**/*.md"))
    
    for file_path in md_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            relative_path = file_path.relative_to(docs_path)
            
            documents.append({
                'path': str(relative_path),
                'full_path': str(file_path),
                'content': content,
                'size': len(content),
                'lines': len(content.split('\n'))
            })
            
        except Exception as e:
            print(f"⚠️  读取文件失败 {file_path}: {e}")
    
    return documents

def analyze_documents(documents):
    """分析文档统计信息"""
    if not documents:
        return {}
    
    total_size = sum(doc['size'] for doc in documents)
    total_lines = sum(doc['lines'] for doc in documents)
    
    # 按目录分组
    dir_stats = {}
    for doc in documents:
        dir_name = str(Path(doc['path']).parent)
        if dir_name not in dir_stats:
            dir_stats[dir_name] = {'count': 0, 'size': 0}
        dir_stats[dir_name]['count'] += 1
        dir_stats[dir_name]['size'] += doc['size']
    
    # 找出最大的文档
    largest_doc = max(documents, key=lambda x: x['size'])
    
    return {
        'total_docs': len(documents),
        'total_size': total_size,
        'total_lines': total_lines,
        'avg_size': total_size // len(documents),
        'directories': dir_stats,
        'largest_doc': largest_doc
    }

def simple_search(documents, query, max_results=5):
    """简单的文档搜索"""
    query_lower = query.lower()
    results = []
    
    for doc in documents:
        content_lower = doc['content'].lower()
        
        # 计算匹配度
        matches = content_lower.count(query_lower)
        if matches > 0:
            # 提取包含查询词的片段
            snippets = []
            lines = doc['content'].split('\n')
            
            for i, line in enumerate(lines):
                if query_lower in line.lower():
                    # 获取上下文（前后各1行）
                    start = max(0, i-1)
                    end = min(len(lines), i+2)
                    context = '\n'.join(lines[start:end])
                    snippets.append(context.strip())
                    
                    if len(snippets) >= 3:  # 最多3个片段
                        break
            
            results.append({
                'path': doc['path'],
                'matches': matches,
                'snippets': snippets,
                'size': doc['size']
            })
    
    # 按匹配数排序
    results.sort(key=lambda x: x['matches'], reverse=True)
    return results[:max_results]

def show_document_tree(documents):
    """显示文档树结构"""
    print("\n📁 文档结构:")
    print("=" * 50)
    
    # 按路径分组
    tree = {}
    for doc in documents:
        path_parts = Path(doc['path']).parts
        current = tree
        
        for part in path_parts[:-1]:  # 目录部分
            if part not in current:
                current[part] = {}
            current = current[part]
        
        # 文件部分
        filename = path_parts[-1]
        current[filename] = doc
    
    def print_tree(node, prefix="", is_last=True):
        items = list(node.items())
        for i, (name, content) in enumerate(items):
            is_last_item = i == len(items) - 1
            current_prefix = "└── " if is_last_item else "├── "
            
            if isinstance(content, dict) and 'content' in content:
                # 这是一个文件
                print(f"{prefix}{current_prefix}📄 {name} ({content['lines']} 行)")
            else:
                # 这是一个目录
                print(f"{prefix}{current_prefix}📂 {name}/")
                next_prefix = prefix + ("    " if is_last_item else "│   ")
                print_tree(content, next_prefix, is_last_item)
    
    print_tree(tree)

def main():
    """主函数"""
    print("🚀 本地知识库演示")
    print("=" * 50)
    print("基于LangChain的本地文档知识库系统")
    print("文档来源: docs/ 目录")
    
    # 加载文档
    documents = load_all_documents()
    
    if not documents:
        print("\n❌ 没有找到任何文档")
        print("请确保docs目录存在且包含.md文件")
        return
    
    print(f"\n✅ 成功加载 {len(documents)} 个文档")
    
    # 分析文档
    stats = analyze_documents(documents)
    
    print("\n📊 知识库统计信息:")
    print("-" * 30)
    print(f"📄 文档总数: {stats['total_docs']}")
    print(f"📝 总字符数: {stats['total_size']:,}")
    print(f"📏 总行数: {stats['total_lines']:,}")
    print(f"📐 平均大小: {stats['avg_size']:,} 字符")
    print(f"📋 最大文档: {stats['largest_doc']['path']} ({stats['largest_doc']['size']:,} 字符)")
    
    print("\n📂 目录分布:")
    for dir_name, info in stats['directories'].items():
        print(f"  {dir_name}: {info['count']} 个文档, {info['size']:,} 字符")
    
    # 显示文档树
    show_document_tree(documents)
    
    # 演示搜索功能
    print("\n🔍 搜索功能演示:")
    print("=" * 50)
    
    demo_queries = ["API", "账户", "区块", "智能合约", "共识"]
    
    for query in demo_queries:
        print(f"\n🔎 搜索: '{query}'")
        results = simple_search(documents, query, max_results=3)
        
        if results:
            print(f"   找到 {len(results)} 个相关文档:")
            for i, result in enumerate(results, 1):
                print(f"   {i}. 📄 {result['path']} ({result['matches']} 次匹配)")
                if result['snippets']:
                    snippet = result['snippets'][0][:100] + "..." if len(result['snippets'][0]) > 100 else result['snippets'][0]
                    print(f"      > {snippet.replace(chr(10), ' ')}")
        else:
            print("   ❌ 未找到相关文档")
    
    print("\n" + "=" * 50)
    print("💡 完整的LangChain知识库功能:")
    print("   • 安装依赖: pip install -r requirements.txt")
    print("   • 配置API密钥: 编辑 .env 文件")
    print("   • 构建知识库: python build_knowledge_base.py")
    print("   • 启动Web界面: streamlit run app.py")
    print("   • 或使用启动脚本: python start.py")
    
    print("\n🎯 主要功能:")
    print("   • 智能向量搜索")
    print("   • AI问答系统")
    print("   • Web交互界面")
    print("   • 文档语义理解")
    
    print("\n👋 演示完成！")

if __name__ == "__main__":
    main()