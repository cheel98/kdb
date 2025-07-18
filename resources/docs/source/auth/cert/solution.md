# 解决方案

## 1. 获取对等节点的证书

a. 通过[latc_peers](../../api/netApi#latc_peers)接口获取其他对等节点的信息；

b. 获取对等节点的CertSerialNumber字段信息；

c. 通过[latc_getCert](../../api/nodeCertApi#apiGetCert)结构获取证书信息。

## 2. 加入通道（子链）中，成为见证节点

### 方法1，不通过合约

a. 向通道的共识节点申请加入（业务层）, 共识节点根据申请者信息（公钥，链id）签发证书[latc_publishCert](../../api/nodeCertApi#latc_publishCert);

b. 节点调用共识节点接口获取证书 [latc_getCert](../../api/nodeCertApi#apiGetCert)结构获取证书信息;

c. 将节点证书以pem格式创建在 `configDir`/child/`chainId` 目录下;

d. 调用加入 [cbyc_selfJoinChain](../../api/cbyc#cbyc-selfjoinchain) 。

### 方法2，通过合约

a. 先为节点颁发证书，可以通过链上或链下的方式;

> 通过链下的方式，在发起加入通道提案时必须指定颁发证书的节点的inode，否则引发两个问题
> 1. 有可能会因同步不到证书而建链失败（新节点与颁发证书的节点未连接）
> 2. 建链过程会拉长，新节点需要向每个邻近节点请求证书

b. 通过以链建链合约申请加入通道，具体方法参考 [加入链合约](../../chainbychain/chainbychain#加入链);