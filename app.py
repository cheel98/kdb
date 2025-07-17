import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
import dashscope
import tempfile
import shutil

from knowledge_base import KnowledgeBase
from build_knowledge_base import KnowledgeBaseBuilder

# 加载环境变量
load_dotenv()

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

def save_uploaded_files(uploaded_files):
    """保存上传的文件到docs目录"""
    docs_path = Path("./docs/uploaded")
    docs_path.mkdir(parents=True, exist_ok=True)
    
    saved_files = []
    for uploaded_file in uploaded_files:
        # 保存文件
        file_path = docs_path / uploaded_file.name
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_files.append(str(file_path))
    
    return saved_files

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
    st.markdown("基于LangChain构建的本地文档知识库")
    
    # 侧边栏
    with st.sidebar:
        st.header("⚙️ 系统设置")
        
        # API密钥设置
        api_key = st.text_input(
            "DashScope API Key", 
            value=os.getenv('DASHSCOPE_API_KEY', ''),
            type="password",
            help="请输入您的DashScope API密钥"
        )
        
        if api_key:
            os.environ['DASHSCOPE_API_KEY'] = api_key
            dashscope.api_key = api_key
        
        st.divider()
        
        # 知识库管理
        st.header("📖 知识库管理")
        
        # 文件上传功能
        st.subheader("📁 上传文档")
        uploaded_files = st.file_uploader(
            "选择要上传的文档文件",
            type=['txt', 'md', 'pdf', 'docx', 'doc'],
            accept_multiple_files=True,
            help="支持的文件格式：TXT, MD, PDF, DOCX, DOC"
        )
        
        if uploaded_files:
            st.write(f"已选择 {len(uploaded_files)} 个文件：")
            for file in uploaded_files:
                st.write(f"- {file.name} ({file.size} bytes)")
            
            if st.button("💾 保存上传的文件", type="primary"):
                try:
                    saved_files = save_uploaded_files(uploaded_files)
                    st.success(f"成功保存 {len(saved_files)} 个文件到 docs/uploaded/ 目录")
                    for file_path in saved_files:
                        st.write(f"✅ {file_path}")
                    st.info("文件已保存，请点击下方'构建/重建知识库'按钮来更新知识库")
                except Exception as e:
                    st.error(f"保存文件失败: {str(e)}")
        
        st.divider()
        
        # 检查向量存储是否存在
        vector_store_path = Path("./vector_store")
        vector_store_exists = vector_store_path.exists()
        
        if vector_store_exists:
            st.success("✅ 知识库已存在")
        else:
            st.warning("⚠️ 知识库不存在")
        
        # 显示docs目录中的文件
        docs_path = Path("./docs")
        if docs_path.exists():
            with st.expander("📂 查看文档目录"):
                for file_path in docs_path.rglob("*"):
                    if file_path.is_file():
                        relative_path = file_path.relative_to(docs_path)
                        st.write(f"📄 {relative_path}")
        
        # 构建知识库按钮
        if st.button("🔨 构建/重建知识库", disabled=not api_key):
            if build_knowledge_base():
                st.rerun()
        
        # 加载知识库按钮
        if st.button("📥 加载知识库", disabled=not (api_key and vector_store_exists)):
            if load_knowledge_base():
                st.success("知识库加载成功！")
        
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
    
    # 创建三个标签页
    tab1, tab2, tab3 = st.tabs(["💬 智能问答", "🔍 文档搜索", "📁 文件管理"])
    
    with tab1:
        st.header("智能问答")
        
        # 聊天历史
        chat_container = st.container()
        
        # 问题输入
        question = st.text_input(
            "请输入您的问题：",
            placeholder="例如：什么是共识算法？",
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
                            with st.expander(f"查看内容片段 {j+1}"):
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
    
    with tab3:
        st.header("文件管理")
        
        # 显示上传目录中的文件
        uploaded_docs_path = Path("./docs/uploaded")
        if uploaded_docs_path.exists():
            uploaded_files = list(uploaded_docs_path.rglob("*"))
            uploaded_files = [f for f in uploaded_files if f.is_file()]
            
            if uploaded_files:
                st.subheader(f"📂 已上传的文件 ({len(uploaded_files)} 个)")
                
                # 创建文件列表
                for file_path in uploaded_files:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        file_size = file_path.stat().st_size
                        file_size_mb = file_size / (1024 * 1024)
                        st.write(f"📄 {file_path.name} ({file_size_mb:.2f} MB)")
                    
                    with col2:
                        # 下载按钮
                        with open(file_path, "rb") as file:
                            st.download_button(
                                label="⬇️ 下载",
                                data=file.read(),
                                file_name=file_path.name,
                                key=f"download_{file_path.name}"
                            )
                    
                    with col3:
                        # 删除按钮
                        if st.button("🗑️ 删除", key=f"delete_{file_path.name}"):
                            try:
                                file_path.unlink()
                                st.success(f"已删除文件: {file_path.name}")
                                st.rerun()
                            except Exception as e:
                                st.error(f"删除文件失败: {str(e)}")
                
                st.divider()
                
                # 批量操作
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("🗑️ 清空所有上传文件", type="secondary"):
                        try:
                            for file_path in uploaded_files:
                                file_path.unlink()
                            st.success("已清空所有上传文件")
                            st.rerun()
                        except Exception as e:
                            st.error(f"清空文件失败: {str(e)}")
                
                with col2:
                    if st.button("🔄 重新构建知识库", type="primary"):
                        if build_knowledge_base():
                            st.success("知识库重新构建完成！")
                            st.rerun()
            else:
                st.info("📭 暂无上传的文件")
        else:
            st.info("📭 上传目录不存在，请先上传一些文件")
        
        st.divider()
        
        # 显示所有文档目录的统计信息
        st.subheader("📊 文档统计")
        docs_path = Path("./docs")
        if docs_path.exists():
            total_files = 0
            total_size = 0
            file_types = {}
            
            for file_path in docs_path.rglob("*"):
                if file_path.is_file():
                    total_files += 1
                    total_size += file_path.stat().st_size
                    ext = file_path.suffix.lower()
                    file_types[ext] = file_types.get(ext, 0) + 1
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.metric("总文件数", total_files)
            with col2:
                st.metric("总大小", f"{total_size / (1024 * 1024):.2f} MB")
            with col3:
                st.metric("文件类型", len(file_types))
            
            if file_types:
                st.subheader("📈 文件类型分布")
                st.bar_chart(file_types)

if __name__ == "__main__":
    main()