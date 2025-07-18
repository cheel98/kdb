import os
import sys
import unittest
import logging
from pathlib import Path

# 添加项目根目录到Python路径以导入config模块
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 添加src目录到Python路径以导入其他模块
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config.config import get_config
from knowledge_base import KnowledgeBase

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestKDB(unittest.TestCase):
    def testResource(self):
        print("测试Python环境和文档加载")
        print("当前工作目录:", os.getcwd())

        try:
            config = get_config()
            docs_path = Path(config.document.docs_path)
            print(f"docs目录是否存在: {docs_path.exists()}")

            if docs_path.exists():
                md_files = list(docs_path.glob("**/*.md"))
                print(f"找到 {len(md_files)} 个markdown文件")
                
                for i, file_path in enumerate(md_files[:5]):  # 只显示前5个
                    print(f"{i+1}. {file_path}")
                    
                if len(md_files) > 5:
                    print(f"... 还有 {len(md_files) - 5} 个文件")
            else:
                print("docs目录不存在")
        except Exception as e:
            print(f"配置加载失败: {e}")

        print("测试完成")



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

