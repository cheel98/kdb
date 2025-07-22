#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gRPC-Web代理服务器

将HTTP请求转发到gRPC服务，解决浏览器CORS问题
"""

import os
import sys
import json
import logging
from pathlib import Path
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import grpc

# 添加项目路径
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 导入生成的gRPC代码
from src.rpc.grpc_generated import knowledge_service_pb2
from src.rpc.grpc_generated import knowledge_service_pb2_grpc

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)

# 启用CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# gRPC客户端连接
grpc_channel = None
grpc_stub = None

def get_grpc_stub(server_address='localhost:50051'):
    """获取gRPC存根"""
    global grpc_channel, grpc_stub
    
    if grpc_stub is None:
        try:
            grpc_channel = grpc.insecure_channel(server_address)
            grpc_stub = knowledge_service_pb2_grpc.KnowledgeServiceStub(grpc_channel)
            logger.info(f"已连接到gRPC服务器: {server_address}")
        except Exception as e:
            logger.error(f"连接gRPC服务器失败: {e}")
            raise
    
    return grpc_stub

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    try:
        stub = get_grpc_stub()
        request_pb = knowledge_service_pb2.HealthCheckRequest()
        response = stub.HealthCheck(request_pb)
        
        return jsonify({
            "healthy": response.healthy,
            "status": response.status,
            "version": response.version
        })
    except Exception as e:
        logger.error(f"健康检查失败: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """聊天接口"""
    try:
        data = request.json
        question = data.get('question', '')
        use_feedback = data.get('use_feedback', True)
        
        if not question:
            return jsonify({"error": "问题不能为空"}), 400
        
        stub = get_grpc_stub()
        request_pb = knowledge_service_pb2.ChatRequest(
            question=question,
            use_feedback=use_feedback
        )
        
        response = stub.Chat(request_pb)
        
        # 转换来源文档
        source_documents = []
        for doc in response.source_documents:
            source_doc = {
                "content": doc.content,
                "source": doc.source,
                "metadata": {k: v for k, v in doc.metadata.items()}
            }
            source_documents.append(source_doc)
        
        # 转换反馈信息
        similar_questions = []
        for sq in response.feedback_info.similar_questions:
            similar_q = {
                "question": sq.question,
                "similarity_score": sq.similarity_score,
                "feedback_type": sq.feedback_type
            }
            similar_questions.append(similar_q)
        
        feedback_info = {
            "is_improved": response.feedback_info.is_improved,
            "confidence_score": response.feedback_info.confidence_score,
            "feedback_count": response.feedback_info.feedback_count,
            "similar_questions": similar_questions
        }
        
        result = {
            "question": response.question,
            "original_answer": response.original_answer,
            "final_answer": response.final_answer,
            "source_documents": source_documents,
            "feedback_info": feedback_info,
            "success": response.success,
            "error_message": response.error_message
        }
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"聊天请求失败: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """提交反馈"""
    try:
        data = request.json
        
        # 验证必要字段
        required_fields = ['question', 'original_answer', 'feedback_type']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"缺少必要字段: {field}"}), 400
        
        stub = get_grpc_stub()
        request_pb = knowledge_service_pb2.FeedbackRequest(
            question=data['question'],
            original_answer=data['original_answer'],
            feedback_type=data['feedback_type'],
            corrected_answer=data.get('corrected_answer', ''),
            feedback_text=data.get('feedback_text', '')
        )
        
        response = stub.SubmitFeedback(request_pb)
        
        result = {
            "feedback_id": response.feedback_id,
            "success": response.success,
            "error_message": response.error_message
        }
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"提交反馈失败: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    try:
        stub = get_grpc_stub()
        request_pb = knowledge_service_pb2.StatsRequest()
        response = stub.GetStats(request_pb)
        
        # 转换知识库统计信息
        kb_stats = {
            "document_count": response.knowledge_base.document_count,
            "vector_count": response.knowledge_base.vector_count,
            "last_updated": response.knowledge_base.last_updated
        }
        
        # 转换反馈系统统计信息
        feedback_stats = {
            "total_feedback_count": response.feedback_system.total_feedback_count,
            "positive_count": response.feedback_system.positive_count,
            "negative_count": response.feedback_system.negative_count,
            "corrected_count": response.feedback_system.corrected_count
        }
        
        result = {
            "knowledge_base": kb_stats,
            "feedback_system": feedback_stats,
            "success": True
        }
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"获取统计信息失败: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search_documents():
    """搜索文档"""
    try:
        data = request.json
        query = data.get('query', '')
        k = data.get('k', 5)
        
        if not query:
            return jsonify({"error": "查询不能为空"}), 400
        
        stub = get_grpc_stub()
        request_pb = knowledge_service_pb2.SearchRequest(
            query=query,
            k=k
        )
        
        response = stub.SearchDocuments(request_pb)
        
        # 转换搜索结果
        results = []
        for result in response.results:
            metadata = {k: v for k, v in result.metadata.items()}
            results.append({
                "content": result.content,
                "score": result.score,
                "metadata": metadata
            })
        
        return jsonify({
            "results": results,
            "success": response.success,
            "error_message": response.error_message
        })
    
    except Exception as e:
        logger.error(f"搜索文档失败: {e}")
        return jsonify({"error": str(e)}), 500

def main(host='0.0.0.0', port=8000, grpc_server='localhost:50051'):
    """启动代理服务器"""
    global grpc_channel, grpc_stub
    
    # 初始化gRPC连接
    try:
        grpc_channel = grpc.insecure_channel(grpc_server)
        grpc_stub = knowledge_service_pb2_grpc.KnowledgeServiceStub(grpc_channel)
        logger.info(f"已连接到gRPC服务器: {grpc_server}")
    except Exception as e:
        logger.error(f"连接gRPC服务器失败: {e}")
        sys.exit(1)
    
    # 启动Flask应用
    logger.info(f"启动gRPC-Web代理服务器 http://{host}:{port}")
    app.run(host=host, port=port, debug=False)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='gRPC-Web代理服务器')
    parser.add_argument('--host', default='0.0.0.0', help='监听地址')
    parser.add_argument('--port', type=int, default=8000, help='HTTP端口')
    parser.add_argument('--grpc-server', default='localhost:50051', help='gRPC服务器地址')
    
    args = parser.parse_args()
    
    main(host=args.host, port=args.port, grpc_server=args.grpc_server)