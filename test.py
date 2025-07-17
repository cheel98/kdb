import os
from pathlib import Path

print("测试Python环境和文档加载")
print("当前工作目录:", os.getcwd())

docs_path = Path("./docs")
print(f"docs目录是否存在: {docs_path.exists()}")

if docs_path.exists():
    md_files = list(docs_path.glob("**/*.md"))
    print(f"找到 {len(md_files)} 个markdown文件")
    
    for i, file_path in enumerate(md_files[:5]):  # 只显示前5个
        print(f"{i+1}. {file_path}")
        
    if len(md_files) > 5:
        print(f"... 还有 {len(md_files) - 5} 个文件")
else:
    print("docs目录不存在")

print("测试完成")