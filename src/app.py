import streamlit as st
import os
import sys
from pathlib import Path
import io
from docx import Document
import PyPDF2
import pdfplumber

# 添加项目根目录到Python路径以导入config模块
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# 添加src目录到Python路径以导入其他模块
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from config.config import get_config, reload_config
import dashscope
from knowledge_base import KnowledgeBase
from build_knowledge_base import KnowledgeBaseBuilder

# 页面配置
st.set_page_config(
    page_title="本地知识库",
    page_icon="📚",
    layout="wide"
)

# 初始化session state
if 'kb' not in st.session_state:
    st.session_state.kb = None
if 'kb_loaded' not in st.session_state:
    st.session_state.kb_loaded = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def load_knowledge_base():
    """加载知识库"""
    try:
        if st.session_state.kb is None:
            st.session_state.kb = KnowledgeBase()
        
        if not st.session_state.kb_loaded:
            st.session_state.kb.load_vector_store()
            st.session_state.kb_loaded = True
        
        return True
    except Exception as e:
        st.error(f"加载知识库失败: {str(e)}")
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

def main():
    st.title("📚 本地知识库系统")
    st.markdown("基于LangChain和通义千问构建的本地文档知识库")
    
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
            st.text(f"分块大小: {config.vector_store.chunk_size}")
        
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
            # 重新加载配置
            reload_config()
            config = get_config()
        
        st.divider()
        
        # 知识库管理
        st.header("📖 知识库管理")
        
        # 检查向量存储是否存在
        vector_store_path = Path(config.vector_store.store_path)
        vector_store_exists = vector_store_path.exists()
        
        if vector_store_exists:
            st.success("✅ 知识库已存在")
        else:
            st.warning("⚠️ 知识库不存在")
        
        # 构建知识库按钮
        if st.button("🔨 构建/重建知识库", disabled=not api_key):
            if build_knowledge_base():
                st.rerun()
        
        # 加载知识库按钮
        if st.button("📥 加载知识库", disabled=not (api_key and vector_store_exists)):
            if load_knowledge_base():
                st.success("知识库加载成功！")
        
        st.divider()
        
        # 文档上传功能
        st.header("📤 文档上传")
        st.markdown("支持格式：MD, TXT, DOC, DOCX, PDF")
        
        # 文件上传区域
        uploaded_files = st.file_uploader(
            "选择要上传的文档文件",
            type=['md', 'txt', 'doc', 'docx', 'pdf'],
            accept_multiple_files=True,
            help="支持同时上传多个文件"
        )
        
        if uploaded_files:
            st.success(f"已选择 {len(uploaded_files)} 个文件")
            
            # 上传按钮
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("📤 上传文档", type="primary"):
                    upload_success = upload_documents_advanced(uploaded_files, config)
                    if upload_success:
                        st.success("文档上传成功！")
                        st.info("请点击重建知识库以包含新文档")
            
            with col2:
                if st.button("🔨 上传并重建"):
                    upload_success = upload_documents_advanced(uploaded_files, config)
                    if upload_success:
                        st.success("文档上传成功！")
                        if build_knowledge_base():
                            st.success("知识库重建完成！")
                            st.rerun()
        
        st.divider()
        
        # 文档管理区域
        with st.expander("📁 文档管理", expanded=False):
            docs_path = Path(config.document.docs_path)
            if docs_path.exists():
                doc_files = list(docs_path.rglob("*.md")) + list(docs_path.rglob("*.txt"))
                
                if doc_files:
                    st.write(f"当前知识库包含 {len(doc_files)} 个文档")
                    
                    # 创建文档列表
                    for doc_file in sorted(doc_files)[:5]:  # 只显示前5个
                        relative_path = doc_file.relative_to(docs_path)
                        file_size = doc_file.stat().st_size
                        
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.text(f"📄 {relative_path}")
                        with col2:
                            if st.button("🗑️", key=f"delete_{doc_file}", help="删除文档"):
                                try:
                                    doc_file.unlink()
                                    st.success(f"已删除 {relative_path}")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"删除失败: {str(e)}")
                    
                    if len(doc_files) > 5:
                        st.info(f"还有 {len(doc_files) - 5} 个文档...")
                else:
                    st.info("知识库中暂无文档")
            else:
                st.warning(f"文档目录不存在: {docs_path}")
        
        st.divider()
        
        # 知识库统计信息
        if st.session_state.kb_loaded and st.session_state.kb:
            st.header("📊 统计信息")
            stats = st.session_state.kb.get_stats()
            st.json(stats)
    
    # 主界面
    if not api_key:
        st.warning("请在侧边栏输入DashScope API密钥")
        return
    
    if not st.session_state.kb_loaded:
        st.info("请先在侧边栏加载知识库")
        return
    
    # 创建两个标签页
    tab1, tab2 = st.tabs(["💬 智能问答", "🔍 文档搜索"])
    
    with tab1:
        st.header("智能问答")
        
        # 聊天历史
        chat_container = st.container()
        
        # 问题输入
        question = st.text_input(
            "请输入您的问题：",
            placeholder="",
            key="question_input"
        )
        
        col1, col2 = st.columns([1, 4])
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
                    response = st.session_state.kb.ask_question(question)
                    
                    # 添加到聊天历史
                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": response["answer"],
                        "sources": response["source_documents"]
                    })
                    
                    # 清空输入框
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"回答问题时发生错误: {str(e)}")
        
        # 显示聊天历史
        with chat_container:
            for i, chat in enumerate(reversed(st.session_state.chat_history)):
                with st.expander(f"Q: {chat['question']}", expanded=(i==0)):
                    st.markdown(f"**回答：**\n{chat['answer']}")
                    
                    if chat['sources']:
                        st.markdown("**参考文档：**")
                        for j, source in enumerate(chat['sources']):
                            st.markdown(f"{j+1}. 📄 {source['source']}")
                            # 使用details而不是嵌套expander
                            with st.container():
                                if st.button(f"查看内容片段 {j+1}", key=f"source_{i}_{j}"):
                                    st.text(source['content'][:500] + "..." if len(source['content']) > 500 else source['content'])
    
    with tab2:
        st.header("文档搜索")
        
        # 搜索输入
        search_query = st.text_input(
            "请输入搜索关键词：",
            placeholder="例如：智能合约",
            key="search_input"
        )
        
        # 搜索参数
        col1, col2 = st.columns([1, 1])
        with col1:
            k = st.slider("返回结果数量", min_value=1, max_value=10, value=5)
        with col2:
            search_button = st.button("🔍 搜索", type="primary")
        
        if search_button and search_query:
            with st.spinner("正在搜索..."):
                try:
                    results = st.session_state.kb.search_documents(search_query, k=k)
                    
                    if results:
                        st.success(f"找到 {len(results)} 个相关文档")
                        
                        for i, result in enumerate(results):
                            with st.expander(f"📄 {result['metadata'].get('source', '未知文档')} (相似度: {result['similarity_score']:.3f})"):
                                st.markdown("**内容：**")
                                st.text(result['content'])
                                
                                st.markdown("**元数据：**")
                                st.json(result['metadata'])
                    else:
                        st.warning("没有找到相关文档")
                        
                except Exception as e:
                    st.error(f"搜索时发生错误: {str(e)}")

def extract_text_from_file(uploaded_file):
    """从不同格式的文件中提取文本内容"""
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    try:
        if file_extension in ['md', 'txt']:
            # 处理文本文件
            return uploaded_file.read().decode('utf-8')
        
        elif file_extension == 'pdf':
            # 处理PDF文件
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        
        elif file_extension in ['doc', 'docx']:
            # 处理Word文档
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
                # 提取文本内容
                text_content = extract_text_from_file(uploaded_file)
                
                # 生成markdown文件名
                base_name = uploaded_file.name.rsplit('.', 1)[0]
                md_filename = f"{base_name}.md"
                file_path = docs_path / md_filename
                
                # 检查文件是否已存在
                if file_path.exists():
                    st.warning(f"文件 {md_filename} 已存在，将被覆盖")
                
                # 创建markdown格式的内容
                markdown_content = f"# {base_name}\n\n{text_content}"
                
                # 写入文件
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

if __name__ == "__main__":
    main()