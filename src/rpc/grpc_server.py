#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gRPC服务器实现
提供知识库的RPC接口服务
"""

import os
import sys
import logging
import json
import uuid
from concurrent import futures
from pathlib import Path
from typing import Dict, Any, List

import grpc

# 添加项目路径
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# 导入生成的gRPC代码
try:
    from generated import knowledge_service_pb2
    from generated import knowledge_service_pb2_grpc
except ImportError:
    # 如果在src目录下运行，尝试从上级目录导入
    sys.path.insert(0, str(project_root))
    from src.rpc.generated import knowledge_service_pb2
    from src.rpc.generated import knowledge_service_pb2_grpc

# 导入业务逻辑模块
try:
    from enhanced_knowledge_base import EnhancedKnowledgeBase
    from feedback_system import FeedbackRecord
    from conversation_service_impl import ConversationServiceImpl
except ImportError:
    from src.app.enhanced_knowledge_base import EnhancedKnowledgeBase
    from src.app.feedback_system import FeedbackRecord
    from src.rpc.conversation_service_impl import ConversationServiceImpl

try:
    from config.config import get_config
except ImportError:
    sys.path.insert(0, str(project_root))
    from config.config import get_config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('kdb')

class KnowledgeServiceImpl(knowledge_service_pb2_grpc.KnowledgeServiceServicer):
    """知识库服务实现"""
    
    def __init__(self, knowledge_base=None):
        """初始化服务"""
        self.kb = knowledge_base
        self.config = None
        self.version = "1.0.0"
        self.conversation_service = None
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """初始化知识库"""
        try:
            # 加载配置
            self.config = get_config()
            
            # 初始化增强知识库
            self.kb = EnhancedKnowledgeBase()
            
            # 加载向量存储
            vector_store_path = Path(self.config.vector_store.store_path)
            if vector_store_path.exists():
                self.kb.load_vector_store()
                logger.info("知识库加载成功")
            else:
                logger.warning(f"向量存储不存在: {vector_store_path}")
                
        except Exception as e:
            logger.error(f"初始化知识库失败: {e}")
            raise
    
    def Chat(self, request, context):
        """聊天接口"""
        try:
            logger.info(f"收到聊天请求: {request.question}")
            
            if not self.kb or not self.kb.qa_chain:
                return knowledge_service_pb2.ChatResponse(
                    success=False,
                    error_message="知识库未初始化或向量存储不存在"
                )
            
            # 调用增强知识库进行问答
            result = self.kb.ask_question_with_feedback(
                question=request.question,
                use_feedback=request.use_feedback
            )
            
            # 转换来源文档
            source_documents = []
            for doc in result.get("source_documents", []):
                source_doc = knowledge_service_pb2.SourceDocument(
                    content=doc["content"],
                    source=doc["source"],
                    metadata=doc["metadata"]
                )
                source_documents.append(source_doc)
            
            # 转换反馈信息
            feedback_info_data = result.get("feedback_info", {})
            similar_questions = []
            for sq in feedback_info_data.get("similar_questions", []):
                similar_q = knowledge_service_pb2.SimilarQuestion(
                    question=sq.get("question", ""),
                    similarity_score=sq.get("similarity_score", 0.0),
                    feedback_type=sq.get("feedback_type", "")
                )
                similar_questions.append(similar_q)
            
            feedback_info = knowledge_service_pb2.FeedbackInfo(
                is_improved=feedback_info_data.get("is_improved", False),
                confidence_score=feedback_info_data.get("confidence_score", 0.0),
                feedback_count=feedback_info_data.get("feedback_count", 0),
                similar_questions=similar_questions
            )
            
            # 构建响应
            response = knowledge_service_pb2.ChatResponse(
                question=result["question"],
                original_answer=result["original_answer"],
                final_answer=result["final_answer"],
                source_documents=source_documents,
                feedback_info=feedback_info,
                success=True
            )
            
            logger.info(f"聊天请求处理成功: {request.question[:50]}...")
            return response
            
        except Exception as e:
            logger.error(f"聊天请求处理失败: {e}")
            return knowledge_service_pb2.ChatResponse(
                success=False,
                error_message=str(e)
            )
    
    def SubmitFeedback(self, request, context):
        """提交反馈"""
        try:
            logger.info(f"收到反馈: {request.feedback_type} for question: {request.question[:50]}...")
            
            if not self.kb:
                return knowledge_service_pb2.FeedbackResponse(
                    success=False,
                    error_message="知识库未初始化"
                )
            
            # 转换来源文档
            source_documents = []
            for doc in request.source_documents:
                source_documents.append({
                    "content": doc.content,
                    "source": doc.source,
                    "metadata": dict(doc.metadata)
                })
            
            # 收集反馈
            feedback_id = self.kb.collect_user_feedback(
                question=request.question,
                original_answer=request.original_answer,
                feedback_type=request.feedback_type,
                corrected_answer=request.corrected_answer if request.corrected_answer else None,
                feedback_text=request.feedback_text if request.feedback_text else None,
                source_documents=source_documents
            )
            
            response = knowledge_service_pb2.FeedbackResponse(
                feedback_id=feedback_id,
                success=True
            )
            
            logger.info(f"反馈提交成功: ID={feedback_id}")
            return response
            
        except Exception as e:
            logger.error(f"反馈提交失败: {e}")
            return knowledge_service_pb2.FeedbackResponse(
                success=False,
                error_message=str(e)
            )
    
    def GetFeedbackHistory(self, request, context):
        """获取反馈历史"""
        try:
            logger.info(f"获取反馈历史: {request.question[:50]}...")
            
            if not self.kb:
                return knowledge_service_pb2.FeedbackHistoryResponse(
                    success=False,
                    error_message="知识库未初始化"
                )
            
            # 获取反馈历史
            history = self.kb.get_feedback_history(request.question)
            
            # 转换反馈记录
            records = []
            for record in history:
                # 解析来源文档
                source_docs = []
                if record.source_documents:
                    try:
                        docs_data = json.loads(record.source_documents)
                        for doc_data in docs_data:
                            source_doc = knowledge_service_pb2.SourceDocument(
                                content=doc_data.get("content", ""),
                                source=doc_data.get("source", ""),
                                metadata=doc_data.get("metadata", {})
                            )
                            source_docs.append(source_doc)
                    except:
                        pass
                
                pb_record = knowledge_service_pb2.FeedbackRecord(
                    id=record.id or 0,
                    question=record.question,
                    original_answer=record.original_answer,
                    user_feedback=record.user_feedback,
                    corrected_answer=record.corrected_answer or "",
                    feedback_text=record.feedback_text or "",
                    timestamp=record.timestamp or "",
                    question_hash=record.question_hash or "",
                    source_documents=source_docs
                )
                records.append(pb_record)
            
            response = knowledge_service_pb2.FeedbackHistoryResponse(
                records=records,
                success=True
            )
            
            logger.info(f"反馈历史获取成功: {len(records)} 条记录")
            return response
            
        except Exception as e:
            logger.error(f"获取反馈历史失败: {e}")
            return knowledge_service_pb2.FeedbackHistoryResponse(
                success=False,
                error_message=str(e)
            )
    
    def GetStats(self, request, context):
        """获取统计信息"""
        try:
            logger.info("获取系统统计信息")
            
            if not self.kb:
                return knowledge_service_pb2.StatsResponse(
                    success=False,
                    error_message="知识库未初始化"
                )
            
            # 获取增强统计信息
            stats = self.kb.get_enhanced_stats()
            
            # 转换知识库统计
            kb_stats_data = stats.get("knowledge_base", {})
            kb_stats = knowledge_service_pb2.KnowledgeBaseStats(
                total_documents=kb_stats_data.get("total_documents", 0),
                total_chunks=kb_stats_data.get("total_chunks", 0),
                vector_store_path=kb_stats_data.get("vector_store_path", "")
            )
            
            # 转换反馈统计
            feedback_stats_data = stats.get("feedback_system", {})
            feedback_stats = knowledge_service_pb2.FeedbackStats(
                total_feedback=feedback_stats_data.get("total_feedback", 0),
                positive_feedback=feedback_stats_data.get("positive_feedback", 0),
                negative_feedback=feedback_stats_data.get("negative_feedback", 0),
                corrected_feedback=feedback_stats_data.get("corrected_feedback", 0),
                improved_answers=feedback_stats_data.get("improved_answers", 0),
                satisfaction_rate=feedback_stats_data.get("satisfaction_rate", 0.0)
            )
            
            # 转换系统配置
            config_data = stats.get("system_config", {})
            system_config = knowledge_service_pb2.SystemConfig(
                feedback_learning_enabled=config_data.get("feedback_learning_enabled", False),
                confidence_threshold=config_data.get("confidence_threshold", 0.0),
                similarity_threshold=config_data.get("similarity_threshold", 0.0),
                feedback_db_path=config_data.get("feedback_db_path", "")
            )
            
            response = knowledge_service_pb2.StatsResponse(
                knowledge_base=kb_stats,
                feedback_system=feedback_stats,
                system_config=system_config,
                success=True
            )
            
            logger.info("统计信息获取成功")
            return response
            
        except Exception as e:
            logger.error(f"获取统计信息失败: {e}")
            return knowledge_service_pb2.StatsResponse(
                success=False,
                error_message=str(e)
            )
    
    def SearchDocuments(self, request, context):
        """搜索文档"""
        try:
            logger.info(f"搜索文档: {request.query}")
            
            if not self.kb or not self.kb.vector_store:
                return knowledge_service_pb2.SearchResponse(
                    success=False,
                    error_message="知识库未初始化或向量存储不存在"
                )
            
            # 执行搜索
            k = request.k if request.k > 0 else 5
            search_results = self.kb.search_documents(request.query, k=k)
            
            # 转换搜索结果
            results = []
            for result in search_results:
                search_result = knowledge_service_pb2.SearchResult(
                    content=result.get("content", ""),
                    score=result.get("score", 0.0),
                    metadata=result.get("metadata", {})
                )
                results.append(search_result)
            
            response = knowledge_service_pb2.SearchResponse(
                results=results,
                success=True
            )
            
            logger.info(f"搜索完成: 返回 {len(results)} 个结果")
            return response
            
        except Exception as e:
            logger.error(f"搜索文档失败: {e}")
            return knowledge_service_pb2.SearchResponse(
                success=False,
                error_message=str(e)
            )
    
    def HealthCheck(self, request, context):
        """健康检查"""
        try:
            # 检查知识库状态
            healthy = self.kb is not None
            status = "healthy" if healthy else "unhealthy"
            
            if healthy and self.kb.qa_chain:
                status = "ready"
            elif healthy:
                status = "initializing"
            
            response = knowledge_service_pb2.HealthCheckResponse(
                healthy=healthy,
                status=status,
                version=self.version
            )
            
            return response
            
        except Exception as e:
            logger.error(f"健康检查失败: {e}")
            return knowledge_service_pb2.HealthCheckResponse(
                healthy=False,
                status="error",
                version=self.version
            )
            
    # 多轮对话相关接口
    def ChatConversation(self, request, context):
        """多轮对话聊天接口"""
        return self.conversation_service.chat_conversation(request, context)
        
    def CreateConversation(self, request, context):
        """创建对话接口"""
        return self.conversation_service.create_conversation(request, context)
        
    def GetConversationHistory(self, request, context):
        """获取对话历史接口"""
        return self.conversation_service.get_conversation_history(request, context)
        
    def ListConversations(self, request, context):
        """列出对话接口"""
        return self.conversation_service.list_conversations(request, context)
        
    def UpdateConversation(self, request, context):
        """更新对话接口"""
        return self.conversation_service.update_conversation(request, context)
        
    def DeleteConversation(self, request, context):
        """删除对话接口"""
        return self.conversation_service.delete_conversation(request, context)
        
    def VerifyEmail(self, request, context):
        """验证邮箱接口"""
        return self.conversation_service.verify_email(request)
        
    def ChatWithEmailVerification(self, request, context):
        """带邮箱验证的对话聊天接口"""
        return self.conversation_service.chat_with_email_verification(request)

def serve(port=50051, max_workers=10):
    """启动gRPC服务器"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    
    # 初始化知识库
    kb = EnhancedKnowledgeBase()
    
    # 注册知识库服务
    knowledge_service = KnowledgeServiceImpl(kb)
    # 初始化对话服务
    knowledge_service.conversation_service = ConversationServiceImpl(kb)
    knowledge_service_pb2_grpc.add_KnowledgeServiceServicer_to_server(
        knowledge_service, server
    )
    
    # 监听端口
    listen_addr = f'[::]:{port}'
    server.add_insecure_port(listen_addr)
    
    # 启动服务器
    server.start()
    logger.info(f"🚀 gRPC服务器启动成功")
    logger.info(f"📡 监听地址: {listen_addr}")
    logger.info(f"🔧 最大工作线程: {max_workers}")
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        logger.info("👋 服务器停止")
        server.stop(0)

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='知识库gRPC服务器')
    parser.add_argument('--port', type=int, default=50051, help='服务端口')
    parser.add_argument('--workers', type=int, default=10, help='最大工作线程数')
    
    args = parser.parse_args()
    
    serve(port=args.port, max_workers=args.workers)