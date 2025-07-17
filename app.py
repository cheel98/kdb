import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
import dashscope

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
        
        # 检查向量存储是否存在
        vector_store_path = Path("./vector_store")
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

if __name__ == "__main__":
    main()