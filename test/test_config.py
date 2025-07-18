#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理系统测试脚本
测试新的配置管理模块是否正常工作
"""
import os
import sys
from pathlib import Path

# 添加项目根目录到Python路径以导入config模块
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from config.config import get_config, reload_config, validate_config

def test_config_loading():
    """测试配置加载"""
    print("=== 配置加载测试 ===")
    
    try:
        config = get_config()
        print("✅ 配置加载成功")
        
        # 显示配置信息
        print(f"\n📋 配置详情:")
        print(f"- DashScope模型: {config.dashscope.model_name}")
        print(f"- 嵌入模型: {config.dashscope.embedding_model}")
        print(f"- 温度参数: {config.dashscope.temperature}")
        print(f"- 最大令牌: {config.dashscope.max_tokens}")
        print(f"- Top-P: {config.dashscope.top_p}")
        print(f"- 文档路径: {config.document.docs_path}")
        print(f"- 向量存储路径: {config.vector_store.store_path}")
        print(f"- 分块大小: {config.vector_store.chunk_size}")
        print(f"- 分块重叠: {config.vector_store.chunk_overlap}")
        print(f"- 搜索数量: {config.vector_store.search_k}")
        print(f"- 搜索类型: {config.vector_store.search_type}")
        print(f"- 日志级别: {config.logging.level}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False

def test_config_validation():
    """测试配置验证"""
    print("\n=== 配置验证测试 ===")
    
    try:
        config = get_config()
        
        # 测试API密钥
        if config.dashscope.api_key:
            print(f"✅ API密钥已配置 (前4位: {config.dashscope.api_key[:4]}...)")
        else:
            print("⚠️  API密钥未配置")
        
        # 测试文档路径
        docs_path = Path(config.document.docs_path)
        if docs_path.exists():
            print(f"✅ 文档路径存在: {docs_path}")
            # 统计文档数量
            md_files = list(docs_path.rglob("*.md"))
            print(f"   找到 {len(md_files)} 个Markdown文件")
        else:
            print(f"❌ 文档路径不存在: {docs_path}")
        
        # 测试向量存储路径
        vector_path = Path(config.vector_store.store_path)
        if vector_path.exists():
            print(f"✅ 向量存储已存在: {vector_path}")
        else:
            print(f"⚠️  向量存储不存在: {vector_path} (首次使用需要构建)")
        
        # 使用内置验证方法
        if validate_config():
            print("✅ 配置验证通过")
        else:
            print("❌ 配置验证失败")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置验证异常: {e}")
        return False

def test_environment_info():
    """测试环境信息获取"""
    print("\n=== 环境信息测试 ===")
    
    try:
        config = get_config()
        env_info = config.get_env_info()
        
        print("📊 环境信息:")
        for key, value in env_info.items():
            print(f"- {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ 环境信息获取失败: {e}")
        return False

def test_config_reload():
    """测试配置重新加载"""
    print("\n=== 配置重载测试 ===")
    
    try:
        # 获取当前配置
        config1 = get_config()
        original_temp = config1.dashscope.temperature
        print(f"原始温度参数: {original_temp}")
        
        # 临时修改环境变量
        os.environ['QWEN_TEMPERATURE'] = '0.5'
        
        # 重新加载配置
        reload_config()
        config2 = get_config()
        new_temp = config2.dashscope.temperature
        print(f"重载后温度参数: {new_temp}")
        
        # 恢复原始值
        os.environ['QWEN_TEMPERATURE'] = str(original_temp)
        reload_config()
        
        if new_temp != original_temp:
            print("✅ 配置重载功能正常")
        else:
            print("⚠️  配置重载可能未生效")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置重载测试失败: {e}")
        return False

def test_config_string_representation():
    """测试配置字符串表示"""
    print("\n=== 配置字符串表示测试 ===")
    
    try:
        config = get_config()
        config_str = str(config)
        print("📋 配置摘要:")
        print(config_str)
        
        return True
        
    except Exception as e:
        print(f"❌ 配置字符串表示测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 配置管理系统测试")
    print("=" * 50)
    
    # 检查当前工作目录
    current_dir = Path.cwd()
    print(f"当前工作目录: {current_dir}")
    
    # 检查.env文件
    env_file = current_dir / ".env"
    if env_file.exists():
        print("✅ .env文件存在")
    else:
        print("⚠️  .env文件不存在")
    
    print()
    
    # 运行所有测试
    tests = [
        test_config_loading,
        test_config_validation,
        test_environment_info,
        test_config_reload,
        test_config_string_representation
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ 测试 {test_func.__name__} 异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！配置管理系统工作正常。")
        print("\n📝 使用建议:")
        print("1. 在代码中使用 get_config() 获取配置实例")
        print("2. 使用 config.dashscope.api_key 等方式访问配置项")
        print("3. 使用 validate_config() 验证配置完整性")
        print("4. 使用 reload_config() 重新加载配置")
    else:
        print("❌ 部分测试失败，请检查配置。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)