if __name__ == "__main__":
    # 测试配置
    try:
        print("配置加载测试...")
        test_config = Config()
        print("✅ 配置加载成功")
        print(test_config)
        
        print("\n配置验证测试...")
        if test_config.validate():
            print("✅ 配置验证通过")
        else:
            print("❌ 配置验证失败")
        
        print("\n环境信息:")
        env_info = test_config.get_env_info()
        for key, value in env_info.items():
            print(f"- {key}: {value}")
            
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")