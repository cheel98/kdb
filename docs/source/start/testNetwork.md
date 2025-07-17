# 一步构建晶格链测试网络
1. 下载最新的晶格链源码，你会得到如下目录结构的代码,这里只需要关注configs

   \- ...

   \- configs            # 配置文件目录,包含网络启动脚本

         - firstNetwork.sh # 网络启动脚本

         - config.yaml.example # 配置文件模板

         - genesis.json.example # 创世区块模板

   \- ...


2. 在执行脚本之前,请确保以下端口未被占用:
   \- 10331 (WebSocket 端口)
   \- 10332 (HTTP 端口) 
   \- 10333 (P2P 端口)

   你可以使用以下命令检查端口是否被占用:
   ```bash
   # Linux/Mac
   lsof -i:10331
   lsof -i:10332  
   lsof -i:10333
   
   如果这些端口被占用,你需要先关闭占用这些端口的程序。

3. 在configs目录下执行脚本
   ```
   ./firstNetwork.sh init
   ```


   如果你不清楚脚本的用法,可以执行:
   ```
   ./firstNetwork.sh help
   ```
4. 执行完init命令后,会提示你输入共识节点数量和观察者节点数量,输入完成后,脚本会自动构建网络,并启动网络。
