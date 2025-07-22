#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gRPC客户端测试脚本
快速测试知识库RPC服务
"""

import sys
import time
from pathlib import Path

# 设置控制台编码为UTF-8（Windows兼容性）
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

# 添加src路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.rpc.grpc_client import KnowledgeServiceClient

def test_basic_functionality():
    """测试基本功能"""
    print("🧪 开始测试知识库gRPC服务")
    print("=" * 50)
    
    # 创建客户端
    try:
        client = KnowledgeServiceClient('localhost:50051')
        print("✅ 客户端连接成功")
    except Exception as e:
        print(f"❌ 客户端连接失败: {e}")
        print("请确保gRPC服务器正在运行: python run_grpc_server.py")
        return False
    
    try:
        # 1. 健康检查
        print("\n1️⃣ 测试健康检查...")
        if not client.health_check():
            print("❌ 健康检查失败")
            return False
        print("✅ 健康检查通过")
        
        # 2. 获取统计信息
        print("\n2️⃣ 测试获取统计信息...")
        stats = client.get_stats()
        if stats:
            print("✅ 统计信息获取成功")
        else:
            print("⚠️ 统计信息获取失败（可能知识库未初始化）")
        
        # 3. 测试搜索功能
        print("\n3️⃣ 测试文档搜索...")
        search_results = client.search_documents("API", k=3)
        if search_results:
            print(f"✅ 搜索成功，返回 {len(search_results)} 个结果")
        else:
            print("⚠️ 搜索失败（可能知识库为空）")
        
        # 4. 测试聊天功能
        print("\n4️⃣ 测试聊天功能...")
        test_question = "什么是API？"
        chat_response = client.chat(test_question, use_feedback=True)
        if chat_response:
            print(f"✅ 聊天成功")
            print(f"问题: {test_question}")
            print(f"答案: {chat_response.final_answer[:100]}...")
            
            # 5. 测试反馈功能
            print("\n5️⃣ 测试反馈功能...")
            feedback_id = client.submit_feedback(
                question=test_question,
                original_answer=chat_response.original_answer,
                feedback_type="positive",
                feedback_text="测试反馈"
            )
            if feedback_id:
                print(f"✅ 反馈提交成功 (ID: {feedback_id})")
                
                # 6. 测试反馈历史
                print("\n6️⃣ 测试反馈历史...")
                history = client.get_feedback_history(test_question)
                if history:
                    print(f"✅ 反馈历史获取成功，共 {len(history)} 条记录")
                else:
                    print("⚠️ 反馈历史获取失败")
            else:
                print("❌ 反馈提交失败")
        else:
            print("❌ 聊天失败（可能知识库未初始化）")
        
        print("\n🎉 所有测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False
    
    finally:
        client.close()

def test_performance():
    """性能测试"""
    print("\n⚡ 开始性能测试")
    print("-" * 30)
    
    client = KnowledgeServiceClient('localhost:50051')
    
    try:
        # 测试多次请求的响应时间
        test_questions = [
            "什么是API？",
            "如何使用Python？",
            "什么是机器学习？",
            "数据库是什么？",
            "什么是云计算？"
        ]
        
        total_time = 0
        successful_requests = 0
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n测试请求 {i}/5: {question}")
            
            start_time = time.time()
            response = client.chat(question, use_feedback=False)
            end_time = time.time()
            
            response_time = end_time - start_time
            total_time += response_time
            
            if response:
                successful_requests += 1
                print(f"✅ 响应时间: {response_time:.2f}秒")
            else:
                print(f"❌ 请求失败")
        
        if successful_requests > 0:
            avg_time = total_time / successful_requests
            print(f"\n📊 性能统计:")
            print(f"  成功请求: {successful_requests}/{len(test_questions)}")
            print(f"  平均响应时间: {avg_time:.2f}秒")
            print(f"  总耗时: {total_time:.2f}秒")
        
    finally:
        client.close()

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='gRPC客户端测试')
    parser.add_argument('--server', default='localhost:50051', help='服务器地址')
    parser.add_argument('--performance', action='store_true', help='运行性能测试')
    parser.add_argument('--basic', action='store_true', help='运行基本功能测试')
    
    args = parser.parse_args()
    
    if not args.basic and not args.performance:
        # 默认运行基本测试
        args.basic = True
    
    success = True
    
    if args.basic:
        success &= test_basic_functionality()
    
    if args.performance:
        test_performance()
    
    if success:
        print("\n🎊 所有测试通过！")
    else:
        print("\n⚠️ 部分测试失败，请检查服务器状态")
    
    return 0 if success else 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)