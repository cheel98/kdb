import os
import logging
from pathlib import Path
from typing import List, Dict, Any

from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document
from dotenv import load_dotenv
import dashscope

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KnowledgeBaseBuilder:
    def __init__(self, docs_path: str = "./docs", vector_store_path: str = "./vector_store"):
        self.docs_path = Path(docs_path)
        self.vector_store_path = Path(vector_store_path)
        
        # 设置DashScope API密钥
        dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
        
        # 使用通义千问的embeddings
        self.embeddings = DashScopeEmbeddings(
            model="text-embedding-v1",
            dashscope_api_key=os.getenv('DASHSCOPE_API_KEY')
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
    def load_documents(self) -> List[Document]:
        """加载docs目录下的所有markdown文档"""
        logger.info(f"开始加载文档，路径: {self.docs_path}")
        
        # 使用DirectoryLoader加载markdown文件
        loader = DirectoryLoader(
            str(self.docs_path),
            glob="**/*.md",
            loader_cls=TextLoader,
            loader_kwargs={'encoding': 'utf-8'}
        )
        
        documents = loader.load()
        logger.info(f"成功加载 {len(documents)} 个文档")
        
        # 为每个文档添加元数据
        for doc in documents:
            # 获取相对路径作为source
            relative_path = Path(doc.metadata['source']).relative_to(self.docs_path)
            doc.metadata['source'] = str(relative_path)
            doc.metadata['type'] = 'markdown'
            
        return documents
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """将文档分割成小块"""
        logger.info("开始分割文档")
        
        texts = self.text_splitter.split_documents(documents)
        logger.info(f"文档分割完成，共生成 {len(texts)} 个文本块")
        
        return texts
    
    def create_vector_store(self, texts: List[Document]) -> FAISS:
        """创建向量存储"""
        logger.info("开始创建向量存储")
        
        # 创建FAISS向量存储
        vector_store = FAISS.from_documents(texts, self.embeddings)
        
        logger.info("向量存储创建完成")
        return vector_store
    
    def save_vector_store(self, vector_store: FAISS):
        """保存向量存储到本地"""
        logger.info(f"保存向量存储到: {self.vector_store_path}")
        
        # 确保目录存在
        self.vector_store_path.mkdir(parents=True, exist_ok=True)
        
        # 保存向量存储
        vector_store.save_local(str(self.vector_store_path))
        logger.info("向量存储保存完成")
    
    def build(self):
        """构建知识库的完整流程"""
        try:
            # 1. 加载文档
            documents = self.load_documents()
            
            if not documents:
                logger.warning("没有找到任何文档")
                return
            
            # 2. 分割文档
            texts = self.split_documents(documents)
            
            # 3. 创建向量存储
            vector_store = self.create_vector_store(texts)
            
            # 4. 保存向量存储
            self.save_vector_store(vector_store)
            
            logger.info("知识库构建完成！")
            
        except Exception as e:
            logger.error(f"构建知识库时发生错误: {str(e)}")
            raise

def main():
    """主函数"""
    # 检查通义千问API密钥
    if not os.getenv('DASHSCOPE_API_KEY'):
        logger.error("请设置DASHSCOPE_API_KEY环境变量")
        return
    
    # 创建知识库构建器
    builder = KnowledgeBaseBuilder()
    
    # 构建知识库
    builder.build()

if __name__ == "__main__":
    main()