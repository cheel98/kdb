# 安装和使用指南

## 快速开始

### 1. 基础演示（无需安装依赖）

如果您想快速查看知识库的基本功能，可以直接运行演示脚本：

```bash
# 使用虚拟环境中的Python（推荐）
.venv\Scripts\python.exe demo.py

# 或使用系统Python
python demo.py
```

这将展示：
- 📊 知识库统计信息（49个文档，198,859字符）
- 📁 完整的文档树结构
- 🔍 基础搜索功能演示

### 2. 完整功能安装

要使用完整的LangChain知识库功能，请按以下步骤操作：

#### 步骤1：激活虚拟环境

```bash
# Windows
.venv\Scripts\activate

# 或直接使用虚拟环境中的pip
.venv\Scripts\pip.exe install -r requirements.txt
```

#### 步骤2：安装依赖包

```bash
pip install -r requirements.txt
```

主要依赖包：
- `langchain==0.1.0` - LangChain框架
- `langchain-community==0.0.10` - 社区扩展
- `langchain-openai==0.0.2` - OpenAI集成
- `chromadb==0.4.22` - 向量数据库
- `faiss-cpu==1.7.4` - Facebook AI相似性搜索
- `streamlit==1.29.0` - Web界面框架

#### 步骤3：配置API密钥

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，添加您的DashScope API密钥
echo "DASHSCOPE_API_KEY=your_actual_api_key_here" > .env
```

#### 步骤4：构建知识库

```bash
# 方法1：使用构建脚本
python build_knowledge_base.py

# 方法2：使用启动脚本（交互式）
python start.py
```

#### 步骤5：启动Web界面

```bash
# 启动Streamlit Web应用
streamlit run app.py

# 或使用启动脚本
python start.py
```

然后在浏览器中打开 http://localhost:8501

## 功能特性

### 🎯 核心功能

1. **智能文档加载**
   - 自动扫描docs目录下的所有Markdown文件
   - 支持递归目录结构
   - 自动提取文档元数据

2. **向量化存储**
   - 使用通义千问Embeddings进行文本向量化
   - FAISS本地向量数据库存储
   - 支持增量更新

3. **智能搜索**
   - 基于语义相似度的文档检索
   - 支持中文和英文查询
   - 返回相关度评分

4. **AI问答系统**
   - 基于检索增强生成(RAG)的问答
   - 上下文感知的回答生成
   - 提供答案来源文档

5. **Web交互界面**
   - 友好的Streamlit Web界面
   - 实时聊天功能
   - 文档搜索和浏览
   - 知识库管理功能

### 📊 当前知识库统计

- **文档总数**: 49个
- **总字符数**: 198,859
- **总行数**: 9,153
- **平均文档大小**: 4,058字符
- **最大文档**: source/api/account.md (1,077行)

### 📂 文档分布

- **API文档**: 13个文档 (source/api/)
- **合约相关**: 11个文档 (design/contractLC/, source/contract/)
- **共识机制**: 4个文档 (source/consensus/, problem/consensus/)
- **配置文档**: 2个文档 (source/configs/)
- **版本信息**: 3个文档 (source/version/)
- **其他功能**: 16个文档

## 使用示例

### 命令行使用

```python
from knowledge_base import KnowledgeBase

# 创建知识库实例
kb = KnowledgeBase()

# 加载向量存储
kb.load_vector_store()

# 搜索文档
results = kb.search_documents("API接口", k=5)

# 问答
response = kb.ask_question("如何获取账户余额？")
print(response['answer'])
```

### Web界面使用

1. 启动Web应用后，在侧边栏输入DashScope API密钥
2. 点击"构建/重建知识库"（首次使用）
3. 点击"加载知识库"
4. 在"智能问答"标签页中提问
5. 在"文档搜索"标签页中搜索关键词

## 故障排除

### 常见问题

1. **pip命令不可用**
   ```bash
   # 使用python -m pip代替
   python -m pip install -r requirements.txt
   
   # 或使用虚拟环境中的pip
   .venv\Scripts\pip.exe install -r requirements.txt
   ```

2. **DashScope API错误**
   - 检查API密钥是否正确
   - 确认账户有足够的额度
   - 检查网络连接

3. **向量存储加载失败**
   ```bash
   # 重新构建知识库
   python build_knowledge_base.py
   ```

4. **Streamlit启动失败**
   ```bash
   # 检查是否安装了streamlit
   pip install streamlit
   
   # 使用完整路径启动
   .venv\Scripts\streamlit.exe run app.py
   ```

### 性能优化

1. **减少向量维度**: 修改embedding模型配置
2. **调整分块大小**: 修改`chunk_size`参数
3. **限制检索数量**: 调整`k`参数
4. **使用本地模型**: 替换为本地embedding模型

## 扩展开发

### 添加新文档格式

```python
# 在build_knowledge_base.py中添加新的loader
from langchain.document_loaders import PDFLoader, WordLoader

# 支持PDF文件
pdf_loader = DirectoryLoader(
    str(self.docs_path),
    glob="**/*.pdf",
    loader_cls=PDFLoader
)
```

### 自定义向量数据库

```python
# 使用Chroma替代FAISS
from langchain.vectorstores import Chroma

vector_store = Chroma.from_documents(
    texts, 
    self.embeddings,
    persist_directory="./chroma_db"
)
```

### 集成其他LLM

```python
# 使用本地模型
from langchain.llms import LlamaCpp

llm = LlamaCpp(
    model_path="./models/llama-model.bin",
    temperature=0
)
```

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 支持

如有问题或建议，请提交Issue或Pull Request。