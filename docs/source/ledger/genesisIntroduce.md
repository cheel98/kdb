# 创世区块

```json
{
  "config": {
    "latcId": 1,
    "latcSaints": [
      "zltc_m7jktxWbNGj34e8UnREgkSotAaJPi6YvD"
    ],
    "observers" : [],
    "epoch": 30000,
    "noRecursion": false,
    "tokenless": false,
    "NoEmptyAnchor": true,
    "EmptyAnchorPeriodMul": 3,
    "period": 10,
    "GM": true,
    "isContractVote": true,
    "isDictatorship": true,
    "deployRule": 0,
    "chainByChainVote": 0,
    "proposalExpireTime": 1,
    "configModifyRule": 1,
    "contractPermission": false,
    "enableCert": true
  },
  "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "number": 0,
  "preacher": "zltc_m7jktxWbNGj34e8UnREgkSotAaJPi6YvD",
  "godAmount": 1000000000000000000000000000000,
  "timestamp": "0x5e5f1470",
  "initVersion": 3
}

```

|             |                      |               | 类型        | 可选值                        |
| ----------- |----------------------|---------------|-----------| ----------------------------- |
| config      | latcId               | 链ID           | int       |                               |
|             | latcSaints           | 共识节点          | []address |                               |
|             | observers           | 见证节点          | []address |                               |
|             | consensus            | 共识机制          | string    | PoA，Raft，PBFT（区分大小写） |
|             | noRecursion          | 合约递归调用        | bool      |                               |
|             | tokenless            | 无币链           | bool      |                               |
|             | period               | 出块间隔          | int       |                               |
|             | NoEmptyAnchor        | 不出空块          | bool      |                               |
|             | EmptyAnchorPeriodMul | 不出空块的间隔       | int       |                               |
|             | GM                   | 国密            | bool      |                               |
|             | isContractVote       | 合约生命周期        | bool      |                               |
|             | isDictatorship       | 生命周期盟主独裁      | bool      |                               |
|             | deployRule           | 合约部署规则        | int       | 0,1,2                         |
|             | contractPermission   | 合约内部管理        | bool      |                               |
|             | chainByChainVote     | 以链建链投票        | int       | 0,1,2                         |
|             | proposalExpireTime   | 提案过期时间        | int       |                               |
|             | configModifyRule     | 链配置更改规则       | int       | 0,1,2                         |
|             | enableCert           | 是否开启节点证书      | bool      |                         |
| parentHash  |                      | 创世区块的父hash    | hex hash  |                               |
| number      |                      | 创世区块高度        | int       |                               |
| preacher    |                      | 联盟链盟主         | address   |                               |
| godAmount   |                      | 盟主初始余额        | int       |                               |
| initVersion |                      | 链版本（区块有变动的版本） | int       | 1,2,3,（4 在测试中）          |
| timestamp   |                      | 创世区块时间戳       | hex       |                               |



## 合约生命周期

### 合约生命周期在创世区块中的定义

在创世区块信息中有关合约生命周期的配置的字段有三个

|      |                |       |                        | 作用域                 | 优先级 |
| ---- | -------------- | ----- | ---------------------- | ---------------------- | ------ |
| 1    | isContractVote | bool  | 是否开启合约生命周期   |                        | 0      |
| 2    | isDictatorship | bool  | 投票方式是否是盟主独裁 | 升级、冻结、解冻、吊销 | 1      |
| 3    | deployRule     | 0/1/2 | 合约部署规则           | 部署                   | 1      |


> 盟主独裁：
>
> 联盟链盟主投票具有一票同意和一票否决权。
>
> 关闭盟主独裁，投票形式即为大多数投票通过规则


>合约部署规则: 
>
>0：部署不需要投票
>
>1：部署需要盟主投票
>
>2：部署需要大多数共识节点投票

开启`isContractVote`后另外两个配置才会生效。

`isDictatorship`和`deployRule` 针对合约生命周期的不同阶段, 它们控制的投票规则互不干扰
