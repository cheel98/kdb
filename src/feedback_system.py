#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
反馈学习系统
实现用户反馈收集、存储和基于反馈的答案优化
"""

import os
import json
import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import hashlib

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FeedbackRecord:
    """反馈记录数据结构"""
    id: Optional[int] = None
    question: str = ""
    original_answer: str = ""
    user_feedback: str = ""  # positive, negative, corrected
    corrected_answer: Optional[str] = None
    feedback_text: Optional[str] = None
    timestamp: Optional[str] = None
    question_hash: Optional[str] = None
    source_documents: Optional[str] = None  # JSON string
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()
        if not self.question_hash:
            self.question_hash = hashlib.md5(self.question.encode()).hexdigest()

class FeedbackDatabase:
    """反馈数据库管理"""
    
    def __init__(self, db_path: str = "./feedback.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """初始化数据库表"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    original_answer TEXT NOT NULL,
                    user_feedback TEXT NOT NULL,
                    corrected_answer TEXT,
                    feedback_text TEXT,
                    timestamp TEXT NOT NULL,
                    question_hash TEXT NOT NULL,
                    source_documents TEXT
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS answer_improvements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_hash TEXT NOT NULL,
                    improved_answer TEXT NOT NULL,
                    confidence_score REAL DEFAULT 0.0,
                    feedback_count INTEGER DEFAULT 1,
                    last_updated TEXT NOT NULL,
                    UNIQUE(question_hash)
                )
            """)
            
            # 创建索引
            conn.execute("CREATE INDEX IF NOT EXISTS idx_question_hash ON feedback(question_hash)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON feedback(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_user_feedback ON feedback(user_feedback)")
            
            conn.commit()
    
    def add_feedback(self, feedback: FeedbackRecord) -> int:
        """添加反馈记录"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO feedback (
                    question, original_answer, user_feedback, corrected_answer,
                    feedback_text, timestamp, question_hash, source_documents
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                feedback.question,
                feedback.original_answer,
                feedback.user_feedback,
                feedback.corrected_answer,
                feedback.feedback_text,
                feedback.timestamp,
                feedback.question_hash,
                feedback.source_documents
            ))
            feedback_id = cursor.lastrowid
            conn.commit()
            
            # 如果是纠正性反馈，更新改进答案
            if feedback.user_feedback == "corrected" and feedback.corrected_answer:
                self._update_improved_answer(feedback)
            
            return feedback_id
    
    def _update_improved_answer(self, feedback: FeedbackRecord):
        """更新改进的答案"""
        with sqlite3.connect(self.db_path) as conn:
            # 检查是否已存在改进答案
            existing = conn.execute(
                "SELECT * FROM answer_improvements WHERE question_hash = ?",
                (feedback.question_hash,)
            ).fetchone()
            
            if existing:
                # 更新现有记录
                conn.execute("""
                    UPDATE answer_improvements 
                    SET improved_answer = ?, feedback_count = feedback_count + 1,
                        last_updated = ?, confidence_score = ?
                    WHERE question_hash = ?
                """, (
                    feedback.corrected_answer,
                    feedback.timestamp,
                    min(1.0, existing[4] + 0.2),  # 增加置信度
                    feedback.question_hash
                ))
            else:
                # 创建新记录
                conn.execute("""
                    INSERT INTO answer_improvements (
                        question_hash, improved_answer, confidence_score,
                        feedback_count, last_updated
                    ) VALUES (?, ?, ?, ?, ?)
                """, (
                    feedback.question_hash,
                    feedback.corrected_answer,
                    0.5,  # 初始置信度
                    1,
                    feedback.timestamp
                ))
            
            conn.commit()
    
    def get_feedback_by_question(self, question: str) -> List[FeedbackRecord]:
        """根据问题获取反馈记录"""
        question_hash = hashlib.md5(question.encode()).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT * FROM feedback WHERE question_hash = ? ORDER BY timestamp DESC",
                (question_hash,)
            ).fetchall()
            
            return [self._row_to_feedback(row) for row in rows]
    
    def get_improved_answer(self, question: str) -> Optional[Dict[str, Any]]:
        """获取改进的答案"""
        question_hash = hashlib.md5(question.encode()).hexdigest()
        
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT * FROM answer_improvements WHERE question_hash = ?",
                (question_hash,)
            ).fetchone()
            
            if row:
                return {
                    "improved_answer": row[2],
                    "confidence_score": row[3],
                    "feedback_count": row[4],
                    "last_updated": row[5]
                }
            
            return None
    
    def get_feedback_stats(self) -> Dict[str, Any]:
        """获取反馈统计信息"""
        with sqlite3.connect(self.db_path) as conn:
            total_feedback = conn.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]
            
            positive_feedback = conn.execute(
                "SELECT COUNT(*) FROM feedback WHERE user_feedback = 'positive'"
            ).fetchone()[0]
            
            negative_feedback = conn.execute(
                "SELECT COUNT(*) FROM feedback WHERE user_feedback = 'negative'"
            ).fetchone()[0]
            
            corrected_feedback = conn.execute(
                "SELECT COUNT(*) FROM feedback WHERE user_feedback = 'corrected'"
            ).fetchone()[0]
            
            improved_answers = conn.execute(
                "SELECT COUNT(*) FROM answer_improvements"
            ).fetchone()[0]
            
            return {
                "total_feedback": total_feedback,
                "positive_feedback": positive_feedback,
                "negative_feedback": negative_feedback,
                "corrected_feedback": corrected_feedback,
                "improved_answers": improved_answers,
                "satisfaction_rate": positive_feedback / max(1, total_feedback) * 100
            }
    
    def _row_to_feedback(self, row) -> FeedbackRecord:
        """将数据库行转换为FeedbackRecord"""
        return FeedbackRecord(
            id=row[0],
            question=row[1],
            original_answer=row[2],
            user_feedback=row[3],
            corrected_answer=row[4],
            feedback_text=row[5],
            timestamp=row[6],
            question_hash=row[7],
            source_documents=row[8]
        )

