# 通义千问知识库系统配置指南

本文档详细说明如何配置和使用基于通义千问的本地知识库系统。

## 🚀 快速配置

### 1. 获取DashScope API密钥

1. 访问 [阿里云DashScope控制台](https://dashscope.console.aliyun.com/)
2. 注册/登录阿里云账号
3. 开通DashScope服务
4. 创建API密钥
5. 复制API密钥备用

### 2. 配置环境变量

创建 `.env` 文件：
```bash
cp .env.example .env
```

编辑 `.env` 文件，添加您的API密钥：
```
DASHSCOPE_API_KEY=your_actual_dashscope_api_key_here
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 测试配置

运行配置测试脚本：
```bash
python test_qwen.py
```

如果看到 "🎉 所有测试通过！" 说明配置正确。

## 📋 系统架构

### 核心组件

1. **文本嵌入模型**: `text-embedding-v1`
   - 用于将文档转换为向量表示
   - 支持中文和英文
   - 向量维度: 1536

2. **语言生成模型**: `qwen-turbo`
   - 用于智能问答
   - 支持上下文理解
   - 中文优化

3. **向量数据库**: FAISS
   - 本地存储
   - 快速相似度搜索
   - 支持增量更新

### 技术栈

- **LangChain**: 大语言模型应用框架
- **DashScope**: 阿里云通义千问API服务
- **FAISS**: Facebook AI相似度搜索库
- **Streamlit**: Web应用框架
- **Python**: 主要编程语言

## 🔧 使用方法

### 命令行使用

1. **构建知识库**:
   ```bash
   python build_knowledge_base.py
   ```

2. **测试知识库**:
   ```bash
   python knowledge_base.py
   ```

3. **启动管理工具**:
   ```bash
   python start.py
   ```

### Web界面使用

1. **启动Web应用**:
   ```bash
   streamlit run app.py
   ```

2. **访问界面**: 打开浏览器访问 http://localhost:8501

3. **配置API密钥**: 在侧边栏输入DashScope API密钥

4. **构建知识库**: 点击"构建/重建知识库"按钮

5. **开始使用**: 在问答界面输入问题

## 📊 性能特点

### 优势

- ✅ **中文优化**: 通义千问对中文理解更准确
- ✅ **成本效益**: 相比GPT-4更经济实惠
- ✅ **响应速度**: 国内访问速度更快
- ✅ **合规性**: 符合国内数据安全要求
- ✅ **稳定性**: 阿里云基础设施保障

### 性能指标

- **嵌入速度**: ~100 tokens/秒
- **问答延迟**: 通常 < 3秒
- **向量维度**: 1536维
- **支持语言**: 中文、英文等多语言

## 🛠️ 高级配置

### 模型参数调优

在代码中可以调整以下参数：

```python
# 语言模型参数
llm = Tongyi(
    temperature=0,          # 控制随机性 (0-1)
    top_p=0.8,             # 核采样参数
    max_tokens=2000        # 最大输出长度
)

# 嵌入模型参数
embeddings = DashScopeEmbeddings(
    model="text-embedding-v1",
    chunk_size=25          # 批处理大小
)
```

### 文档分块策略

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,       # 块大小
    chunk_overlap=200,     # 重叠长度
    length_function=len,   # 长度计算函数
)
```

### 检索参数优化

```python
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}  # 返回最相关的4个文档块
)
```

## 🔍 故障排除

### 常见问题

1. **API密钥错误**
   ```
   错误: Invalid API key
   解决: 检查DASHSCOPE_API_KEY是否正确设置
   ```

2. **网络连接问题**
   ```
   错误: Connection timeout
   解决: 检查网络连接，确保可以访问阿里云服务
   ```

3. **依赖包问题**
   ```
   错误: ModuleNotFoundError
   解决: 重新安装依赖 pip install -r requirements.txt
   ```

4. **内存不足**
   ```
   错误: Out of memory
   解决: 减少chunk_size或增加系统内存
   ```

### 调试技巧

1. **启用详细日志**:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **测试API连接**:
   ```bash
   python test_qwen.py
   ```

3. **检查向量数据库**:
   ```python
   # 查看向量数据库信息
   vector_store = FAISS.load_local("./vector_store", embeddings)
   print(f"文档数量: {vector_store.index.ntotal}")
   ```

## 📈 扩展开发

### 添加新功能

1. **自定义提示模板**:
   ```python
   custom_prompt = PromptTemplate(
       input_variables=["context", "question"],
       template="根据以下信息回答问题：\n{context}\n\n问题：{question}\n答案："
   )
   ```

2. **集成其他数据源**:
   ```python
   # 支持PDF文档
   from langchain.document_loaders import PyPDFLoader
   
   # 支持网页内容
   from langchain.document_loaders import WebBaseLoader
   ```

3. **添加缓存机制**:
   ```python
   from langchain.cache import InMemoryCache
   import langchain
   langchain.llm_cache = InMemoryCache()
   ```

### 性能优化

1. **批量处理**: 一次处理多个文档
2. **异步调用**: 使用异步API提高并发性
3. **缓存策略**: 缓存常用查询结果
4. **索引优化**: 定期重建向量索引

## 📝 最佳实践

1. **文档组织**: 保持清晰的目录结构
2. **定期更新**: 及时更新知识库内容
3. **监控使用**: 关注API调用量和成本
4. **备份数据**: 定期备份向量数据库
5. **安全管理**: 妥善保管API密钥

## 📞 技术支持

- **DashScope文档**: https://help.aliyun.com/zh/dashscope/
- **LangChain文档**: https://python.langchain.com/
- **问题反馈**: 通过GitHub Issues提交问题

---

*最后更新: 2024年*