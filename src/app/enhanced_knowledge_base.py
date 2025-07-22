#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强的知识库系统
集成反馈学习功能的知识库
"""

import os
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 修改相对导入为绝对导入
from src.app.knowledge_base import KnowledgeBase
from src.app.feedback_system import FeedbackLearningSystem, FeedbackRecord
from config.config import get_config

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedKnowledgeBase(KnowledgeBase):
    """增强的知识库，集成反馈学习功能"""
    
    def __init__(self, vector_store_path: str = None, feedback_db_path: str = None):
        """
        初始化增强知识库
        
        Args:
            vector_store_path: 向量存储路径
            feedback_db_path: 反馈数据库路径
        """
        super().__init__(vector_store_path)
        
        # 初始化反馈学习系统
        self.feedback_db_path = feedback_db_path or "./feedback.db"
        self.feedback_system = FeedbackLearningSystem(self.feedback_db_path)
        
        # 配置参数
        self.enable_feedback_learning = True
        self.confidence_threshold = 0.7
        self.similarity_threshold = 0.8
        
        logger.info("增强知识库初始化完成")
    
    def ask_question_with_feedback(self, question: str, use_feedback: bool = True) -> Dict[str, Any]:
        """
        基于知识库回答问题，并考虑用户反馈
        
        Args:
            question: 用户问题
            use_feedback: 是否使用反馈优化答案
            
        Returns:
            包含答案、来源文档、反馈信息的字典
        """
        if not self.qa_chain:
            raise ValueError("QA链未初始化，请先调用load_vector_store()")
        
        logger.info(f"处理问题: {question}")
        
        # 获取原始答案
        original_result = self.qa_chain({"query": question})
        original_answer = original_result["result"]
        source_documents = original_result["source_documents"]
        
        # 准备返回结果
        response = {
            "question": question,
            "original_answer": original_answer,
            "final_answer": original_answer,
            "source_documents": [
                {
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "未知"),
                    "metadata": doc.metadata
                }
                for doc in source_documents
            ],
            "feedback_info": {
                "is_improved": False,
                "confidence_score": 0.0,
                "feedback_count": 0,
                "similar_questions": []
            }
        }
        
        # 如果启用反馈学习，尝试获取优化答案
        if use_feedback and self.enable_feedback_learning:
            try:
                optimized_answer, feedback_meta = self.feedback_system.get_optimized_answer(
                    question, original_answer
                )
                
                if feedback_meta["is_improved"]:
                    response["final_answer"] = optimized_answer
                    response["feedback_info"].update(feedback_meta)
                    logger.info(f"使用优化答案，置信度: {feedback_meta['confidence_score']:.2f}")
                
                # 获取相似问题的反馈
                similar_questions = self.feedback_system.get_similar_questions_feedback(
                    question, self.similarity_threshold
                )
                response["feedback_info"]["similar_questions"] = similar_questions[:3]  # 最多3个
                
            except Exception as e:
                logger.warning(f"获取反馈优化答案失败: {e}")
        
        return response
    
    def collect_user_feedback(self, question: str, original_answer: str, 
                             feedback_type: str, corrected_answer: str = None,
                             feedback_text: str = None, source_documents: List[Dict] = None) -> int:
        """
        收集用户反馈
        
        Args:
            question: 用户问题
            original_answer: 原始答案
            feedback_type: 反馈类型 ('positive', 'negative', 'corrected')
            corrected_answer: 纠正后的答案（仅当feedback_type='corrected'时需要）
            feedback_text: 反馈文本
            source_documents: 来源文档
            
        Returns:
            反馈记录ID
        """
        try:
            feedback_id = self.feedback_system.collect_feedback(
                question=question,
                original_answer=original_answer,
                feedback_type=feedback_type,
                corrected_answer=corrected_answer,
                feedback_text=feedback_text,
                source_documents=source_documents
            )
            
            logger.info(f"收集到用户反馈: {feedback_type}, ID: {feedback_id}")
            return feedback_id
            
        except Exception as e:
            logger.error(f"收集反馈失败: {e}")
            raise
    
    def get_feedback_history(self, question: str) -> List[FeedbackRecord]:
        """
        获取问题的反馈历史
        
        Args:
            question: 用户问题
            
        Returns:
            反馈记录列表
        """
        return self.feedback_system.get_feedback_history(question)
    
    def get_feedback_stats(self) -> Dict[str, Any]:
        """
        获取反馈系统统计信息
        
        Returns:
            统计信息字典
        """
        return self.feedback_system.get_system_stats()
    
    def get_enhanced_stats(self) -> Dict[str, Any]:
        """
        获取增强知识库的完整统计信息
        
        Returns:
            完整统计信息
        """
        # 获取基础知识库统计
        base_stats = self.get_stats()
        
        # 获取反馈系统统计
        feedback_stats = self.get_feedback_stats()
        
        # 合并统计信息
        enhanced_stats = {
            "knowledge_base": base_stats,
            "feedback_system": feedback_stats,
            "system_config": {
                "feedback_learning_enabled": self.enable_feedback_learning,
                "confidence_threshold": self.confidence_threshold,
                "similarity_threshold": self.similarity_threshold,
                "feedback_db_path": self.feedback_db_path
            }
        }
        
        return enhanced_stats
    
    def search_documents(self, query: str, k: int = None) -> List[Dict[str, Any]]:
        """
        搜索文档（重写父类方法以添加反馈信息）
        
        Args:
            query: 搜索查询
            k: 返回结果数量
            
        Returns:
            搜索结果列表
        """
        # 调用父类的搜索方法
        base_results = super().search_documents(query, k)
        
        # 为结果添加评分信息（转换similarity_score为score）
        for result in base_results:
            if 'similarity_score' in result:
                result['score'] = 1.0 - result['similarity_score']  # 转换为相似度评分
        
        return base_results
    
    def search_with_feedback_context(self, query: str, k: int = None) -> List[Dict[str, Any]]:
        """
        搜索文档，并包含反馈上下文信息
        
        Args:
            query: 搜索查询
            k: 返回结果数量
            
        Returns:
            包含反馈信息的搜索结果
        """
        # 获取基础搜索结果
        base_results = self.search_documents(query, k)
        
        # 为每个结果添加反馈上下文
        enhanced_results = []
        for result in base_results:
            enhanced_result = result.copy()
            
            # 检查是否有相关的反馈改进
            try:
                similar_feedback = self.feedback_system.get_similar_questions_feedback(
                    query, self.similarity_threshold
                )
            except:
                similar_feedback = []
            
            enhanced_result["feedback_context"] = {
                "has_similar_feedback": len(similar_feedback) > 0,
                "similar_questions_count": len(similar_feedback),
                "top_similar_question": similar_feedback[0] if similar_feedback else None
            }
            
            enhanced_results.append(enhanced_result)
        
        return enhanced_results
    
    def export_learning_data(self, output_dir: str = "./learning_exports") -> Dict[str, str]:
        """
        导出学习数据用于分析和备份
        
        Args:
            output_dir: 输出目录
            
        Returns:
            导出文件路径字典
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 导出反馈数据
        feedback_file = output_path / f"feedback_data_{timestamp}.json"
        feedback_success = self.feedback_system.export_feedback_data(str(feedback_file))
        
        # 导出知识库统计
        stats_file = output_path / f"kb_stats_{timestamp}.json"
        try:
            import json
            stats = self.get_enhanced_stats()
            with open(stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            stats_success = True
        except Exception as e:
            logger.error(f"导出统计数据失败: {e}")
            stats_success = False
        
        return {
            "feedback_data": str(feedback_file) if feedback_success else None,
            "stats_data": str(stats_file) if stats_success else None,
            "export_timestamp": timestamp
        }
    
    def update_feedback_settings(self, enable_feedback: bool = None, 
                                confidence_threshold: float = None,
                                similarity_threshold: float = None):
        """
        更新反馈学习设置
        
        Args:
            enable_feedback: 是否启用反馈学习
            confidence_threshold: 置信度阈值
            similarity_threshold: 相似度阈值
        """
        if enable_feedback is not None:
            self.enable_feedback_learning = enable_feedback
            logger.info(f"反馈学习已{'启用' if enable_feedback else '禁用'}")
        
        if confidence_threshold is not None:
            if 0.0 <= confidence_threshold <= 1.0:
                self.confidence_threshold = confidence_threshold
                self.feedback_system.confidence_threshold = confidence_threshold
                logger.info(f"置信度阈值更新为: {confidence_threshold}")
            else:
                raise ValueError("置信度阈值必须在0.0-1.0之间")
        
        if similarity_threshold is not None:
            if 0.0 <= similarity_threshold <= 1.0:
                self.similarity_threshold = similarity_threshold
                logger.info(f"相似度阈值更新为: {similarity_threshold}")
            else:
                raise ValueError("相似度阈值必须在0.0-1.0之间")

def main():
    """演示增强知识库使用"""
    try:
        # 获取配置并验证
        config = get_config()
        if not config.validate():
            logger.error("配置验证失败，请检查环境变量设置")
            return
        
        logger.info(f"使用配置: {config}")
        
        # 创建增强知识库实例
        enhanced_kb = EnhancedKnowledgeBase()
        
        # 加载向量存储
        enhanced_kb.load_vector_store()
        
        # 测试问答
        question = "什么是API？"
        print(f"\n问题: {question}")
        
        # 获取答案（包含反馈优化）
        result = enhanced_kb.ask_question_with_feedback(question)
        print(f"原始答案: {result['original_answer'][:100]}...")
        print(f"最终答案: {result['final_answer'][:100]}...")
        print(f"反馈信息: {result['feedback_info']}")
        
        # 模拟收集反馈
        feedback_id = enhanced_kb.collect_user_feedback(
            question=question,
            original_answer=result['original_answer'],
            feedback_type="negative",
            feedback_text="答案不够详细"
        )
        print(f"\n收集反馈ID: {feedback_id}")
        
        # 获取统计信息
        stats = enhanced_kb.get_enhanced_stats()
        print(f"\n增强知识库统计: {stats}")
        
    except Exception as e:
        logger.error(f"增强知识库操作失败: {e}")
        raise

if __name__ == "__main__":
    main()