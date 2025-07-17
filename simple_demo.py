#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版本的知识库演示

这个脚本展示了如何在没有安装LangChain等依赖的情况下，
演示知识库的基本概念和文档结构。
"""

import os
import json
from pathlib import Path
from collections import defaultdict
import re

class SimpleKnowledgeBase:
    """简化版知识库，用于演示基本功能"""
    
    def __init__(self, docs_path="./docs"):
        self.docs_path = Path(docs_path)
        self.documents = []
        self.index = defaultdict(list)
        
    def load_documents(self):
        """加载所有markdown文档"""
        print(f"📚 正在加载文档从: {self.docs_path}")
        
        if not self.docs_path.exists():
            print(f"❌ 文档目录不存在: {self.docs_path}")
            return
        
        # 递归查找所有.md文件
        md_files = list(self.docs_path.glob("**/*.md"))
        
        for file_path in md_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                relative_path = file_path.relative_to(self.docs_path)
                
                doc = {
                    'path': str(relative_path),
                    'content': content,
                    'size': len(content),
                    'lines': len(content.split('\n'))
                }
                
                self.documents.append(doc)
                
                # 简单的关键词索引
                words = re.findall(r'\w+', content.lower())
                for word in set(words):
                    if len(word) > 2:  # 忽略太短的词
                        self.index[word].append(len(self.documents) - 1)
                        
            except Exception as e:
                print(f"⚠️  读取文件失败 {file_path}: {e}")
        
        print(f"✅ 成功加载 {len(self.documents)} 个文档")
        
    def search_documents(self, query, max_results=5):
        """简单的文档搜索"""
        query_words = re.findall(r'\w+', query.lower())
        
        # 计算文档得分
        doc_scores = defaultdict(int)
        
        for word in query_words:
            if word in self.index:
                for doc_idx in self.index[word]:
                    doc_scores[doc_idx] += 1
        
        # 按得分排序
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for doc_idx, score in sorted_docs[:max_results]:
            doc = self.documents[doc_idx]
            
            # 查找包含查询词的片段
            content = doc['content']
            snippets = []
            
            for word in query_words:
                pattern = re.compile(f'.{{0,50}}{re.escape(word)}.{{0,50}}', re.IGNORECASE)
                matches = pattern.findall(content)
                snippets.extend(matches[:2])  # 最多2个片段
            
            results.append({
                'path': doc['path'],
                'score': score,
                'snippets': snippets[:3],  # 最多3个片段
                'size': doc['size'],
                'lines': doc['lines']
            })
        
        return results
    
    def get_statistics(self):
        """获取知识库统计信息"""
        if not self.documents:
            return {"status": "空"}
        
        total_size = sum(doc['size'] for doc in self.documents)
        total_lines = sum(doc['lines'] for doc in self.documents)
        
        # 按目录分组统计
        dir_stats = defaultdict(int)
        for doc in self.documents:
            dir_name = str(Path(doc['path']).parent)
            dir_stats[dir_name] += 1
        
        return {
            "文档总数": len(self.documents),
            "总字符数": total_size,
            "总行数": total_lines,
            "索引词汇数": len(self.index),
            "目录分布": dict(dir_stats)
        }
    
    def show_document_tree(self):
        """显示文档树结构"""
        print("\n📁 文档结构:")
        print("-" * 40)
        
        # 按路径排序
        sorted_docs = sorted(self.documents, key=lambda x: x['path'])
        
        current_dir = ""
        for doc in sorted_docs:
            path = Path(doc['path'])
            dir_name = str(path.parent)
            
            if dir_name != current_dir:
                current_dir = dir_name
                if dir_name != ".":
                    print(f"\n📂 {dir_name}/")
            
            indent = "  " if dir_name != "." else ""
            print(f"{indent}📄 {path.name} ({doc['lines']} 行, {doc['size']} 字符)")

def main():
    """主演示函数"""
    print("🚀 简化版知识库演示")
    print("=" * 50)
    
    # 创建知识库实例
    kb = SimpleKnowledgeBase()
    
    # 加载文档
    kb.load_documents()
    
    if not kb.documents:
        print("\n❌ 没有找到任何文档，请确保docs目录存在且包含.md文件")
        return
    
    # 显示统计信息
    stats = kb.get_statistics()
    print("\n📊 知识库统计:")
    print("-" * 30)
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for k, v in value.items():
                print(f"  {k}: {v} 个文档")
        else:
            print(f"{key}: {value}")
    
    # 显示文档树
    kb.show_document_tree()
    
    # 交互式搜索
    print("\n🔍 搜索演示 (输入 'quit' 退出):")
    print("-" * 40)
    
    while True:
        try:
            query = input("\n请输入搜索关键词: ").strip()
            
            if query.lower() in ['quit', 'exit', '退出']:
                break
            
            if not query:
                continue
            
            results = kb.search_documents(query)
            
            if results:
                print(f"\n找到 {len(results)} 个相关文档:")
                for i, result in enumerate(results, 1):
                    print(f"\n{i}. 📄 {result['path']} (得分: {result['score']})")
                    if result['snippets']:
                        print("   片段:")
                        for snippet in result['snippets']:
                            print(f"   > {snippet.strip()}")
            else:
                print("❌ 没有找到相关文档")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ 搜索时发生错误: {e}")
    
    print("\n👋 演示结束")

if __name__ == "__main__":
    main()