import os
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any

# 添加项目根目录到Python路径以导入config模块
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from config.config import get_config
import dashscope

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KnowledgeBaseBuilder:
    """知识库构建器"""
    
    def __init__(self, docs_path: str = None, vector_store_path: str = None):
        # 获取配置
        self.config = get_config()
        
        # 使用配置或默认值
        self.docs_path = Path(docs_path or self.config.document.docs_path)
        self.vector_store_path = Path(vector_store_path or self.config.vector_store.store_path)
        
        # 设置DashScope API密钥
        dashscope.api_key = self.config.dashscope.api_key
        
        # 使用通义千问的embeddings
        self.embeddings = DashScopeEmbeddings(
            model=self.config.dashscope.embedding_model,
            dashscope_api_key=self.config.dashscope.api_key
        )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.vector_store.chunk_size,
            chunk_overlap=self.config.vector_store.chunk_overlap,
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
    try:
        # 获取配置并验证
        config = get_config()
        if not config.validate():
            logger.error("配置验证失败，请检查环境变量设置")
            return
        
        logger.info(f"使用配置: {config}")
        
        # 创建知识库构建器
        builder = KnowledgeBaseBuilder()
        
        # 构建知识库
        builder.build()
        
    except Exception as e:
        logger.error(f"构建知识库失败: {e}")
        raise

if __name__ == "__main__":
    main()