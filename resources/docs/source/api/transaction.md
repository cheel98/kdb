# 交易接口服务

## latc_getReceipt

### 获取合约回执

- 根据账户链区块哈希获取合约回执

- 请求参数

  - `hash`：账户链区块哈希

- 返回值

  - `contractAddress`:`string` 合约地址
  - `contractRet`:`string` 合约返回结果或错误信息
  - `dblockHash`:`string` 执行合约对应的守护区块
  - `dblockNumber`:`int` 执行合约守护区块的高度
  - `events`:`array` 合约执行过程中的日志列表
    - `event.address`:`string` 合约地址
    - `event.topics`:`string[]` 合约地址列表 <!-- TODO: 这个字段不知道什么意思 -->
    - `event.data`:`string` 合约日志信息
    - `event.dblockNumber`:`int` 执行合约产生日志的守护区块高度
    - `event.removed`:`bool` 是否被删除
    - `event.dataHex`:`string` 十六进制日志信息
  - `jouleUsed`:`int` 合约执行消耗的手续费
  - `receiptindex`:`int` 合约执行在守护区块中的索引
  - `successs`:`bool` 合约石油成功执行
  - `tblockHash`:`string` 合约账户区块的哈希值，即交易哈希

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "latc_getReceipt",
    "params": [ "0x959640415fe52107d1d4af36ed381b2469181c159db5c75235de0806387ea2ef"
    ]
  }'
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": {
      "contractAddress": "zltc_",
      "contractRet": "0x",
      "dblockHash": "0xa58e07012f68cc17bdd39a695f49087d72f37c5d35f349d5921fe57ee99d6362",
      "dblockNumber": 0,
      "events": [
        {
          "address": "zltc_",
          "topics": [],
          "data": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE=",
          "logIndex": 0,
          "tblockHash": "0xcfdffa2b015b7ea242c29942a0eed62ea67726cb8ca70ef2e2c08f9a9c2b75de",
          "dblockNumber": 0,
          "removed": false,
          "dataHex": ""
        }
      ],
      "jouleUsed": 0,
      "receiptIndex": 0,
      "success": true,
      "tblockHash": "0xcfdffa2b015b7ea242c29942a0eed62ea67726cb8ca70ef2e2c08f9a9c2b75de"
    }
  }
  ```

- 错误码

  -

## wallet_sendTBlock

### 发起转账

- 参数
  -  {}
    - `type`:`string`  固定值 `send`

    - `number`:`int` 账户区块高度
    - `parentHash`:`hash` 依赖的TBlock父区块hash
    - `daemonHash`:`hash` 依赖的DBlockhash
    - `owner`:`hash` 转账发起者
    - `linker`:`hash`  转账接受者
    - `amount`:`int` 转账额度
    - `payload`:`string` payload 信息 选填
    - `timestamp`:`int` 发起时间戳

  - 账户密码

- 返回值
  - 交易hash

- 实例

  ```bash
  curl --location --request GET 'http://172.22.3.124:20011' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_sendTBlock",
      "params": [
          {
              "type": "send",
              "number": 1,
              "parentHash": "0xb6bcc6e368c2fc12ee9fe0c0ef06ac141509c02650dbc4e4d66ea853d4640ea8",
              "daemonHash": "0x2a2afb26d4cbda93b3578ad09bdcb34897a323442109233663a5c443177c09fe",
              "owner": "zltc_hRzdBQSUeHa2DLo1JTcVgJVCdxV949uQf",
              "linker": "zltc_QLbz7JHiBTspS962RLKV8GndWFwjA5K66",
              "amount": 0,
              "proofOfWork": "",
              "payload": "0x005468697320697320616e20756c747261206c6f6e672c20756c747261206c6f6e672c20756c747261206c6f6e672c20756c747261206c6f6e6720",
              "timestamp": 1704852369
          },
          "Aa123456"
      ],
      "id": 1
  }'
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": {
       "0xcfdffa2b015b7ea242c29942a0eed62ea67726cb8ca70ef2e2c08f9a9c2b75de"
    }
  }
  ```

- 错误码

  -

### 接收转账

- 参数

  - {}
    - `type`:`string`  固定值 `receive`
    - `owner`:`hash` 转账接受者
    - `pairedHash`:`hash`  发起转账的那笔TBlock的hash
    - `timestamp`:`int` 时间戳
  - 账户密码
- 返回值
  - 交易hash
- 实例

```json
curl --location --request GET '192.168.2.12:6001' \
--header 'Content-Type: application/json' \
--data '{
    "jsonrpc": "2.0",
    "method": "wallet_sendTBlock",
    "params": [
        {
            "type": "receive",
            "owner": "zltc_Xmk6g2Lgxitrx4xEPUZgF4hHdnHwDcBuU",
            "pairedHash": "0x747565af57530280fac5cbb5292bd9266ebd2b9506b2a0045bdaf11edae9906c",
            "timestamp": 1607572085
        },
        "aA592918942"
    ],
    "id": 1
}'
```

- 返回结果

```json
{
  "jsonrpc": "2.0",
  "id": "1234567890",
  "result": {
     "0x747565af57530280fac5cbb5292bd9266ebd2b9506b2a0045bdaf11edae9906c"
  }
}
```

