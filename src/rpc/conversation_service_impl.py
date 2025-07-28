import logging
import uuid
import re
import hashlib
from typing import List, Dict, Any, Optional

from src.db.conversation_manager import ConversationManager
from src.app.knowledge_base import KnowledgeBase
from src.rpc.generated.knowledge_service_pb2 import (
    ConversationChatRequest, ChatResponse, SourceDocument,FeedbackInfo,SimilarQuestion,
    CreateConversationRequest, ConversationResponse,
    ConversationHistoryRequest, ConversationHistoryResponse,
    ListConversationsRequest, ListConversationsResponse,
    UpdateConversationRequest, DeleteConversationRequest, DeleteConversationResponse,
    EmailVerificationRequest, EmailVerificationResponse,
    EmailChatRequest,
    Message as ProtoMessage
)

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ConversationServiceImpl:
    """对话服务实现"""

    def __init__(self, knowledge_base: KnowledgeBase):
        """初始化对话服务

        Args:
            knowledge_base: 知识库实例
        """
        self.kb = knowledge_base
        self.conversation_manager = ConversationManager()
        logger.info("对话服务初始化完成")
        

    def chat_conversation(self, request: ConversationChatRequest) -> ChatResponse:
        """多轮对话聊天

        Args:
            request: 聊天请求

        Returns:
            ChatResponse: 聊天响应
        """
        try:
            # 获取对话上下文
            context = self.conversation_manager.get_conversation_context(
                request.conversation_id, 
                request.max_history_turns
            )
            context_str = ""
            for msg in context:
                prefix = "用户: " if msg['role'] == 'user' else "助手: "
                context_str += f"{prefix}{msg['content']}\n"
            
            # 添加用户问题到对话
            self.conversation_manager.add_message(
                request.conversation_id,
                request.question,
                'user'
            )
            
            # 调用知识库回答问题
            result = self.kb.ask_question_with_feedback(
                question=request.question,
                use_feedback=request.use_feedback
            )
            # 添加助手回复到对话
            self.conversation_manager.add_message(
                request.conversation_id,
                result["final_answer"],
                'assistant',
                [doc["metadata"].get('source', '') for doc in result["source_documents"]]
            )
            
            # 构建响应
            # 转换反馈信息
            feedback_info_data = result.get("feedback_info", {})
            similar_questions = []
            for sq in feedback_info_data.get("similar_questions", []):
                similar_q = SimilarQuestion(
                    question=sq.get("question", ""),
                    similarity_score=sq.get("similarity_score", 0.0),
                    feedback_type=sq.get("feedback_type", "")
                )
                similar_questions.append(similar_q)
            
            response = ChatResponse(
                final_answer=result["final_answer"],
                source_documents=[SourceDocument(source=doc["metadata"].get('source', '')) for doc in result["source_documents"]],
                feedback_info= FeedbackInfo(
                    is_improved=feedback_info_data.get("is_improved", False),
                    confidence_score=feedback_info_data.get("confidence_score", 0.0),
                    feedback_count=feedback_info_data.get("feedback_count", 0),
                    similar_questions=similar_questions
                )
            )
            
            return response
        except Exception as e:
            logger.error(f"多轮对话聊天失败: {e}")
            raise

    def create_conversation(self, request: CreateConversationRequest) -> ConversationResponse:
        """创建对话

        Args:
            request: 创建对话请求

        Returns:
            ConversationResponse: 对话响应
        """
        try:
            # 创建对话
            conversation = self.conversation_manager.create_conversation(
                request.title,
                request.user_id
            )
            
            # 构建响应
            response = ConversationResponse(
                conversation_id=conversation['conversation_id'],
                title=conversation['title'],
                user_id=conversation['user_id'],
                created_at=conversation['created_at'],
                updated_at=conversation['updated_at'],
                is_archived=conversation['is_archived']
            )
            
            return response
        except Exception as e:
            logger.error(f"创建对话失败: {e}")
            raise

    def get_conversation_history(self, request: ConversationHistoryRequest) -> ConversationHistoryResponse:
        """获取对话历史

        Args:
            request: 对话历史请求

        Returns:
            ConversationHistoryResponse: 对话历史响应
        """
        try:
            # 获取对话历史
            conversation, messages, total_count = self.conversation_manager.get_conversation_history(
                request.conversation_id,
                request.limit,
                request.offset
            )
            
            # 构建消息列表
            proto_messages = []
            for msg in messages:
                proto_msg = ProtoMessage(
                    message_id=msg['message_id'],
                    conversation_id=msg['conversation_id'],
                    content=msg['content'],
                    role=msg['role'],
                    created_at=msg['created_at']
                )
                proto_msg.source_documents.extend(msg['source_documents'])
                proto_messages.append(proto_msg)
            
            # 构建响应
            response = ConversationHistoryResponse(
                conversation_id=conversation['conversation_id'],
                title=conversation['title'],
                total_count=total_count
            )
            response.messages.extend(proto_messages)
            
            return response
        except Exception as e:
            logger.error(f"获取对话历史失败: {e}")
            raise

    def list_conversations(self, request: ListConversationsRequest) -> ListConversationsResponse:
        """列出对话

        Args:
            request: 列出对话请求

        Returns:
            ListConversationsResponse: 列出对话响应
        """
        try:
            # 列出对话
            conversations, total_count = self.conversation_manager.list_conversations(
                request.user_id,
                request.limit,
                request.offset,
                request.include_archived
            )
            
            # 构建对话列表
            proto_conversations = []
            for conv in conversations:
                proto_conv = ConversationResponse(
                    conversation_id=conv['conversation_id'],
                    title=conv['title'],
                    user_id=conv['user_id'],
                    created_at=conv['created_at'],
                    updated_at=conv['updated_at'],
                    is_archived=conv['is_archived']
                )
                proto_conversations.append(proto_conv)
            
            # 构建响应
            response = ListConversationsResponse(
                total_count=total_count
            )
            response.conversations.extend(proto_conversations)
            
            return response
        except Exception as e:
            logger.error(f"列出对话失败: {e}")
            raise

    def update_conversation(self, request: UpdateConversationRequest) -> ConversationResponse:
        """更新对话

        Args:
            request: 更新对话请求

        Returns:
            ConversationResponse: 对话响应
        """
        try:
            # 更新对话
            conversation = self.conversation_manager.update_conversation(
                request.conversation_id,
                request.title,
                request.is_archived
            )
            
            # 构建响应
            response = ConversationResponse(
                conversation_id=conversation['conversation_id'],
                title=conversation['title'],
                user_id=conversation['user_id'],
                created_at=conversation['created_at'],
                updated_at=conversation['updated_at'],
                is_archived=conversation['is_archived']
            )
            
            return response
        except Exception as e:
            logger.error(f"更新对话失败: {e}")
            raise

    def delete_conversation(self, request: DeleteConversationRequest) -> DeleteConversationResponse:
        """删除对话

        Args:
            request: 删除对话请求

        Returns:
            DeleteConversationResponse: 删除对话响应
        """
        try:
            # 删除对话
            success = self.conversation_manager.delete_conversation(request.conversation_id)
            
            # 构建响应
            response = DeleteConversationResponse(
                success=success
            )
            
            return response
        except Exception as e:
            logger.error(f"删除对话失败: {e}")
            raise

    def verify_email(self, request: EmailVerificationRequest) -> EmailVerificationResponse:
        """验证邮箱

        Args:
            request: 邮箱验证请求

        Returns:
            EmailVerificationResponse: 邮箱验证响应
        """
        try:
            email = request.email.strip().lower()
            
            # 验证邮箱格式
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            is_valid = bool(re.match(email_pattern, email))
            
            if not is_valid:
                return EmailVerificationResponse(
                    is_valid=False,
                    user_id="",
                    success=False,
                    error_message="邮箱格式无效"
                )
            
            # 基于邮箱生成用户ID
            user_id = hashlib.md5(email.encode('utf-8')).hexdigest()[:16]
            
            return EmailVerificationResponse(
                is_valid=True,
                user_id=user_id,
                success=True,
                error_message=""
            )
        except Exception as e:
            logger.error(f"邮箱验证失败: {e}")
            return EmailVerificationResponse(
                is_valid=False,
                user_id="",
                success=False,
                error_message=f"邮箱验证失败: {str(e)}"
            )

    def chat_with_email_verification(self, request: EmailChatRequest) -> ChatResponse:
        """带邮箱验证的对话聊天

        Args:
            request: 带邮箱验证的聊天请求

        Returns:
            ChatResponse: 聊天响应
        """
        try:
            # 验证邮箱
            email_verification = EmailVerificationRequest(email=request.email)
            email_response = self.verify_email(email_verification)
            
            if not email_response.success or not email_response.is_valid:
                return ChatResponse(
                    question=request.question,
                    original_answer="",
                    final_answer="",
                    source_documents=[],
                    feedback_info={},
                    success=False,
                    error_message=email_response.error_message or "邮箱验证失败"
                )
            
            user_id = email_response.user_id
            conversation_id = request.conversation_id
            
            # 如果没有提供对话ID，创建新对话
            if not conversation_id:
                title = request.conversation_title if request.conversation_title else f"对话 - {request.email}"
                create_request = CreateConversationRequest(
                    title=title,
                    user_id=user_id
                )
                conversation_response = self.create_conversation(create_request)
                conversation_id = conversation_response.conversation_id
            
            # 验证对话是否属于该用户
            try:
                conversation, _, _ = self.conversation_manager.get_conversation_history(conversation_id, 1, 0)
                if conversation['user_id'] != user_id:
                    return ChatResponse(
                        question=request.question,
                        original_answer="",
                        final_answer="",
                        source_documents=[],
                        feedback_info={},
                        success=False,
                        error_message="无权访问该对话"
                    )
            except ValueError:
                return ChatResponse(
                    question=request.question,
                    original_answer="",
                    final_answer="",
                    source_documents=[],
                    feedback_info={},
                    success=False,
                    error_message="对话不存在"
                )
            
            # 构建对话聊天请求
            chat_request = ConversationChatRequest(
                question=request.question,
                conversation_id=conversation_id,
                use_feedback=request.use_feedback,
                use_reranking=request.use_reranking,
                top_k=request.top_k,
                similarity_threshold=request.similarity_threshold,
                max_history_turns=request.max_history_turns
            )
            
            # 如果有系统配置，添加到请求中
            if request.HasField("system_config"):
                chat_request.system_config.CopyFrom(request.system_config)
            
            # 执行对话聊天
            response = self.chat_conversation(chat_request)
            return response
            
        except Exception as e:
            logger.error(f"带邮箱验证的对话聊天失败: {e}")
            return ChatResponse(
                question=request.question,
                original_answer="",
                final_answer="",
                source_documents=[],
                feedback_info={},
                success=False,
                error_message=f"聊天失败: {str(e)}"
            )

    def _convert_system_config(self, proto_config) -> Dict[str, Any]:
        """转换系统配置

        Args:
            proto_config: 协议系统配置

        Returns:
            Dict: 系统配置字典
        """
        return {
            'model': proto_config.model,
            'temperature': proto_config.temperature,
            'top_p': proto_config.top_p,
            'max_tokens': proto_config.max_tokens
        }