class FeedbackLearningSystem:
    """反馈学习系统主类"""
    
    def __init__(self, db_path: str = "./feedback.db"):
        self.db = FeedbackDatabase(db_path)
        self.confidence_threshold = 0.7  # 使用改进答案的置信度阈值
    
    def collect_feedback(self, question: str, original_answer: str, 
                        feedback_type: str, corrected_answer: str = None,
                        feedback_text: str = None, source_documents: List[Dict] = None) -> int:
        """收集用户反馈"""
        feedback = FeedbackRecord(
            question=question,
            original_answer=original_answer,
            user_feedback=feedback_type,
            corrected_answer=corrected_answer,
            feedback_text=feedback_text,
            source_documents=json.dumps(source_documents) if source_documents else None
        )
        
        feedback_id = self.db.add_feedback(feedback)
        logger.info(f"收集到反馈: {feedback_type}, ID: {feedback_id}")
        
        return feedback_id
    
    def get_optimized_answer(self, question: str, original_answer: str) -> Tuple[str, Dict[str, Any]]:
        """获取优化后的答案"""
        improved = self.db.get_improved_answer(question)
        
        if improved and improved["confidence_score"] >= self.confidence_threshold:
            return improved["improved_answer"], {
                "is_improved": True,
                "confidence_score": improved["confidence_score"],
                "feedback_count": improved["feedback_count"],
                "last_updated": improved["last_updated"]
            }
        
        return original_answer, {
            "is_improved": False,
            "confidence_score": 0.0,
            "feedback_count": 0
        }
    
    def get_similar_questions_feedback(self, question: str, similarity_threshold: float = 0.8) -> List[Dict[str, Any]]:
        """获取相似问题的反馈（简单实现，基于关键词匹配）"""
        # 这里可以集成更复杂的相似度计算，如使用embedding
        question_words = set(question.lower().split())
        
        with sqlite3.connect(self.db.db_path) as conn:
            all_feedback = conn.execute(
                "SELECT DISTINCT question, question_hash FROM feedback"
            ).fetchall()
            
            similar_feedback = []
            for q, q_hash in all_feedback:
                q_words = set(q.lower().split())
                similarity = len(question_words & q_words) / len(question_words | q_words)
                
                if similarity >= similarity_threshold:
                    improved = self.db.get_improved_answer(q)
                    if improved:
                        similar_feedback.append({
                            "question": q,
                            "similarity": similarity,
                            "improved_answer": improved["improved_answer"],
                            "confidence_score": improved["confidence_score"]
                        })
            
            return sorted(similar_feedback, key=lambda x: x["similarity"], reverse=True)
    
    def get_feedback_history(self, question: str) -> List[FeedbackRecord]:
        """获取问题的反馈历史"""
        return self.db.get_feedback_by_question(question)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """获取系统统计信息"""
        return self.db.get_feedback_stats()
    
    def export_feedback_data(self, output_path: str) -> bool:
        """导出反馈数据用于进一步分析"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                # 导出反馈数据
                feedback_data = conn.execute("SELECT * FROM feedback").fetchall()
                improved_data = conn.execute("SELECT * FROM answer_improvements").fetchall()
                
                export_data = {
                    "feedback_records": feedback_data,
                    "improved_answers": improved_data,
                    "export_timestamp": datetime.now().isoformat()
                }
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                
                logger.info(f"反馈数据已导出到: {output_path}")
                return True
                
        except Exception as e:
            logger.error(f"导出反馈数据失败: {e}")
            return False

if __name__ == "__main__":
    # 测试代码
    feedback_system = FeedbackLearningSystem()
    
    # 模拟收集反馈
    question = "什么是人工智能？"
    original_answer = "人工智能是计算机科学的一个分支。"
    corrected_answer = "人工智能是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。"
    
    # 收集纠正性反馈
    feedback_id = feedback_system.collect_feedback(
        question=question,
        original_answer=original_answer,
        feedback_type="corrected",
        corrected_answer=corrected_answer,
        feedback_text="原答案太简单，需要更详细的解释"
    )
    
    print(f"反馈ID: {feedback_id}")
    
    # 获取优化后的答案
    optimized_answer, meta = feedback_system.get_optimized_answer(question, original_answer)
    print(f"优化后的答案: {optimized_answer}")
    print(f"元信息: {meta}")
    
    # 获取统计信息
    stats = feedback_system.get_system_stats()
    print(f"系统统计: {stats}")