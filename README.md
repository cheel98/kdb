# 本地知识库系统

基于LangChain构建的本地文档知识库，支持智能问答和文档搜索功能。

## 功能特性

- 📚 **文档加载**: 自动加载docs目录下的所有Markdown文档
- 🔍 **智能搜索**: 基于向量相似度的文档搜索
- 💬 **智能问答**: 基于检索增强生成(RAG)的问答系统
- 🌐 **Web界面**: 友好的Streamlit Web界面
- 💾 **本地存储**: 向量数据库本地存储，无需外部依赖

## 项目结构

```
knowledgeDB/
├── docs/                    # 文档目录（知识源）
│   ├── cross/
│   ├── design/
│   ├── problem/
│   ├── public/
│   └── source/
├── vector_store/            # 向量存储目录（自动生成）
├── build_knowledge_base.py  # 知识库构建脚本
├── knowledge_base.py        # 知识库查询接口
├── app.py                   # Streamlit Web应用
├── requirements.txt         # 依赖包列表
├── .env.example            # 环境变量模板
└── README.md               # 说明文档
```

## 安装和配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制环境变量模板并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，添加您的DashScope API密钥：

```
DASHSCOPE_API_KEY=your_actual_api_key_here
```

## 使用方法

### 方法一：使用Web界面（推荐）

1. 启动Web应用：

```bash
streamlit run app.py
```

2. 在浏览器中打开显示的URL（通常是 http://localhost:8501）

3. 在侧边栏输入DashScope API密钥

4. 点击"构建/重建知识库"按钮构建向量数据库

5. 点击"加载知识库"按钮加载知识库

6. 使用"智能问答"或"文档搜索"功能

### 方法二：使用命令行

1. 构建知识库：

```bash
python build_knowledge_base.py
```

2. 测试知识库：

```bash
python knowledge_base.py
```

## 核心组件说明

### KnowledgeBaseBuilder

负责构建知识库的核心类：

- **文档加载**: 递归加载docs目录下的所有.md文件
- **文本分割**: 将长文档分割成适合向量化的小块
- **向量化**: 使用通义千问Embeddings将文本转换为向量
- **存储**: 将向量存储到本地FAISS数据库

### KnowledgeBase

提供知识库查询功能的核心类：

- **文档搜索**: 基于向量相似度搜索相关文档
- **智能问答**: 结合检索到的文档内容生成答案
- **统计信息**: 提供知识库的基本统计信息

### Streamlit Web应用

提供用户友好的Web界面：

- **知识库管理**: 构建、加载知识库
- **智能问答**: 交互式问答界面，支持聊天历史
- **文档搜索**: 关键词搜索，显示相关文档片段
- **系统设置**: API密钥配置，统计信息显示

## 技术栈

- **LangChain**: 大语言模型应用框架
- **通义千问**: 文本嵌入和语言模型
- **FAISS**: 向量相似度搜索
- **Streamlit**: Web应用框架
- **Python**: 主要编程语言

## 注意事项

1. **API密钥**: 需要有效的DashScope API密钥才能使用
2. **文档格式**: 目前只支持Markdown格式的文档
3. **中文支持**: 完全支持中文文档和查询
4. **存储空间**: 向量数据库会占用一定的磁盘空间
5. **网络连接**: 首次构建知识库时需要网络连接调用通义千问API

## 常见问题

### Q: 如何添加新文档？
A: 将新的Markdown文档放入docs目录，然后重新构建知识库。

### Q: 支持其他文档格式吗？
A: 目前只支持Markdown格式，可以通过修改代码支持其他格式。

### Q: 如何获取DashScope API密钥？
A: 访问阿里云DashScope控制台 https://dashscope.console.aliyun.com/ 注册并获取API密钥。

### Q: 支持其他语言模型吗？
A: 目前使用通义千问模型，可以通过修改代码支持其他兼容的模型。

### Q: 可以使用其他嵌入模型吗？
A: 可以，修改代码中的embeddings配置即可。

### Q: 如何提高搜索准确性？
A: 可以调整文本分割参数、增加检索文档数量、优化提示模板等。

## 扩展功能

- 支持更多文档格式（PDF、Word等）
- 添加文档更新检测和增量更新
- 集成更多向量数据库（Chroma、Pinecone等）
- 添加用户认证和权限管理
- 支持多语言文档

## 许可证

本项目采用MIT许可证。