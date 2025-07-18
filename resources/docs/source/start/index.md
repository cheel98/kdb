# Zlattice建链

### 1、增加配置文件config.toml和genesis.json

将genesis.json.exmaple和config.toml.exmaple分别拷贝一份，将文件名改为genesis.json和config.toml

[![hyCMhF.png](https://z3.ax1x.com/2021/09/03/hyCMhF.png)](https://imgtu.com/i/hyCMhF)

### 2、创建saint账户，saint账户是专门作为见证账户

[![hyP0aV.png](https://z3.ax1x.com/2021/09/03/hyP0aV.png)](https://imgtu.com/i/hyP0aV)

[![hyi6Ff.png](https://z3.ax1x.com/2021/09/03/hyi6Ff.png)](https://imgtu.com/i/hyi6Ff)

[![hyFuAP.png](https://z3.ax1x.com/2021/09/03/hyFuAP.png)](https://imgtu.com/i/hyFuAP)

首次run saint后项目目录中生成saintkey文件

已有saintkey文件后，run saint会选择更新saintkey内容，也就是更新saint账户信息。

[![hyFyu9.png](https://z3.ax1x.com/2021/09/03/hyFyu9.png)](https://imgtu.com/i/hyFyu9)

### 3、更改genesis.json和config.toml中的配置

更改genesis.json文件中的"latcSaints"和"preacher"

[![hykBIP.png](https://z3.ax1x.com/2021/09/03/hykBIP.png)](https://imgtu.com/i/hykBIP)

更改config.toml中的Host项为自己的本机ip，其他项可不变。

注意：若本机ip非固定ip，每次启动链前，需要检查ip是否变化，作相应更改

[![hyA9zD.png](https://z3.ax1x.com/2021/09/03/hyA9zD.png)](https://imgtu.com/i/hyA9zD)

### 4、配置start命令，启动链

同saint命令配置，配置start

[![hyVIit.png](https://z3.ax1x.com/2021/09/03/hyVIit.png)](https://imgtu.com/i/hyVIit)

[![hyZI0J.png](https://z3.ax1x.com/2021/09/03/hyZI0J.png)](https://imgtu.com/i/hyZI0J)

go build配置完start，开始run start

[![hyeuAs.png](https://z3.ax1x.com/2021/09/03/hyeuAs.png)](https://imgtu.com/i/hyeuAs)

若进入console界面，且有出块信息，则链创建成功，如下：

[![hyeTKS.png](https://z3.ax1x.com/2021/09/03/hyeTKS.png)](https://imgtu.com/i/hyeTKS)

此时，本地链已经创建成功，但链上只有saint账户，若要测试交易，还可以创建普通账户，见操作5

### 5、创建普通账户

流程如图：

![hyurvV.png](https://z3.ax1x.com/2021/09/03/hyurvV.png)

[](https://imgtu.com/i/hyurvV)

[![hyucbF.png](https://z3.ax1x.com/2021/09/03/hyucbF.png)](https://imgtu.com/i/hyucbF)

[![hyuIv6.png](https://z3.ax1x.com/2021/09/03/hyuIv6.png)](https://imgtu.com/i/hyuIv6)

### 可选：使用CouchDB替代LevelDB存储链数据的方法
#### Step1: 完成上述配置后，在config.toml文件中**解除**下面四行的注释

`CouchDB_Enable = true # false 则使用默认leveldb，true则使用CouchDB`

`CouchDB_Address= "127.0.0.1:5984" #CouchDB连接URL`

`CouchDB_Username= "admin" #CouchDB用户名`

`CouchDB_Password= "password" #CouchDB密码`


#### Step2: 安装CouchDB
推荐使用docker一键部署，因为跨设备网络通讯存在不稳定性，强烈建议CouchDB和晶格链在**同一台机器**上部署！

`sudo  docker run -p 5984:5984 -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=password -d couchdb`

#### Step3: 创建数据库

docker下的CouchDB容器启动之后，浏览器打开 

127.0.0.1（根据情况调整，这个地址是docker宿主机地址）:5984/_utils/

![](http://home.ustc.edu.cn/~zyma/pics/1.jpg)

用户名+密码在docker启动时已经指定：admin/password

登录后，按照下图选择 Create Database

![](http://home.ustc.edu.cn/~zyma/pics/2.jpg)

输入数据库名latc，点击Create即可

![](http://home.ustc.edu.cn/~zyma/pics/3.jpg)

#### Step4: 启动晶格链
根据上文run start即可启动CouchDB模式下的晶格链。