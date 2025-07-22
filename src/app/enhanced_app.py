import streamlit as st
import os
import sys
from pathlib import Path
import io
from docx import Document
import PyPDF2
import pdfplumber
import json
from datetime import datetime

# 添加项目根目录到Python路径以导入config模块
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 添加src目录到Python路径以导入其他模块
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config.config import get_config, reload_config
import dashscope
# 修改为绝对导入路径
from src.app.enhanced_knowledge_base import EnhancedKnowledgeBase
from src.app.build_knowledge_base import KnowledgeBaseBuilder
from src.app.feedback_system import FeedbackRecord

# 页面配置
st.set_page_config(
    page_title="智能知识库 - 反馈学习版",
    page_icon="🧠",
    layout="wide"
)

# 初始化session state
if 'enhanced_kb' not in st.session_state:
    st.session_state.enhanced_kb = None
if 'kb_loaded' not in st.session_state:
    st.session_state.kb_loaded = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'feedback_mode' not in st.session_state:
    st.session_state.feedback_mode = True
if 'show_feedback_panel' not in st.session_state:
    st.session_state.show_feedback_panel = {}

def load_enhanced_knowledge_base():
    """加载增强知识库"""
    try:
        if st.session_state.enhanced_kb is None:
            st.session_state.enhanced_kb = EnhancedKnowledgeBase()
        
        if not st.session_state.kb_loaded:
            st.session_state.enhanced_kb.load_vector_store()
            st.session_state.kb_loaded = True
        
        return True
    except Exception as e:
        st.error(f"加载增强知识库失败: {str(e)}")
        return False

def build_knowledge_base():
    """构建知识库"""
    try:
        with st.spinner("正在构建知识库，请稍候..."):
            builder = KnowledgeBaseBuilder()
            builder.build()
        st.success("知识库构建完成！")
        # 重置加载状态
        st.session_state.kb_loaded = False
        return True
    except Exception as e:
        st.error(f"构建知识库失败: {str(e)}")
        return False

def render_feedback_panel(chat_index, chat_item):
    """渲染反馈面板"""
    feedback_key = f"feedback_{chat_index}"
    
    if feedback_key not in st.session_state.show_feedback_panel:
        st.session_state.show_feedback_panel[feedback_key] = False
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
    
    with col1:
        if st.button("👍 满意", key=f"positive_{chat_index}"):
            collect_feedback(chat_item, "positive")
            st.success("感谢您的反馈！")
    
    with col2:
        if st.button("👎 不满意", key=f"negative_{chat_index}"):
            collect_feedback(chat_item, "negative")
            st.info("感谢反馈，我们会持续改进")
    
    with col3:
        if st.button("✏️ 纠正", key=f"correct_{chat_index}"):
            st.session_state.show_feedback_panel[feedback_key] = True
    
    with col4:
        if st.button("📊 查看反馈历史", key=f"history_{chat_index}"):
            show_feedback_history(chat_item["question"])
    
    # 显示纠正面板
    if st.session_state.show_feedback_panel[feedback_key]:
        with st.expander("✏️ 提供正确答案", expanded=True):
            corrected_answer = st.text_area(
                "请提供正确的答案：",
                height=150,
                key=f"corrected_answer_{chat_index}"
            )
            
            feedback_text = st.text_input(
                "补充说明（可选）：",
                key=f"feedback_text_{chat_index}"
            )
            
            col_submit, col_cancel = st.columns([1, 1])
            
            with col_submit:
                if st.button("提交纠正", key=f"submit_correction_{chat_index}"):
                    if corrected_answer.strip():
                        collect_feedback(
                            chat_item, 
                            "corrected", 
                            corrected_answer=corrected_answer,
                            feedback_text=feedback_text
                        )
                        st.success("纠正已提交，谢谢您的贡献！")
                        st.session_state.show_feedback_panel[feedback_key] = False
                        st.rerun()
                    else:
                        st.warning("请提供纠正后的答案")
            
            with col_cancel:
                if st.button("取消", key=f"cancel_correction_{chat_index}"):
                    st.session_state.show_feedback_panel[feedback_key] = False
                    st.rerun()

