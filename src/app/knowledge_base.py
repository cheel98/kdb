import os
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

# 添加项目根目录到Python路径以导入config模块
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Tongyi
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from config.config import get_config
import dashscope

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KnowledgeBase:
    def __init__(self, vector_store_path: str = None):
        """
        初始化知识库
        
        Args:
            vector_store_path: 向量存储路径
        """
        # 获取配置
        self.config = get_config()
        
        self.vector_store_path = Path(vector_store_path or self.config.vector_store.store_path)
        
        # 设置DashScope API密钥
        dashscope.api_key = self.config.dashscope.api_key
        
        # 使用通义千问的embeddings
        self.embeddings = DashScopeEmbeddings(
            model=self.config.dashscope.embedding_model,
            dashscope_api_key=self.config.dashscope.api_key
        )
        
        # 使用通义千问LLM
        self.llm = Tongyi(
            temperature=self.config.dashscope.temperature,
            max_tokens=self.config.dashscope.max_tokens,
            top_p=self.config.dashscope.top_p
        )
        
        self.vector_store = None
        self.qa_chain = None
        
        # 自定义提示模板
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""基于以下上下文信息回答问题。如果上下文中没有相关信息，请说明无法从提供的文档中找到答案。

上下文信息：
{context}

问题：{question}

回答："""
        )
    
    def load_vector_store(self):
        """加载本地向量存储"""
        if not self.vector_store_path.exists():
            raise FileNotFoundError(f"向量存储路径不存在: {self.vector_store_path}")
        
        logger.info(f"加载向量存储: {self.vector_store_path}")
        self.vector_store = FAISS.load_local(
            str(self.vector_store_path), 
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        
        # 创建QA链
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 5}),
            chain_type_kwargs={"prompt": self.prompt_template},
            return_source_documents=True
        )
        
        logger.info("向量存储加载完成")
    
    def search_documents(self, query: str, k: int = None) -> List[Dict[str, Any]]:
        """搜索相关文档"""
        if not self.vector_store:
            raise ValueError("向量存储未加载，请先调用load_vector_store()")
        
        k = k or self.config.vector_store.search_k
        logger.info(f"搜索查询: {query}，返回数量: {k}")
        
        # 执行相似性搜索
        if self.config.vector_store.search_type == "similarity":
            docs = self.vector_store.similarity_search_with_score(query, k=k)
        elif self.config.vector_store.search_type == "mmr":
            docs = self.vector_store.max_marginal_relevance_search(query, k=k)
            docs = [(doc, 0.0) for doc in docs]  # MMR doesn't return scores
        else:
            docs = self.vector_store.similarity_search_with_score(query, k=k)
        
        results = []
        for doc, score in docs:
            results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "similarity_score": score
            })
        
        logger.info(f"找到 {len(results)} 个相关文档")
        return results
    
    def ask_question(self, question: str) -> Dict[str, Any]:
        """基于知识库回答问题"""
        if not self.qa_chain:
            raise ValueError("QA链未初始化，请先调用load_vector_store()")
        
        logger.info(f"处理问题: {question}")
        
        # 执行问答
        result = self.qa_chain({"query": question})
        
        # 整理返回结果
        response = {
            "question": question,
            "answer": result["result"],
            "source_documents": [
                {
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "未知"),
                    "metadata": doc.metadata
                }
                for doc in result["source_documents"]
            ]
        }
        
        return response
    
    def get_stats(self) -> Dict[str, Any]:
        """获取知识库统计信息"""
        if not self.vector_store:
            return {"status": "未加载"}
        
        # 获取向量存储中的文档数量
        index_to_docstore_id = self.vector_store.index_to_docstore_id
        doc_count = len(index_to_docstore_id)
        
        return {
            "status": "已加载",
            "document_count": doc_count,
            "vector_store_path": str(self.vector_store_path)
        }

def main():
    """演示知识库使用"""
    try:
        # 获取配置并验证
        config = get_config()
        if not config.validate():
            logger.error("配置验证失败，请检查环境变量设置")
            return
        
        logger.info(f"使用配置: {config}")
        
        # 创建知识库实例
        kb = KnowledgeBase()
        
        # 加载向量存储
        kb.load_vector_store()
        
        # 测试搜索
        query = "什么是API？"
        print(f"\n搜索查询: {query}")
        docs = kb.search_documents(query)
        
        for i, doc in enumerate(docs, 1):
            print(f"\n文档 {i}:")
            print(f"内容: {doc['content'][:200]}...")
            print(f"来源: {doc['metadata'].get('source', 'Unknown')}")
            print(f"相似度: {doc['similarity_score']:.4f}")
        
        # 测试问答
        print(f"\n问答测试: {query}")
        answer = kb.ask_question(query)
        print(f"回答: {answer['answer']}")
        
        # 获取统计信息
        stats = kb.get_stats()
        print(f"\n知识库统计: {stats}")
        
    except Exception as e:
        logger.error(f"知识库操作失败: {e}")
        raise

if __name__ == "__main__":
    main()
