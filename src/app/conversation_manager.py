#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话管理系统
实现多轮对话的存储、检索和管理
"""

import os
import sys
import logging
import json
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

import sqlalchemy as sa
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.pool import QueuePool

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from config.config import get_config

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 创建SQLAlchemy基类
Base = declarative_base()


class Conversation(Base):
    """对话模型"""
    __tablename__ = 'conversations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String(36), unique=True, nullable=False, index=True)
    user_id = Column(String(36), nullable=True, index=True)  # 可选的用户标识
    title = Column(String(255), nullable=True)  # 对话标题
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)  # 是否活跃
    metadata = Column(Text, nullable=True)  # 存储JSON格式的元数据

    # 关系：一个对话有多个消息
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Conversation(id={self.id}, conversation_id='{self.conversation_id}')>"


class Message(Base):
    """消息模型"""
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False, index=True)
    message_id = Column(String(36), unique=True, nullable=False)
    role = Column(String(20), nullable=False)  # user, assistant, system
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(Text, nullable=True)  # 存储JSON格式的元数据，如源文档信息

    # 关系：多个消息属于一个对话
    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self):
        return f"<Message(id={self.id}, role='{self.role}')>"


class ConversationManager:
    """对话管理器"""

    def __init__(self):
        """初始化对话管理器"""
        self.config = get_config()
        self.db_url = self._get_db_url()
        self.engine = create_engine(
            self.db_url,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=3600,
            echo=False
        )
        self.Session = sessionmaker(bind=self.engine)
        self.max_turns = int(os.getenv('CONVERSATION_MAX_TURNS', '10'))
        self.expiry_days = int(os.getenv('CONVERSATION_EXPIRY_DAYS', '30'))
        
        # 确保数据库表存在
        self._create_tables()
        
        logger.info("对话管理器初始化完成")

    def _get_db_url(self) -> str:
        """获取数据库连接URL"""
        host = os.getenv('MYSQL_HOST', 'localhost')
        port = os.getenv('MYSQL_PORT', '3306')
        user = os.getenv('MYSQL_USER', 'root')
        password = os.getenv('MYSQL_PASSWORD', '')
        database = os.getenv('MYSQL_DATABASE', 'zlattice_knowledge')
        charset = os.getenv('MYSQL_CHARSET', 'utf8mb4')
        
        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}"

    def _create_tables(self):
        """创建数据库表"""
        Base.metadata.create_all(self.engine)

    def create_conversation(self, user_id: str = None, title: str = None, metadata: Dict = None) -> str:
        """创建新对话
        
        Args:
            user_id: 用户ID（可选）
            title: 对话标题（可选）
            metadata: 元数据（可选）
            
        Returns:
            conversation_id: 对话ID
        """
        conversation_id = str(uuid.uuid4())
        
        with self.Session() as session:
            conversation = Conversation(
                conversation_id=conversation_id,
                user_id=user_id,
                title=title,
                metadata=json.dumps(metadata) if metadata else None
            )
            session.add(conversation)
            session.commit()
            
            logger.info(f"创建新对话: {conversation_id}")
            return conversation_id

    def add_message(self, conversation_id: str, role: str, content: str, metadata: Dict = None) -> str:
        """添加消息到对话
        
        Args:
            conversation_id: 对话ID
            role: 角色（user, assistant, system）
            content: 消息内容
            metadata: 元数据（可选）
            
        Returns:
            message_id: 消息ID
        """
        message_id = str(uuid.uuid4())
        
        with self.Session() as session:
            # 查找对话
            conversation = session.query(Conversation).filter_by(conversation_id=conversation_id).first()
            if not conversation:
                raise ValueError(f"对话不存在: {conversation_id}")
            
            # 添加消息
            message = Message(
                conversation_id=conversation.id,
                message_id=message_id,
                role=role,
                content=content,
                metadata=json.dumps(metadata) if metadata else None
            )
            session.add(message)
            
            # 更新对话的更新时间
            conversation.updated_at = datetime.utcnow()
            
            session.commit()
            
            logger.info(f"添加消息到对话 {conversation_id}: {role}")
            return message_id

    def get_conversation_history(self, conversation_id: str, limit: int = None) -> List[Dict[str, Any]]:
        """获取对话历史
        
        Args:
            conversation_id: 对话ID
            limit: 限制返回的消息数量（可选）
            
        Returns:
            messages: 消息列表
        """
        with self.Session() as session:
            # 查找对话
            conversation = session.query(Conversation).filter_by(conversation_id=conversation_id).first()
            if not conversation:
                raise ValueError(f"对话不存在: {conversation_id}")
            
            # 查询消息，按创建时间排序
            query = session.query(Message).filter_by(conversation_id=conversation.id).order_by(Message.created_at)
            
            # 如果指定了限制，则只返回最近的n条消息
            if limit:
                query = query.limit(limit)
            
            messages = []
            for msg in query.all():
                message_data = {
                    "message_id": msg.message_id,
                    "role": msg.role,
                    "content": msg.content,
                    "created_at": msg.created_at.isoformat(),
                    "metadata": json.loads(msg.metadata) if msg.metadata else None
                }
                messages.append(message_data)
            
            return messages

    def get_conversation_context(self, conversation_id: str, max_turns: int = None) -> List[Dict[str, Any]]:
        """获取对话上下文（用于多轮对话）
        
        Args:
            conversation_id: 对话ID
            max_turns: 最大轮次（可选，默认使用配置值）
            
        Returns:
            context: 上下文消息列表
        """
        max_turns = max_turns or self.max_turns
        
        # 计算需要的消息数量（每轮包含用户和助手的消息）
        limit = max_turns * 2
        
        with self.Session() as session:
            # 查找对话
            conversation = session.query(Conversation).filter_by(conversation_id=conversation_id).first()
            if not conversation:
                raise ValueError(f"对话不存在: {conversation_id}")
            
            # 查询最近的消息，按创建时间倒序
            messages = session.query(Message)\
                .filter_by(conversation_id=conversation.id)\
                .order_by(Message.created_at.desc())\
                .limit(limit)\
                .all()
            
            # 将消息按正确的顺序排列
            messages.reverse()
            
            context = []
            for msg in messages:
                message_data = {
                    "role": msg.role,
                    "content": msg.content
                }
                context.append(message_data)
            
            return context

    def list_conversations(self, user_id: str = None, active_only: bool = True, 
                          limit: int = 10, offset: int = 0) -> List[Dict[str, Any]]:
        """列出对话
        
        Args:
            user_id: 用户ID（可选）
            active_only: 是否只返回活跃对话
            limit: 限制返回的对话数量
            offset: 分页偏移量
            
        Returns:
            conversations: 对话列表
        """
        with self.Session() as session:
            query = session.query(Conversation)
            
            # 如果指定了用户ID，则只返回该用户的对话
            if user_id:
                query = query.filter_by(user_id=user_id)
            
            # 如果只返回活跃对话
            if active_only:
                query = query.filter_by(is_active=True)
            
            # 按更新时间倒序排序，并应用分页
            query = query.order_by(Conversation.updated_at.desc()).offset(offset).limit(limit)
            
            conversations = []
            for conv in query.all():
                # 获取对话的消息数量
                message_count = session.query(func.count(Message.id)).filter_by(conversation_id=conv.id).scalar()
                
                conversation_data = {
                    "conversation_id": conv.conversation_id,
                    "user_id": conv.user_id,
                    "title": conv.title,
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat(),
                    "is_active": conv.is_active,
                    "message_count": message_count,
                    "metadata": json.loads(conv.metadata) if conv.metadata else None
                }
                conversations.append(conversation_data)
            
            return conversations

    def update_conversation_title(self, conversation_id: str, title: str) -> bool:
        """更新对话标题
        
        Args:
            conversation_id: 对话ID
            title: 新标题
            
        Returns:
            success: 是否成功
        """
        with self.Session() as session:
            conversation = session.query(Conversation).filter_by(conversation_id=conversation_id).first()
            if not conversation:
                return False
            
            conversation.title = title
            conversation.updated_at = datetime.utcnow()
            session.commit()
            
            return True

    def archive_conversation(self, conversation_id: str) -> bool:
        """归档对话（标记为非活跃）
        
        Args:
            conversation_id: 对话ID
            
        Returns:
            success: 是否成功
        """
        with self.Session() as session:
            conversation = session.query(Conversation).filter_by(conversation_id=conversation_id).first()
            if not conversation:
                return False
            
            conversation.is_active = False
            conversation.updated_at = datetime.utcnow()
            session.commit()
            
            return True

    def delete_conversation(self, conversation_id: str) -> bool:
        """删除对话
        
        Args:
            conversation_id: 对话ID
            
        Returns:
            success: 是否成功
        """
        with self.Session() as session:
            conversation = session.query(Conversation).filter_by(conversation_id=conversation_id).first()
            if not conversation:
                return False
            
            # 删除对话（级联删除所有消息）
            session.delete(conversation)
            session.commit()
            
            logger.info(f"删除对话: {conversation_id}")
            return True

    def cleanup_expired_conversations(self) -> int:
        """清理过期对话
        
        Returns:
            count: 清理的对话数量
        """
        expiry_date = datetime.utcnow() - timedelta(days=self.expiry_days)
        
        with self.Session() as session:
            # 查找过期的对话
            expired_conversations = session.query(Conversation)\
                .filter(Conversation.updated_at < expiry_date)\
                .all()
            
            count = 0
            for conv in expired_conversations:
                session.delete(conv)
                count += 1
            
            session.commit()
            
            if count > 0:
                logger.info(f"清理了 {count} 个过期对话")
            
            return count

    def get_stats(self) -> Dict[str, Any]:
        """获取对话统计信息
        
        Returns:
            stats: 统计信息
        """
        with self.Session() as session:
            total_conversations = session.query(func.count(Conversation.id)).scalar()
            active_conversations = session.query(func.count(Conversation.id)).filter_by(is_active=True).scalar()
            total_messages = session.query(func.count(Message.id)).scalar()
            
            # 按角色统计消息
            role_counts = {}
            for role, count in session.query(Message.role, func.count(Message.id)).group_by(Message.role).all():
                role_counts[role] = count
            
            # 最近的活动
            latest_conversation = session.query(Conversation).order_by(Conversation.updated_at.desc()).first()
            latest_activity = latest_conversation.updated_at.isoformat() if latest_conversation else None
            
            return {
                "total_conversations": total_conversations,
                "active_conversations": active_conversations,
                "total_messages": total_messages,
                "message_by_role": role_counts,
                "latest_activity": latest_activity,
                "config": {
                    "max_turns": self.max_turns,
                    "expiry_days": self.expiry_days
                }
            }