def collect_feedback(chat_item, feedback_type, corrected_answer=None, feedback_text=None):
    """收集用户反馈"""
    try:
        if st.session_state.enhanced_kb:
            feedback_id = st.session_state.enhanced_kb.collect_user_feedback(
                question=chat_item["question"],
                original_answer=chat_item.get("original_answer", chat_item["answer"]),
                feedback_type=feedback_type,
                corrected_answer=corrected_answer,
                feedback_text=feedback_text,
                source_documents=chat_item.get("sources", [])
            )
            
            # 更新聊天历史中的反馈信息
            for chat in st.session_state.chat_history:
                if chat["question"] == chat_item["question"]:
                    if "feedback_given" not in chat:
                        chat["feedback_given"] = []
                    chat["feedback_given"].append({
                        "type": feedback_type,
                        "timestamp": datetime.now().isoformat(),
                        "feedback_id": feedback_id
                    })
                    break
            
    except Exception as e:
        st.error(f"提交反馈失败: {str(e)}")

def show_feedback_history(question):
    """显示问题的反馈历史"""
    try:
        if st.session_state.enhanced_kb:
            history = st.session_state.enhanced_kb.get_feedback_history(question)
            
            if history:
                st.subheader("📊 反馈历史")
                for i, record in enumerate(history):
                    with st.expander(f"反馈 {i+1} - {record.user_feedback} ({record.timestamp[:19]})"):
                        st.write(f"**反馈类型**: {record.user_feedback}")
                        if record.feedback_text:
                            st.write(f"**说明**: {record.feedback_text}")
                        if record.corrected_answer:
                            st.write(f"**纠正答案**: {record.corrected_answer}")
            else:
                st.info("暂无反馈历史")
    except Exception as e:
        st.error(f"获取反馈历史失败: {str(e)}")

def render_answer_with_feedback_info(result):
    """渲染带有反馈信息的答案"""
    # 获取答案内容，兼容不同的键名
    answer = result.get('answer') or result.get('final_answer', '')
    original_answer = result.get('original_answer', answer)
    
    # 显示答案
    if result.get("feedback_info", {}).get("is_improved", False):
        st.success("🎯 这是基于用户反馈优化的答案")
        feedback_info = result["feedback_info"]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("置信度", f"{feedback_info['confidence_score']:.1%}")
        with col2:
            st.metric("反馈次数", feedback_info['feedback_count'])
        with col3:
            st.metric("最后更新", feedback_info.get('last_updated', 'N/A')[:10])
        
        # 显示原始答案对比
        with st.expander("📋 查看原始答案对比"):
            col_orig, col_improved = st.columns(2)
            with col_orig:
                st.subheader("原始答案")
                st.write(original_answer)
            with col_improved:
                st.subheader("优化答案")
                st.write(answer)
    
    st.markdown(f"**回答：**\n{answer}")
    
    # 显示相似问题建议
    similar_questions = result.get("feedback_info", {}).get("similar_questions", [])
    if similar_questions:
        with st.expander("🔗 相关问题参考"):
            for sq in similar_questions:
                st.write(f"**问题**: {sq['question']} (相似度: {sq['similarity']:.1%})")
                st.write(f"**参考答案**: {sq['improved_answer'][:200]}...")
                st.divider()

def extract_text_from_file(uploaded_file):
    """从不同格式的文件中提取文本内容"""
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    try:
        if file_extension in ['md', 'txt']:
            return uploaded_file.read().decode('utf-8')
        elif file_extension == 'pdf':
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        elif file_extension in ['doc', 'docx']:
            doc = Document(io.BytesIO(uploaded_file.read()))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        else:
            raise ValueError(f"不支持的文件格式: {file_extension}")
    except Exception as e:
        raise Exception(f"提取文本失败: {str(e)}")

def upload_documents_advanced(uploaded_files, config):
    """上传并处理多种格式的文档到docs目录"""
    try:
        docs_path = Path(config.document.docs_path)
        docs_path.mkdir(parents=True, exist_ok=True)
        
        for uploaded_file in uploaded_files:
            try:
                text_content = extract_text_from_file(uploaded_file)
                base_name = uploaded_file.name.rsplit('.', 1)[0]
                md_filename = f"{base_name}.md"
                file_path = docs_path / md_filename
                
                if file_path.exists():
                    st.warning(f"文件 {md_filename} 已存在，将被覆盖")
                
                markdown_content = f"# {base_name}\n\n{text_content}"
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                
                st.success(f"✅ {uploaded_file.name} 已转换并保存为 {md_filename}")
                
            except Exception as e:
                st.error(f"处理文件 {uploaded_file.name} 时发生错误: {str(e)}")
                continue
        
        return True
        
    except Exception as e:
        st.error(f"上传文档时发生错误: {str(e)}")
        return False

