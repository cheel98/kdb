import os
import uuid
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any

import pymysql
from sqlalchemy import create_engine, Column, String, Text, Boolean, DateTime, ForeignKey, Enum, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import TEXT

from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 数据库配置
DB_HOST = os.getenv('MYSQL_HOST', 'localhost')
DB_PORT = int(os.getenv('MYSQL_PORT', '3306'))
DB_USER = os.getenv('MYSQL_USER', 'root')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
DB_NAME = os.getenv('MYSQL_DATABASE', 'zlatticedoc')
DB_CHARSET = os.getenv('MYSQL_CHARSET', 'utf8mb4')

# 对话配置
MAX_HISTORY_TURNS = int(os.getenv('CONVERSATION_MAX_HISTORY_TURNS', '10'))
EXPIRE_DAYS = int(os.getenv('CONVERSATION_EXPIRE_DAYS', '30'))

# 创建数据库连接
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset={DB_CHARSET}"

# 创建SQLAlchemy基类
Base = declarative_base()


class Conversation(Base):
    """对话模型"""
    __tablename__ = 'conversations'

    conversation_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    user_id = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    is_archived = Column(Boolean, default=False, index=True)

    # 关系
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'conversation_id': self.conversation_id,
            'title': self.title,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_archived': self.is_archived
        }


class Message(Base):
    """消息模型"""
    __tablename__ = 'messages'

    message_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String(36), ForeignKey('conversations.conversation_id', ondelete='CASCADE'), nullable=False, index=True)
    content = Column(TEXT, nullable=False)
    role = Column(Enum('user', 'assistant'), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # 关系
    conversation = relationship("Conversation", back_populates="messages")
    sources = relationship("MessageSource", back_populates="message", cascade="all, delete-orphan")

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'message_id': self.message_id,
            'conversation_id': self.conversation_id,
            'content': self.content,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'source_documents': [source.source_document for source in self.sources]
        }


class MessageSource(Base):
    """消息源文档模型"""
    __tablename__ = 'message_sources'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    message_id = Column(String(36), ForeignKey('messages.message_id', ondelete='CASCADE'), nullable=False, index=True)
    source_document = Column(String(255), nullable=False)

    # 关系
    message = relationship("Message", back_populates="sources")


