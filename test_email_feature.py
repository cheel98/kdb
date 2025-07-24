#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮箱验证功能测试脚本
"""

import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from rpc.grpc_client import KnowledgeServiceClient

def test_email_verification():
    """测试邮箱验证功能"""
    print("🧪 测试邮箱验证功能")
    print("=" * 50)
    
    client = KnowledgeServiceClient()
    
    try:
        # 健康检查
        if not client.health_check():
            print("❌ 服务器不健康，无法进行测试")
            return False
        
        # 测试有效邮箱
        print("\n📧 测试有效邮箱:")
        valid_emails = [
            "test@example.com",
            "user123@gmail.com",
            "admin@company.org"
        ]
        
        for email in valid_emails:
            print(f"\n测试邮箱: {email}")
            response = client.verify_email(email)
            if response and response.is_valid:
                print(f"✅ 验证成功，用户ID: {response.user_id}")
            else:
                print(f"❌ 验证失败")
        
        # 测试无效邮箱
        print("\n📧 测试无效邮箱:")
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            ""
        ]
        
        for email in invalid_emails:
            print(f"\n测试邮箱: {email}")
            response = client.verify_email(email)
            if response and not response.is_valid:
                print(f"✅ 正确识别为无效邮箱")
            else:
                print(f"❌ 验证结果不正确")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False
    
    finally:
        client.close()

def test_email_chat():
    """测试带邮箱验证的聊天功能"""
    print("\n🧪 测试带邮箱验证的聊天功能")
    print("=" * 50)
    
    client = KnowledgeServiceClient()
    
    try:
        # 健康检查
        if not client.health_check():
            print("❌ 服务器不健康，无法进行测试")
            return False
        
        # 测试邮箱聊天
        test_email = "test@example.com"
        test_question = "什么是人工智能？"
        
        print(f"\n📧 使用邮箱: {test_email}")
        print(f"❓ 测试问题: {test_question}")
        
        response = client.chat_with_email(
            email=test_email,
            question=test_question,
            conversation_title="测试对话"
        )
        
        if response and response.success:
            print("✅ 邮箱聊天测试成功")
            print(f"📝 回答: {response.final_answer[:100]}...")
            
            # 测试后续对话
            if response.feedback_info and 'conversation_id' in response.feedback_info:
                conversation_id = response.feedback_info['conversation_id']
                print(f"🆔 对话ID: {conversation_id}")
                
                # 发送第二个问题
                follow_up_question = "请详细解释一下"
                print(f"\n❓ 后续问题: {follow_up_question}")
                
                follow_up_response = client.chat_with_email(
                    email=test_email,
                    question=follow_up_question,
                    conversation_id=conversation_id
                )
                
                if follow_up_response and follow_up_response.success:
                    print("✅ 后续对话测试成功")
                    print(f"📝 回答: {follow_up_response.final_answer[:100]}...")
                else:
                    print("❌ 后续对话测试失败")
            
            return True
        else:
            print("❌ 邮箱聊天测试失败")
            return False
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False
    
    finally:
        client.close()

def main():
    """主测试函数"""
    print("🚀 开始邮箱功能测试")
    print("=" * 60)
    
    # 测试邮箱验证
    email_test_passed = test_email_verification()
    
    # 测试邮箱聊天
    chat_test_passed = test_email_chat()
    
    # 总结测试结果
    print("\n📊 测试结果总结")
    print("=" * 50)
    print(f"邮箱验证功能: {'✅ 通过' if email_test_passed else '❌ 失败'}")
    print(f"邮箱聊天功能: {'✅ 通过' if chat_test_passed else '❌ 失败'}")
    
    if email_test_passed and chat_test_passed:
        print("\n🎉 所有测试通过！邮箱功能正常工作")
        return True
    else:
        print("\n⚠️ 部分测试失败，请检查服务器配置")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)