def main():
    st.title("🧠 智能知识库系统 - 反馈学习版")
    st.markdown("基于LangChain和通义千问构建的智能文档知识库，支持用户反馈学习")
    
    # 获取配置
    try:
        config = get_config()
    except Exception as e:
        st.error(f"配置加载失败: {e}")
        return
    
    # 侧边栏
    with st.sidebar:
        st.header("⚙️ 系统设置")
        
        # 显示当前配置信息
        with st.expander("📋 当前配置", expanded=False):
            st.text(f"模型: {config.dashscope.model_name}")
            st.text(f"嵌入模型: {config.dashscope.embedding_model}")
            st.text(f"文档路径: {config.document.docs_path}")
            st.text(f"向量存储: {config.vector_store.store_path}")
        
        # API密钥设置
        api_key = st.text_input(
            "DashScope API Key", 
            value=config.dashscope.api_key,
            type="password",
            help="请输入您的DashScope API密钥"
        )
        
        if api_key and api_key != config.dashscope.api_key:
            os.environ['DASHSCOPE_API_KEY'] = api_key
            dashscope.api_key = api_key
            reload_config()
            config = get_config()
        
        st.divider()
        
        # 反馈学习设置
        st.header("🎯 反馈学习设置")
        
        feedback_enabled = st.checkbox(
            "启用反馈学习", 
            value=st.session_state.feedback_mode,
            help="启用后系统会根据用户反馈优化答案"
        )
        st.session_state.feedback_mode = feedback_enabled
        
        confidence_threshold = st.slider(
            "置信度阈值", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.7, 
            step=0.1,
            help="使用优化答案的最低置信度"
        )
        
        similarity_threshold = st.slider(
            "相似度阈值", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.8, 
            step=0.1,
            help="相似问题匹配的最低相似度"
        )
        
        # 更新设置
        if st.session_state.enhanced_kb:
            st.session_state.enhanced_kb.update_feedback_settings(
                enable_feedback=feedback_enabled,
                confidence_threshold=confidence_threshold,
                similarity_threshold=similarity_threshold
            )
        
        st.divider()
        
        # 知识库管理
        st.header("📖 知识库管理")
        
        vector_store_path = Path(config.vector_store.store_path)
        vector_store_exists = vector_store_path.exists()
        
        if vector_store_exists:
            st.success("✅ 知识库已存在")
        else:
            st.warning("⚠️ 知识库不存在")
        
        if st.button("🔨 构建/重建知识库", disabled=not api_key):
            if build_knowledge_base():
                st.rerun()
        
        if st.button("📥 加载知识库", disabled=not (api_key and vector_store_exists)):
            if load_enhanced_knowledge_base():
                st.success("增强知识库加载成功！")
        
        st.divider()
        
        # 反馈统计
        if st.session_state.kb_loaded and st.session_state.enhanced_kb:
            st.header("📊 反馈统计")
            try:
                stats = st.session_state.enhanced_kb.get_feedback_stats()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("总反馈数", stats['total_feedback'])
                    st.metric("正面反馈", stats['positive_feedback'])
                with col2:
                    st.metric("满意度", f"{stats['satisfaction_rate']:.1f}%")
                    st.metric("改进答案", stats['improved_answers'])
                
                # 导出数据
                if st.button("📤 导出学习数据"):
                    export_result = st.session_state.enhanced_kb.export_learning_data()
                    if export_result['feedback_data']:
                        st.success(f"数据已导出: {export_result['export_timestamp']}")
                    else:
                        st.error("导出失败")
                        
            except Exception as e:
                st.error(f"获取统计信息失败: {str(e)}")
        
        # 文档上传功能
        st.header("📤 文档上传")
        uploaded_files = st.file_uploader(
            "选择要上传的文档文件",
            type=['md', 'txt', 'doc', 'docx', 'pdf'],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            if st.button("📤 上传文档"):
                if upload_documents_advanced(uploaded_files, config):
                    st.success("文档上传成功！")
    
    # 主界面
    if not api_key:
        st.warning("请在侧边栏输入DashScope API密钥")
        return
    
    if not st.session_state.kb_loaded:
        st.info("请先在侧边栏加载知识库")
        return
    
    # 创建标签页
    tab1, tab2, tab3 = st.tabs(["💬 智能问答", "🔍 文档搜索", "📈 学习分析"])
    
    with tab1:
        st.header("智能问答")
        
        # 问题输入
        question = st.text_input(
            "请输入您的问题：",
            placeholder="例如：什么是人工智能？",
            key="question_input"
        )
        
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            ask_button = st.button("🤔 提问", type="primary")
        with col2:
            clear_button = st.button("🗑️ 清空历史")
        
        if clear_button:
            st.session_state.chat_history = []
            st.rerun()
        
        if ask_button and question:
            with st.spinner("正在思考中..."):
                try:
                    result = st.session_state.enhanced_kb.ask_question_with_feedback(
                        question, use_feedback=st.session_state.feedback_mode
                    )
                    
                    # 添加到聊天历史
                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": result["final_answer"],
                        "original_answer": result["original_answer"],
                        "sources": result["source_documents"],
                        "feedback_info": result["feedback_info"],
                        "timestamp": datetime.now().isoformat()
                    })
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"回答问题时发生错误: {str(e)}")
        
        # 显示聊天历史
        for i, chat in enumerate(reversed(st.session_state.chat_history)):
            with st.expander(f"Q: {chat['question']}", expanded=(i==0)):
                # 显示答案和反馈信息
                render_answer_with_feedback_info(chat)
                
                # 显示来源文档
                if chat['sources']:
                    st.markdown("**参考文档：**")
                    for j, source in enumerate(chat['sources']):
                        st.markdown(f"{j+1}. 📄 {source['source']}")
                
                st.divider()
                
                # 反馈面板
                if st.session_state.feedback_mode:
                    st.markdown("**📝 请为这个回答提供反馈：**")
                    render_feedback_panel(len(st.session_state.chat_history) - 1 - i, chat)
    
    with tab2:
        st.header("文档搜索")
        
        search_query = st.text_input(
            "请输入搜索关键词：",
            placeholder="例如：智能合约",
            key="search_input"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            k = st.slider("返回结果数量", min_value=1, max_value=10, value=5)
        with col2:
            search_button = st.button("🔍 搜索", type="primary")
        
        if search_button and search_query:
            with st.spinner("正在搜索..."):
                try:
                    results = st.session_state.enhanced_kb.search_with_feedback_context(search_query, k=k)
                    
                    if results:
                        st.success(f"找到 {len(results)} 个相关文档")
                        
                        for i, result in enumerate(results):
                            feedback_context = result.get('feedback_context', {})
                            title = f"📄 {result['metadata'].get('source', '未知文档')} (相似度: {result['similarity_score']:.3f})"
                            
                            if feedback_context.get('has_similar_feedback'):
                                title += " 🎯"
                            
                            with st.expander(title):
                                st.markdown("**内容：**")
                                st.text(result['content'])
                                
                                if feedback_context.get('has_similar_feedback'):
                                    st.info(f"💡 发现 {feedback_context['similar_questions_count']} 个相似问题的反馈")
                                
                                st.markdown("**元数据：**")
                                st.json(result['metadata'])
                    else:
                        st.warning("没有找到相关文档")
                        
                except Exception as e:
                    st.error(f"搜索时发生错误: {str(e)}")
    
    with tab3:
        st.header("学习分析")
        
        if st.session_state.enhanced_kb:
            try:
                enhanced_stats = st.session_state.enhanced_kb.get_enhanced_stats()
                
                # 知识库统计
                st.subheader("📚 知识库统计")
                kb_stats = enhanced_stats['knowledge_base']
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("文档数量", kb_stats.get('document_count', 0))
                with col2:
                    st.metric("状态", kb_stats.get('status', '未知'))
                
                # 反馈系统统计
                st.subheader("🎯 反馈学习统计")
                feedback_stats = enhanced_stats['feedback_system']
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("总反馈", feedback_stats['total_feedback'])
                with col2:
                    st.metric("正面反馈", feedback_stats['positive_feedback'])
                with col3:
                    st.metric("负面反馈", feedback_stats['negative_feedback'])
                with col4:
                    st.metric("纠正反馈", feedback_stats['corrected_feedback'])
                
                # 满意度图表
                if feedback_stats['total_feedback'] > 0:
                    st.subheader("📊 用户满意度")
                    satisfaction_rate = feedback_stats['satisfaction_rate']
                    
                    # 创建简单的进度条显示
                    st.progress(satisfaction_rate / 100)
                    st.write(f"满意度: {satisfaction_rate:.1f}%")
                
                # 系统配置
                st.subheader("⚙️ 系统配置")
                system_config = enhanced_stats['system_config']
                st.json(system_config)
                
            except Exception as e:
                st.error(f"获取统计信息失败: {str(e)}")
        else:
            st.info("请先加载知识库")

if __name__ == "__main__":
    main()