#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gRPC客户端示例
演示如何调用知识库RPC服务
"""

import sys
import logging
from pathlib import Path

import grpc

# 添加项目路径
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# 导入生成的gRPC代码
from grpc_generated import knowledge_service_pb2
from grpc_generated import knowledge_service_pb2_grpc

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KnowledgeServiceClient:
    """知识库服务客户端"""
    
    def __init__(self, server_address='localhost:50051'):
        """初始化客户端"""
        self.server_address = server_address
        self.channel = None
        self.stub = None
        self.connect()
    
    def connect(self):
        """连接到服务器"""
        try:
            self.channel = grpc.insecure_channel(self.server_address)
            self.stub = knowledge_service_pb2_grpc.KnowledgeServiceStub(self.channel)
            logger.info(f"已连接到服务器: {self.server_address}")
        except Exception as e:
            logger.error(f"连接服务器失败: {e}")
            raise
    
    def close(self):
        """关闭连接"""
        if self.channel:
            self.channel.close()
            logger.info("连接已关闭")
    
    def health_check(self):
        """健康检查"""
        try:
            request = knowledge_service_pb2.HealthCheckRequest()
            response = self.stub.HealthCheck(request)
            
            print(f"🏥 健康检查结果:")
            print(f"  状态: {'健康' if response.healthy else '不健康'}")
            print(f"  详情: {response.status}")
            print(f"  版本: {response.version}")
            
            return response.healthy
            
        except grpc.RpcError as e:
            logger.error(f"健康检查失败: {e}")
            return False
    
    def chat(self, question, use_feedback=True):
        """聊天对话"""
        try:
            request = knowledge_service_pb2.ChatRequest(
                question=question,
                use_feedback=use_feedback
            )
            
            response = self.stub.Chat(request)
            
            if response.success:
                print(f"\n💬 问题: {response.question}")
                print(f"📝 答案: {response.final_answer}")
                
                if response.feedback_info.is_improved:
                    print(f"🎯 这是优化后的答案 (置信度: {response.feedback_info.confidence_score:.2%})")
                
                if response.source_documents:
                    print(f"\n📚 参考文档 ({len(response.source_documents)} 个):")
                    for i, doc in enumerate(response.source_documents[:3], 1):
                        print(f"  {i}. {doc.source}: {doc.content[:100]}...")
                
                if response.feedback_info.similar_questions:
                    print(f"\n🔍 相似问题:")
                    for sq in response.feedback_info.similar_questions:
                        print(f"  - {sq.question} (相似度: {sq.similarity_score:.2%})")
                
                return response
            else:
                print(f"❌ 聊天失败: {response.error_message}")
                return None
                
        except grpc.RpcError as e:
            logger.error(f"聊天请求失败: {e}")
            return None
    
    def submit_feedback(self, question, original_answer, feedback_type, 
                       corrected_answer=None, feedback_text=None):
        """提交反馈"""
        try:
            request = knowledge_service_pb2.FeedbackRequest(
                question=question,
                original_answer=original_answer,
                feedback_type=feedback_type,
                corrected_answer=corrected_answer or "",
                feedback_text=feedback_text or ""
            )
            
            response = self.stub.SubmitFeedback(request)
            
            if response.success:
                print(f"✅ 反馈提交成功 (ID: {response.feedback_id})")
                return response.feedback_id
            else:
                print(f"❌ 反馈提交失败: {response.error_message}")
                return None
                
        except grpc.RpcError as e:
            logger.error(f"提交反馈失败: {e}")
            return None
    
    def get_feedback_history(self, question):
        """获取反馈历史"""
        try:
            request = knowledge_service_pb2.FeedbackHistoryRequest(
                question=question
            )
            
            response = self.stub.GetFeedbackHistory(request)
            
            if response.success:
                print(f"\n📊 反馈历史 ({len(response.records)} 条):")
                for i, record in enumerate(response.records, 1):
                    print(f"  {i}. [{record.user_feedback}] {record.timestamp[:19]}")
                    if record.feedback_text:
                        print(f"     说明: {record.feedback_text}")
                    if record.corrected_answer:
                        print(f"     纠正: {record.corrected_answer[:100]}...")
                
                return response.records
            else:
                print(f"❌ 获取反馈历史失败: {response.error_message}")
                return None
                
        except grpc.RpcError as e:
            logger.error(f"获取反馈历史失败: {e}")
            return None
    
    def get_stats(self):
        """获取统计信息"""
        try:
            request = knowledge_service_pb2.StatsRequest()
            response = self.stub.GetStats(request)
            
            if response.success:
                print(f"\n📈 系统统计信息:")
                print(f"\n📚 知识库:")
                print(f"  文档数量: {response.knowledge_base.total_documents}")
                print(f"  文档块数: {response.knowledge_base.total_chunks}")
                print(f"  存储路径: {response.knowledge_base.vector_store_path}")
                
                print(f"\n💬 反馈系统:")
                print(f"  总反馈数: {response.feedback_system.total_feedback}")
                print(f"  正面反馈: {response.feedback_system.positive_feedback}")
                print(f"  负面反馈: {response.feedback_system.negative_feedback}")
                print(f"  纠正反馈: {response.feedback_system.corrected_feedback}")
                print(f"  改进答案: {response.feedback_system.improved_answers}")
                print(f"  满意度: {response.feedback_system.satisfaction_rate:.2%}")
                
                print(f"\n⚙️ 系统配置:")
                print(f"  反馈学习: {'启用' if response.system_config.feedback_learning_enabled else '禁用'}")
                print(f"  置信阈值: {response.system_config.confidence_threshold:.2f}")
                print(f"  相似阈值: {response.system_config.similarity_threshold:.2f}")
                
                return response
            else:
                print(f"❌ 获取统计信息失败: {response.error_message}")
                return None
                
        except grpc.RpcError as e:
            logger.error(f"获取统计信息失败: {e}")
            return None
    
    def verify_email(self, email):
        """验证邮箱"""
        try:
            request = knowledge_service_pb2.EmailVerificationRequest(
                email=email
            )
            
            response = self.stub.VerifyEmail(request)
            
            if response.success:
                print(f"✅ 邮箱验证成功")
                print(f"  邮箱: {email}")
                print(f"  有效性: {'有效' if response.is_valid else '无效'}")
                print(f"  用户ID: {response.user_id}")
                return response
            else:
                print(f"❌ 邮箱验证失败: {response.error_message}")
                return None
                
        except grpc.RpcError as e:
            logger.error(f"邮箱验证请求失败: {e}")
            return None
    
    def chat_with_email(self, email, question, conversation_id=None, 
                       conversation_title=None, use_feedback=True, 
                       use_reranking=True, top_k=5, similarity_threshold=0.7,
                       max_history_turns=10):
        """带邮箱验证的对话聊天"""
        try:
            request = knowledge_service_pb2.EmailChatRequest(
                email=email,
                question=question,
                conversation_id=conversation_id or "",
                conversation_title=conversation_title or "",
                use_feedback=use_feedback,
                use_reranking=use_reranking,
                top_k=top_k,
                similarity_threshold=similarity_threshold,
                max_history_turns=max_history_turns
            )
            
            response = self.stub.ChatWithEmailVerification(request)
            
            if response.success:
                print(f"\n💬 问题: {response.question}")
                print(f"📧 邮箱: {email}")
                print(f"📝 答案: {response.final_answer}")
                
                if response.feedback_info and 'conversation_id' in response.feedback_info:
                    print(f"🆔 对话ID: {response.feedback_info['conversation_id']}")
                
                if response.source_documents:
                    print(f"\n📚 参考文档 ({len(response.source_documents)} 个):")
                    for i, doc in enumerate(response.source_documents[:3], 1):
                        print(f"  {i}. {doc.source}: {doc.content[:100]}...")
                
                return response
            else:
                print(f"❌ 聊天失败: {response.error_message}")
                return None
                
        except grpc.RpcError as e:
            logger.error(f"邮箱聊天请求失败: {e}")
            return None

    def search_documents(self, query, k=5):
        """搜索文档"""
        try:
            request = knowledge_service_pb2.SearchRequest(
                query=query,
                k=k
            )
            
            response = self.stub.SearchDocuments(request)
            
            if response.success:
                print(f"\n🔍 搜索结果 ({len(response.results)} 个):")
                for i, result in enumerate(response.results, 1):
                    print(f"  {i}. [评分: {result.score:.3f}] {result.content[:100]}...")
                    if result.metadata:
                        print(f"     来源: {result.metadata.get('source', '未知')}")
                
                return response.results
            else:
                print(f"❌ 搜索失败: {response.error_message}")
                return None
                
        except grpc.RpcError as e:
            logger.error(f"搜索请求失败: {e}")
            return None

def interactive_demo():
    """交互式演示"""
    print("🤖 知识库gRPC客户端演示")
    print("=" * 50)
    
    # 创建客户端
    client = KnowledgeServiceClient()
    
    try:
        # 健康检查
        if not client.health_check():
            print("❌ 服务器不健康，退出演示")
            return
        
        # 获取统计信息
        client.get_stats()
        
        # 选择聊天模式
        print("\n💬 选择聊天模式:")
        print("1. 🔓 普通聊天 (不保存对话)")
        print("2. 📧 邮箱验证聊天 (保存对话到数据库)")
        
        mode_choice = input("请选择模式 (1-2): ").strip()
        
        email = None
        conversation_id = None
        
        if mode_choice == '2':
            # 邮箱验证模式
            while True:
                email = input("📧 请输入邮箱地址: ").strip()
                if not email:
                    continue
                
                # 验证邮箱
                email_response = client.verify_email(email)
                if email_response and email_response.is_valid:
                    break
                else:
                    print("❌ 邮箱格式无效，请重新输入")
            
            # 询问是否创建新对话
            create_new = input("\n🆕 是否创建新对话? (y/n): ").strip().lower()
            if create_new == 'y':
                conversation_title = input("📝 请输入对话标题 (可选): ").strip()
            else:
                conversation_id = input("🆔 请输入现有对话ID (可选): ").strip()
        
        print("\n💬 开始聊天 (输入 'quit' 退出):")
        print("-" * 30)
        
        while True:
            try:
                question = input("\n❓ 请输入问题: ").strip()
                
                if question.lower() in ['quit', 'exit', '退出']:
                    break
                
                if not question:
                    continue
                
                # 根据模式发送聊天请求
                if mode_choice == '2' and email:
                    # 邮箱验证聊天
                    response = client.chat_with_email(
                        email=email,
                        question=question,
                        conversation_id=conversation_id,
                        conversation_title=conversation_title if 'conversation_title' in locals() else None
                    )
                    # 更新对话ID以便后续使用
                    if response and response.feedback_info and 'conversation_id' in response.feedback_info:
                        conversation_id = response.feedback_info['conversation_id']
                else:
                    # 普通聊天
                    response = client.chat(question)
                
                if response:
                    # 询问反馈
                    print("\n📝 请对答案进行评价:")
                    print("1. 👍 满意")
                    print("2. 👎 不满意")
                    print("3. ✏️ 需要纠正")
                    print("4. ⏭️ 跳过")
                    
                    feedback_choice = input("请选择 (1-4): ").strip()
                    
                    if feedback_choice == '1':
                        client.submit_feedback(question, response.original_answer, "positive")
                    elif feedback_choice == '2':
                        feedback_text = input("请说明不满意的原因: ").strip()
                        client.submit_feedback(question, response.original_answer, "negative", 
                                             feedback_text=feedback_text)
                    elif feedback_choice == '3':
                        corrected_answer = input("请提供正确答案: ").strip()
                        feedback_text = input("补充说明 (可选): ").strip()
                        if corrected_answer:
                            client.submit_feedback(question, response.original_answer, "corrected",
                                                 corrected_answer=corrected_answer,
                                                 feedback_text=feedback_text)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ 处理请求时出错: {e}")
        
        print("\n👋 演示结束")
        
    finally:
        client.close()

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='知识库gRPC客户端')
    parser.add_argument('--server', default='localhost:50051', help='服务器地址')
    parser.add_argument('--demo', action='store_true', help='运行交互式演示')
    parser.add_argument('--health', action='store_true', help='仅进行健康检查')
    parser.add_argument('--stats', action='store_true', help='仅获取统计信息')
    parser.add_argument('--question', help='发送单个问题')
    parser.add_argument('--email', help='邮箱地址 (用于验证和保存对话)')
    parser.add_argument('--verify-email', help='验证指定邮箱地址')
    
    args = parser.parse_args()
    
    client = KnowledgeServiceClient(args.server)
    
    try:
        if args.health:
            client.health_check()
        elif args.stats:
            client.get_stats()
        elif args.verify_email:
            client.verify_email(args.verify_email)
        elif args.question:
            if args.email:
                # 带邮箱验证的聊天
                client.chat_with_email(args.email, args.question)
            else:
                # 普通聊天
                client.chat(args.question)
        elif args.demo:
            interactive_demo()
        else:
            print("请指定操作参数，使用 --help 查看帮助")
    
    finally:
        client.close()

if __name__ == '__main__':
    main()