class ConversationManager:
    """对话管理器"""

    def __init__(self):
        """初始化对话管理器"""
        try:
            self.engine = create_engine(DATABASE_URL)
            self.Session = sessionmaker(bind=self.engine)
            # 创建表
            Base.metadata.create_all(self.engine)
            logger.info("数据库连接成功")
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise

    def create_conversation(self, title: str, user_id: str) -> Dict[str, Any]:
        """创建新对话

        Args:
            title: 对话标题
            user_id: 用户ID

        Returns:
            Dict: 对话信息
        """
        session = self.Session()
        try:
            conversation = Conversation(title=title, user_id=user_id)
            session.add(conversation)
            session.commit()
            return conversation.to_dict()
        except Exception as e:
            session.rollback()
            logger.error(f"创建对话失败: {e}")
            raise
        finally:
            session.close()

    def add_message(self, conversation_id: str, content: str, role: str, source_documents: Optional[List[str]] = None) -> Dict[str, Any]:
        """添加消息

        Args:
            conversation_id: 对话ID
            content: 消息内容
            role: 角色 (user/assistant)
            source_documents: 源文档列表

        Returns:
            Dict: 消息信息
        """
        session = self.Session()
        try:
            # 检查对话是否存在
            conversation = session.query(Conversation).filter_by(conversation_id=conversation_id).first()
            if not conversation:
                raise ValueError(f"对话不存在: {conversation_id}")

            # 创建消息
            message = Message(conversation_id=conversation_id, content=content, role=role)
            session.add(message)

            # 添加源文档
            if source_documents:
                for doc in source_documents:
                    source = MessageSource(message_id=message.message_id, source_document=doc)
                    session.add(source)

            # 更新对话的更新时间
            conversation.updated_at = datetime.utcnow()
            session.commit()

            return message.to_dict()
        except Exception as e:
            session.rollback()
            logger.error(f"添加消息失败: {e}")
            raise
        finally:
            session.close()

    def get_conversation_history(self, conversation_id: str, limit: int = 100, offset: int = 0) -> Tuple[Dict[str, Any], List[Dict[str, Any]], int]:
        """获取对话历史

        Args:
            conversation_id: 对话ID
            limit: 限制数量
            offset: 偏移量

        Returns:
            Tuple: (对话信息, 消息列表, 总消息数)
        """
        session = self.Session()
        try:
            # 获取对话
            conversation = session.query(Conversation).filter_by(conversation_id=conversation_id).first()
            if not conversation:
                raise ValueError(f"对话不存在: {conversation_id}")

            # 获取消息总数
            total_count = session.query(func.count(Message.message_id)).filter_by(conversation_id=conversation_id).scalar()

            # 获取消息列表
            messages = session.query(Message).filter_by(conversation_id=conversation_id).order_by(Message.created_at).offset(offset).limit(limit).all()

            # 转换为字典
            conversation_dict = conversation.to_dict()
            messages_dict = [message.to_dict() for message in messages]

            return conversation_dict, messages_dict, total_count
        except Exception as e:
            logger.error(f"获取对话历史失败: {e}")
            raise
        finally:
            session.close()

    def get_conversation_context(self, conversation_id: str, max_turns: int = MAX_HISTORY_TURNS) -> List[Dict[str, Any]]:
        """获取对话上下文

        Args:
            conversation_id: 对话ID
            max_turns: 最大轮次

        Returns:
            List: 消息列表
        """
        session = self.Session()
        try:
            # 获取最近的消息
            messages = session.query(Message).filter_by(conversation_id=conversation_id).order_by(Message.created_at.desc()).limit(max_turns * 2).all()
            messages.reverse()  # 按时间正序排列

            # 转换为字典
            return [message.to_dict() for message in messages]
        except Exception as e:
            logger.error(f"获取对话上下文失败: {e}")
            raise
        finally:
            session.close()

    def list_conversations(self, user_id: str, limit: int = 20, offset: int = 0, include_archived: bool = False) -> Tuple[List[Dict[str, Any]], int]:
        """列出对话

        Args:
            user_id: 用户ID
            limit: 限制数量
            offset: 偏移量
            include_archived: 是否包含已归档

        Returns:
            Tuple: (对话列表, 总对话数)
        """
        session = self.Session()
        try:
            # 构建查询
            query = session.query(Conversation).filter_by(user_id=user_id)
            if not include_archived:
                query = query.filter_by(is_archived=False)

            # 获取总数
            total_count = query.count()

            # 获取对话列表
            conversations = query.order_by(Conversation.updated_at.desc()).offset(offset).limit(limit).all()

            # 转换为字典
            return [conversation.to_dict() for conversation in conversations], total_count
        except Exception as e:
            logger.error(f"列出对话失败: {e}")
            raise
        finally:
            session.close()

    def update_conversation(self, conversation_id: str, title: Optional[str] = None, is_archived: Optional[bool] = None) -> Dict[str, Any]:
        """更新对话

        Args:
            conversation_id: 对话ID
            title: 对话标题
            is_archived: 是否归档

        Returns:
            Dict: 对话信息
        """
        session = self.Session()
        try:
            # 获取对话
            conversation = session.query(Conversation).filter_by(conversation_id=conversation_id).first()
            if not conversation:
                raise ValueError(f"对话不存在: {conversation_id}")

            # 更新字段
            if title is not None:
                conversation.title = title
            if is_archived is not None:
                conversation.is_archived = is_archived

            # 更新时间
            conversation.updated_at = datetime.utcnow()

            session.commit()
            return conversation.to_dict()
        except Exception as e:
            session.rollback()
            logger.error(f"更新对话失败: {e}")
            raise
        finally:
            session.close()

    def delete_conversation(self, conversation_id: str) -> bool:
        """删除对话

        Args:
            conversation_id: 对话ID

        Returns:
            bool: 是否成功
        """
        session = self.Session()
        try:
            # 获取对话
            conversation = session.query(Conversation).filter_by(conversation_id=conversation_id).first()
            if not conversation:
                raise ValueError(f"对话不存在: {conversation_id}")

            # 删除对话
            session.delete(conversation)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"删除对话失败: {e}")
            raise
        finally:
            session.close()

    def archive_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """归档对话

        Args:
            conversation_id: 对话ID

        Returns:
            Dict: 对话信息
        """
        return self.update_conversation(conversation_id, is_archived=True)

    def unarchive_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """取消归档对话

        Args:
            conversation_id: 对话ID

        Returns:
            Dict: 对话信息
        """
        return self.update_conversation(conversation_id, is_archived=False)

    def cleanup_expired_conversations(self, days: int = EXPIRE_DAYS) -> int:
        """清理过期对话

        Args:
            days: 过期天数

        Returns:
            int: 删除的对话数
        """
        session = self.Session()
        try:
            # 计算过期时间
            expire_date = datetime.utcnow() - timedelta(days=days)

            # 查询过期对话
            expired_conversations = session.query(Conversation).filter(Conversation.updated_at < expire_date).all()

            # 删除过期对话
            count = 0
            for conversation in expired_conversations:
                session.delete(conversation)
                count += 1

            session.commit()
            return count
        except Exception as e:
            session.rollback()
            logger.error(f"清理过期对话失败: {e}")
            raise
        finally:
            session.close()

    def get_conversation_stats(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """获取对话统计信息

        Args:
            user_id: 用户ID

        Returns:
            Dict: 统计信息
        """
        session = self.Session()
        try:
            # 构建查询
            query = session.query(Conversation)
            if user_id:
                query = query.filter_by(user_id=user_id)

            # 总对话数
            total_conversations = query.count()

            # 活跃对话数
            active_conversations = query.filter_by(is_archived=False).count()

            # 归档对话数
            archived_conversations = query.filter_by(is_archived=True).count()

            # 总消息数
            query_messages = session.query(Message)
            if user_id:
                query_messages = query_messages.join(Conversation).filter(Conversation.user_id == user_id)
            total_messages = query_messages.count()

            # 用户消息数
            user_messages = query_messages.filter_by(role='user').count()

            # 助手消息数
            assistant_messages = query_messages.filter_by(role='assistant').count()

            return {
                'total_conversations': total_conversations,
                'active_conversations': active_conversations,
                'archived_conversations': archived_conversations,
                'total_messages': total_messages,
                'user_messages': user_messages,
                'assistant_messages': assistant_messages
            }
        except Exception as e:
            logger.error(f"获取对话统计信息失败: {e}")
            raise
        finally:
            session.close()