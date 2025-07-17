import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

from langchain_community.embeddings import DashScopeEmbeddings
from langchain.vectorstores import FAISS
from langchain_community.llms import Tongyi
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import dashscope

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KnowledgeBase:
    def __init__(self, vector_store_path: str = "./vector_store"):
        self.vector_store_path = Path(vector_store_path)
        
        # 设置DashScope API密钥
        dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
        
        # 使用通义千问的embeddings
        self.embeddings = DashScopeEmbeddings(
            model="text-embedding-v1",
            dashscope_api_key=os.getenv('DASHSCOPE_API_KEY')
        )
        
        # 使用通义千问LLM
        self.llm = Tongyi(temperature=0)
        
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
    
    def search_documents(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """搜索相关文档"""
        if not self.vector_store:
            raise ValueError("向量存储未加载，请先调用load_vector_store()")
        
        # 执行相似性搜索
        docs = self.vector_store.similarity_search_with_score(query, k=k)
        
        results = []
        for doc, score in docs:
            results.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "similarity_score": score
            })
        
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
    # 检查DashScope API密钥
    if not os.getenv('DASHSCOPE_API_KEY'):
        logger.error("请设置DASHSCOPE_API_KEY环境变量")
        return
    
    try:
        # 创建知识库实例
        kb = KnowledgeBase()
        
        # 加载向量存储
        kb.load_vector_store()
        
        # 显示统计信息
        stats = kb.get_stats()
        print(f"知识库状态: {stats}")
        
        # 示例查询
        test_questions = [
            "什么是共识算法？",
            "如何部署智能合约？",
            "API接口有哪些？"
        ]
        
        for question in test_questions:
            print(f"\n问题: {question}")
            response = kb.ask_question(question)
            print(f"回答: {response['answer']}")
            print(f"参考文档数量: {len(response['source_documents'])}")
            
    except Exception as e:
        logger.error(f"运行时发生错误: {str(e)}")

if __name__ == "__main__":
    main()