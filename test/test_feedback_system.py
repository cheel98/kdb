#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
反馈学习系统测试脚本
验证反馈收集、存储和优化功能
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from feedback_system import FeedbackLearningSystem, FeedbackRecord, FeedbackDatabase

class TestFeedbackSystem(unittest.TestCase):
    """反馈系统测试类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时数据库
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        self.feedback_system = FeedbackLearningSystem(self.temp_db.name)
        
        # 测试数据
        self.test_question = "什么是人工智能？"
        self.test_original_answer = "人工智能是计算机科学的一个分支。"
        self.test_corrected_answer = "人工智能是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。"
    
    def tearDown(self):
        """测试后清理"""
        # 删除临时数据库
        try:
            if hasattr(self, 'feedback_system'):
                # 确保数据库连接关闭
                del self.feedback_system
            if os.path.exists(self.temp_db.name):
                os.unlink(self.temp_db.name)
        except (PermissionError, OSError):
            # Windows文件锁定问题，忽略
            pass
    
    def test_feedback_record_creation(self):
        """测试反馈记录创建"""
        record = FeedbackRecord(
            question=self.test_question,
            original_answer=self.test_original_answer,
            user_feedback="positive"
        )
        
        self.assertEqual(record.question, self.test_question)
        self.assertEqual(record.user_feedback, "positive")
        self.assertIsNotNone(record.timestamp)
        self.assertIsNotNone(record.question_hash)
    
    def test_database_initialization(self):
        """测试数据库初始化"""
        db = FeedbackDatabase(self.temp_db.name)
        
        # 验证表是否创建
        import sqlite3
        with sqlite3.connect(self.temp_db.name) as conn:
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
            
            table_names = [table[0] for table in tables]
            self.assertIn('feedback', table_names)
            self.assertIn('answer_improvements', table_names)
    
    def test_positive_feedback_collection(self):
        """测试正面反馈收集"""
        feedback_id = self.feedback_system.collect_feedback(
            question=self.test_question,
            original_answer=self.test_original_answer,
            feedback_type="positive",
            feedback_text="答案很好"
        )
        
        self.assertIsInstance(feedback_id, int)
        self.assertGreater(feedback_id, 0)
        
        # 验证反馈是否存储
        history = self.feedback_system.get_feedback_history(self.test_question)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].user_feedback, "positive")
    
    def test_negative_feedback_collection(self):
        """测试负面反馈收集"""
        feedback_id = self.feedback_system.collect_feedback(
            question=self.test_question,
            original_answer=self.test_original_answer,
            feedback_type="negative",
            feedback_text="答案太简单"
        )
        
        self.assertIsInstance(feedback_id, int)
        
        # 验证统计信息
        stats = self.feedback_system.get_system_stats()
        self.assertEqual(stats['negative_feedback'], 1)
        self.assertEqual(stats['total_feedback'], 1)
    
    def test_corrected_feedback_and_optimization(self):
        """测试纠正反馈和答案优化"""
        # 提交纠正反馈
        feedback_id = self.feedback_system.collect_feedback(
            question=self.test_question,
            original_answer=self.test_original_answer,
            feedback_type="corrected",
            corrected_answer=self.test_corrected_answer,
            feedback_text="需要更详细的解释"
        )
        
        self.assertIsInstance(feedback_id, int)
        
        # 验证改进答案是否生成
        improved = self.feedback_system.db.get_improved_answer(self.test_question)
        self.assertIsNotNone(improved)
        self.assertEqual(improved['improved_answer'], self.test_corrected_answer)
        self.assertGreater(improved['confidence_score'], 0)
        
        # 测试获取优化答案
        optimized_answer, meta = self.feedback_system.get_optimized_answer(
            self.test_question, self.test_original_answer
        )
        
        # 由于置信度可能不够高，可能返回原始答案
        self.assertIsNotNone(optimized_answer)
        self.assertIsInstance(meta, dict)
    
    def test_multiple_corrections_confidence_increase(self):
        """测试多次纠正提高置信度"""
        # 第一次纠正
        self.feedback_system.collect_feedback(
            question=self.test_question,
            original_answer=self.test_original_answer,
            feedback_type="corrected",
            corrected_answer=self.test_corrected_answer
        )
        
        improved_1 = self.feedback_system.db.get_improved_answer(self.test_question)
        initial_confidence = improved_1['confidence_score']
        
        # 第二次纠正（相同答案）
        self.feedback_system.collect_feedback(
            question=self.test_question,
            original_answer=self.test_original_answer,
            feedback_type="corrected",
            corrected_answer=self.test_corrected_answer
        )
        
        improved_2 = self.feedback_system.db.get_improved_answer(self.test_question)
        final_confidence = improved_2['confidence_score']
        
        # 置信度应该增加
        self.assertGreater(final_confidence, initial_confidence)
        self.assertEqual(improved_2['feedback_count'], 2)
    
    def test_similar_questions_detection(self):
        """测试相似问题检测"""
        # 添加一个相似问题的反馈
        similar_question = "人工智能是什么？"
        self.feedback_system.collect_feedback(
            question=similar_question,
            original_answer="AI是一种技术",
            feedback_type="corrected",
            corrected_answer="人工智能是模拟人类智能的技术"
        )
        
        # 检测相似问题
        similar_feedback = self.feedback_system.get_similar_questions_feedback(
            self.test_question, similarity_threshold=0.5
        )
        
        # 应该能找到相似问题
        self.assertGreater(len(similar_feedback), 0)
        self.assertIn('similarity', similar_feedback[0])
        self.assertIn('improved_answer', similar_feedback[0])
    
    def test_feedback_statistics(self):
        """测试反馈统计功能"""
        # 添加各种类型的反馈
        self.feedback_system.collect_feedback(
            question="问题1", original_answer="答案1", feedback_type="positive"
        )
        self.feedback_system.collect_feedback(
            question="问题2", original_answer="答案2", feedback_type="negative"
        )
        self.feedback_system.collect_feedback(
            question="问题3", original_answer="答案3", feedback_type="corrected",
            corrected_answer="纠正答案3"
        )
        
        stats = self.feedback_system.get_system_stats()
        
        self.assertEqual(stats['total_feedback'], 3)
        self.assertEqual(stats['positive_feedback'], 1)
        self.assertEqual(stats['negative_feedback'], 1)
        self.assertEqual(stats['corrected_feedback'], 1)
        self.assertEqual(stats['improved_answers'], 1)
        self.assertAlmostEqual(stats['satisfaction_rate'], 33.33, places=1)
    
    def test_data_export(self):
        """测试数据导出功能"""
        # 添加一些测试数据
        self.feedback_system.collect_feedback(
            question=self.test_question,
            original_answer=self.test_original_answer,
            feedback_type="corrected",
            corrected_answer=self.test_corrected_answer
        )
        
        # 导出数据
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            export_file = f.name
        
        try:
            success = self.feedback_system.export_feedback_data(export_file)
            self.assertTrue(success)
            
            # 验证导出文件存在且包含数据
            self.assertTrue(os.path.exists(export_file))
            
            import json
            with open(export_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.assertIn('feedback_records', data)
            self.assertIn('improved_answers', data)
            self.assertIn('export_timestamp', data)
            
        finally:
            if os.path.exists(export_file):
                os.unlink(export_file)
    
    def test_confidence_threshold_behavior(self):
        """测试置信度阈值行为"""
        # 设置高置信度阈值
        self.feedback_system.confidence_threshold = 0.9
        
        # 添加一次纠正（置信度应该不够高）
        self.feedback_system.collect_feedback(
            question=self.test_question,
            original_answer=self.test_original_answer,
            feedback_type="corrected",
            corrected_answer=self.test_corrected_answer
        )
        
        # 应该返回原始答案（置信度不够）
        optimized_answer, meta = self.feedback_system.get_optimized_answer(
            self.test_question, self.test_original_answer
        )
        
        self.assertEqual(optimized_answer, self.test_original_answer)
        self.assertFalse(meta['is_improved'])
        
        # 降低阈值
        self.feedback_system.confidence_threshold = 0.3
        
        # 现在应该返回优化答案
        optimized_answer, meta = self.feedback_system.get_optimized_answer(
            self.test_question, self.test_original_answer
        )
        
        self.assertEqual(optimized_answer, self.test_corrected_answer)
        self.assertTrue(meta['is_improved'])

def run_integration_test():
    """运行集成测试"""
    print("🧪 开始反馈学习系统集成测试...")
    
    # 创建临时数据库
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as temp_db:
        temp_db_path = temp_db.name
    
    try:
        # 初始化系统
        feedback_system = FeedbackLearningSystem(temp_db_path)
        
        # 模拟用户交互流程
        print("\n1. 模拟用户提问和反馈...")
        
        question = "什么是机器学习？"
        original_answer = "机器学习是AI的一部分。"
        
        # 收集负面反馈
        feedback_id_1 = feedback_system.collect_feedback(
            question=question,
            original_answer=original_answer,
            feedback_type="negative",
            feedback_text="答案太简单了"
        )
        print(f"   收集负面反馈，ID: {feedback_id_1}")
        
        # 收集纠正反馈
        corrected_answer = "机器学习是人工智能的一个子领域，通过算法让计算机从数据中学习模式。"
        feedback_id_2 = feedback_system.collect_feedback(
            question=question,
            original_answer=original_answer,
            feedback_type="corrected",
            corrected_answer=corrected_answer,
            feedback_text="提供更详细的定义"
        )
        print(f"   收集纠正反馈，ID: {feedback_id_2}")
        
        # 再次纠正以提高置信度
        feedback_id_3 = feedback_system.collect_feedback(
            question=question,
            original_answer=original_answer,
            feedback_type="corrected",
            corrected_answer=corrected_answer
        )
        print(f"   再次纠正提高置信度，ID: {feedback_id_3}")
        
        # 收集正面反馈
        feedback_id_4 = feedback_system.collect_feedback(
            question=question,
            original_answer=corrected_answer,
            feedback_type="positive",
            feedback_text="这个答案很好"
        )
        print(f"   收集正面反馈，ID: {feedback_id_4}")
        
        print("\n2. 测试答案优化...")
        
        # 获取优化答案
        optimized_answer, meta = feedback_system.get_optimized_answer(question, original_answer)
        print(f"   原始答案: {original_answer}")
        print(f"   优化答案: {optimized_answer}")
        print(f"   是否改进: {meta['is_improved']}")
        print(f"   置信度: {meta['confidence_score']:.2f}")
        
        print("\n3. 测试相似问题检测...")
        
        # 添加相似问题
        similar_question = "机器学习是什么？"
        feedback_system.collect_feedback(
            question=similar_question,
            original_answer="ML是一种技术",
            feedback_type="corrected",
            corrected_answer="机器学习是让机器自动学习的技术"
        )
        
        similar_feedback = feedback_system.get_similar_questions_feedback(question, 0.6)
        print(f"   找到 {len(similar_feedback)} 个相似问题")
        for sf in similar_feedback:
            print(f"   - {sf['question']} (相似度: {sf['similarity']:.2f})")
        
        print("\n4. 获取系统统计...")
        
        stats = feedback_system.get_system_stats()
        print(f"   总反馈数: {stats['total_feedback']}")
        print(f"   正面反馈: {stats['positive_feedback']}")
        print(f"   负面反馈: {stats['negative_feedback']}")
        print(f"   纠正反馈: {stats['corrected_feedback']}")
        print(f"   改进答案: {stats['improved_answers']}")
        print(f"   满意度: {stats['satisfaction_rate']:.1f}%")
        
        print("\n5. 测试数据导出...")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as export_file:
            export_path = export_file.name
        
        try:
            success = feedback_system.export_feedback_data(export_path)
            if success:
                print(f"   数据导出成功: {export_path}")
                
                import json
                with open(export_path, 'r', encoding='utf-8') as f:
                    export_data = json.load(f)
                
                print(f"   导出记录数: {len(export_data['feedback_records'])}")
                print(f"   改进答案数: {len(export_data['improved_answers'])}")
            else:
                print("   数据导出失败")
        finally:
            if os.path.exists(export_path):
                os.unlink(export_path)
        
        print("\n✅ 集成测试完成！")
        
    finally:
        # 清理临时文件
        try:
            # 确保对象被删除以释放数据库连接
            if 'feedback_system' in locals():
                del feedback_system
            if os.path.exists(temp_db_path):
                os.unlink(temp_db_path)
        except (PermissionError, OSError):
            # Windows文件锁定问题，忽略
            print(f"   注意: 无法删除临时文件 {temp_db_path} (文件被锁定)")
            pass

if __name__ == "__main__":
    print("🧪 反馈学习系统测试")
    print("=" * 50)
    
    # 运行单元测试
    print("\n📋 运行单元测试...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\n" + "=" * 50)
    
    # 运行集成测试
    run_integration_test()