## 节点管理

### node_peers

#### 获取P2P网络的连接情况

参数：

示例：

crul



```
curl --location --request GET '[Your Ip]:[Your port]' \
--header 'ChainId: [your Chain Id]' \
--header 'Content-Type: application/json' \
--data '{"jsonrpc":"2.0","method":"node_peers","params":[],"id":1}'
```

request body

json

```
{"jsonrpc":"2.0","method":"node_peers","params":[],"id":1}
```

返回值：

json

```
{
    "jsonRpc": "2.0",
    "id": 1,
    "result": [
        {
            "inode": "/ip4/172.22.3.124/tcp/20007/p2p/16Uiu2HAkysPjzQtLrru7WfcB5XGjgZ42sPZemMoHTmavM93EoyXF",
            "id": "16Uiu2HAkysPjzQtLrru7WfcB5XGjgZ42sPZemMoHTmavM93EoyXF",
            "name": "",
            "caps": null,
            "network": {
                "localAddress": "/ip4/172.22.3.124/tcp/20002",
                "remoteAddress": "/ip4/172.22.3.124/tcp/20007",
                "inbound": false,
                "trusted": false,
                "static": false
            },
            "protocols": null
        }
    ]
}
```

### node_connectNode

#### 连接新的节点

异步接口，是否连接成功需要借助node_peers 判断

参数：

- 节点的INodeInfo

示例：

crul



```
curl --location --request GET 'http://172.22.0.23:10332' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ0ZXN0Iiwic3ViIjoic29tZWJvZHkiLCJhdWQiOlsic29tZWJvZHlfZWxzZSJdLCJleHAiOjE3MjY4Nzk2NjIsIm5iZiI6MTcyNjc5MzI2MiwiaWF0IjoxNzI2NzkzMjYyLCJqdGkiOiIxIn0.ZKqCmFyEsMVJDdkFM7NCLP8pMbgdqciB8asyIiH9ty4' \
--header 'Content-Type: application/json' \
--data '{
    "jsonrpc": "2.0",
    "method": "node_connectNode",
    "params": [
        "<InodeInfo>"
    ],
    "id": 1
}
'
```

request body

json

```
{
    "jsonrpc": "2.0",
    "method": "node_connectNode",
    "params": [
        "<InodeInfo>"
    ],
    "id": 1
}
```

返回值：

json

```
{
    "jsonRpc": "2.0",
    "id": 1,
    "result": null
}
```

### node_disconnectNode

#### 断开节点连接

异步接口，是否断开连接成功需要借助node_peers 判断

参数：

- 节点的INodeInfo

示例：

crul

```
curl --location --request GET 'http://172.22.0.23:10332' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ0ZXN0Iiwic3ViIjoic29tZWJvZHkiLCJhdWQiOlsic29tZWJvZHlfZWxzZSJdLCJleHAiOjE3MjY4Nzk2NjIsIm5iZiI6MTcyNjc5MzI2MiwiaWF0IjoxNzI2NzkzMjYyLCJqdGkiOiIxIn0.ZKqCmFyEsMVJDdkFM7NCLP8pMbgdqciB8asyIiH9ty4' \
--header 'Content-Type: application/json' \
--data '{
    "jsonrpc": "2.0",
    "method": "node_disconnectNode",
    "params": [
        "<InodeInfo>"
    ],
    "id": 1
}
'
```

返回值：

```
{
    "jsonRpc": "2.0",
    "id": 1,
    "result": null
}
```

### node_version

#### 获取节点版本

异步接口，是否断开连接成功需要借助node_peers 判断

参数：

无

示例：

crul

```
curl --location --request GET 'http://172.22.3.124:20011' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ0ZXN0Iiwic3ViIjoic29tZWJvZHkiLCJhdWQiOlsic29tZWJvZHlfZWxzZSJdLCJleHAiOjE3MTg2Nzc2NjgsIm5iZiI6MTcxODU5MTI2OCwiaWF0IjoxNzE4NTkxMjY4LCJqdGkiOiIxIn0.6DSCM6RCg8OuwXMXKRzuKDKeLkTMY5OyiA0uCe19qR4' \
--header 'Content-Type: application/json' \
--data '{
    "jsonrpc": "2.0",
    "method": "node_nodeVersion",
    "params": [],
    "id": 1
}'
```

返回值：

```
{
    "jsonRpc": "2.0",
    "id": 1,
    "result": {
        "IsIncentive": "无激励",
        "IsConsortium": "联盟链",
        "BuildDate": "2025-02-17 03:08:30",
        "Version": "v2.1.0"
    }
}
```

## 

## 审计

### latc_getEvidences

#### 获取关键信息留痕方法

- 获取留痕信息，主要留痕信息类型有`vote`、`tblock`、`onChain`、`execute`、`sign`、`dblock`等

- 请求参数

  - `params[0]`:`string` 留痕时间（日期具体到天）
  - `params[1]`:`enum` 留痕类型 `vote`、`tblock`、`onChain`、`execute`、`sign`、`dblock`
  - `params[2]`:`int` 当前页
  - `params[3]`:`int` 每页留痕信息条数

- 返回值

  - `total`: 日志数量
  - `data`: 数据
    - `name`: `string` 名称，包含日期等信息
      - `Number`:`int` 区块高度
      - `miner`:`string` 区块打包者账户地址
      - `parentHash`:`string` 父区块 16 进制编码哈希值
      - `timestamp`:`uint64` 时间戳
      - `hash`:`string` data 的 16 进制哈希值

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
   -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "latc_getEvidences",
    "params": [
        "20220311",
        "dblock",
        1,
        10
    ]
  }'
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": {
      "total": 1,
      "data": {
        "20220311_none_dblock_5018_0xce3270a...": {
          "Number": "1",
          "miner": "zltc_",
          "parentHash": "0xa58e07012f68cc17bdd39a695f49087d72f37c5d35f349d5921fe57ee99d6362",
          "timestamp": "1234567890",
          "hash": "0xcfdffa2b015b7ea242c29942a0eed62ea67726cb8ca70ef2e2c08f9a9c2b75de"
        }
      }
    }
  }
  ```

- 错误码

  - `32000`: 未开启留痕功能

### latc_getErrorEvidences

#### 获取`error`级别信息留痕方法

- 获取`Error`级别的留痕信息，主要留痕信息类型有`vote`、`tblock`、`onChain`、`execute`、`sign`、`dblock`等

- 请求参数

  - `params[0]`:`string` 留痕时间（日期具体到天）
  - `params[1]`:`enum` 留痕级别 `error`，`crit`
  - `params[2]`:`enum` 留痕类型 `vote`、`tblock`、`onChain`、`execute`、`sign`、`dblock`
  - `params[3]`:`int` 当前页
  - `params[4]`:`int` 每页留痕信息条数

- 返回值

  - `total`: 日志数量
  - `data`: 数据
    - `name`: `string` 名称，包含日期等信息
      - `Number`:`int` 区块高度
      - `miner`:`string` 区块打包者账户地址
      - `parentHash`:`string` 父区块 16 进制编码哈希值
      - `timestamp`:`uint64` 时间戳
      - `hash`:`string` data 的 16 进制哈希值

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
   -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "latc_getEvidences",
    "params": [
        "20220311",
        "error"
        "dblock",
        1,
        10
    ]
  }'
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": {
      "total": 1,
      "data": {
        "20220311_none_dblock_5018_0xce3270a...": {
          "Number": "1",
          "miner": "zltc_",
          "parentHash": "0xa58e07012f68cc17bdd39a695f49087d72f37c5d35f349d5921fe57ee99d6362",
          "timestamp": "1234567890",
          "hash": "0xcfdffa2b015b7ea242c29942a0eed62ea67726cb8ca70ef2e2c08f9a9c2b75de"
        }
      }
    }
  }
  ```

- 错误码

  - `32000`: 未开启留痕功能

## 链管理

### latc_peers

#### 获取链的对等节点

参数：

示例：

crul



```
curl --location --request GET '[Your Ip]:[Your port]' \
--header 'ChainId: [your Chain Id]' \
--header 'Content-Type: application/json' \
--data '{"jsonrpc":"2.0","method":"latc_peers","params":[],"id":1}'
```

request body

json

```
{"jsonrpc":"2.0","method":"latc_peers","params":[],"id":1}
```

返回值：

json

```
{
    "jsonRpc": "2.0",
    "id": 1,
    "result": {
        "16Uiu2HAmGohS2TyDQwrpZQXFrdPbkH9MuEsfcv7dijNM8m4bcyYA": {
            "Id": "16Uiu2HAmGohS2TyDQwrpZQXFrdPbkH9MuEsfcv7dijNM8m4bcyYA",
            "Saint": "zltc_VwaVTdGi3RrMqXg9xVUiiP9dCYUhRTKfj",
            "ChainId": 1,
            "CertSerialNumber": 314963778182285158441689297968533602950,
            "DBNum": 0,
            "DBHash": "0x93e388362786e3311665e3e4f9c8cad5f11aaa0da73b2a65dbdd4811981a4d17",
            "GinHttpPort": 0,
            "DFS": false,
            "inode": "/ip4/172.22.0.23/tcp/46337/p2p/16Uiu2HAmGohS2TyDQwrpZQXFrdPbkH9MuEsfcv7dijNM8m4bcyYA"
        }
    }
}
```

### latc_connectPeer

#### 连接新的链的对等节点

异步接口，是否连接成功需要借助latc_peers 判断

参数：

- 节点的Id(hash): 如：16Uiu2HAkysPjzQtLrru7WfcB5XGjgZ42sPZemMoHTmavM93EoyXF

示例：

crul



```
curl --location --request GET 'http://172.22.0.23:10332' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ0ZXN0Iiwic3ViIjoic29tZWJvZHkiLCJhdWQiOlsic29tZWJvZHlfZWxzZSJdLCJleHAiOjE3MjY4Nzk2NjIsIm5iZiI6MTcyNjc5MzI2MiwiaWF0IjoxNzI2NzkzMjYyLCJqdGkiOiIxIn0.ZKqCmFyEsMVJDdkFM7NCLP8pMbgdqciB8asyIiH9ty4' \
--header 'Content-Type: application/json' \
--data '{
    "jsonrpc": "2.0",
    "method": "latc_connectPeer",
    "params": [
        "16Uiu2HAkysPjzQtLrru7WfcB5XGjgZ42sPZemMoHTmavM93EoyXF"
    ],
    "id": 1
}
'
```

返回值：

json

```
{
    "jsonRpc": "2.0",
    "id": 1,
    "result": null
}
```

### latc_disconnectPeer

#### 断开对等节点

异步接口，是否断开连接成功需要借助latc_peers 判断

参数：

- 节点的Id(hash): 如：16Uiu2HAkysPjzQtLrru7WfcB5XGjgZ42sPZemMoHTmavM93EoyXF

示例：

crul



```
curl --location --request GET 'http://172.22.0.23:10332' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ0ZXN0Iiwic3ViIjoic29tZWJvZHkiLCJhdWQiOlsic29tZWJvZHlfZWxzZSJdLCJleHAiOjE3MjY4Nzk2NjIsIm5iZiI6MTcyNjc5MzI2MiwiaWF0IjoxNzI2NzkzMjYyLCJqdGkiOiIxIn0.ZKqCmFyEsMVJDdkFM7NCLP8pMbgdqciB8asyIiH9ty4' \
--header 'Content-Type: application/json' \
--data '{
    "jsonrpc": "2.0",
    "method": "latc_disconnectPeer",
    "params": [
        "16Uiu2HAkysPjzQtLrru7WfcB5XGjgZ42sPZemMoHTmavM93EoyXF"
    ],
    "id": 1
}
'
```

返回值：

json

```
{
    "jsonRpc": "2.0",
    "id": 1,
    "result": null
}
```

### witness_nodeList

#### 获取见证节点列表

- 见证节点列表以当前节点的最新区块为准

- 请求参数

  - 无参数

- 返回值

  - `address`:`string` 节点地址
  - `SignatureCount`:`int` 见证区块数量
  - `SignatureFailCount`:`int` 见证失败区块数量
  - `ShouldSignatureCount`:`int` 应当见证的区块数量
  - `Online`:`bool` 是否在线

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "witness_nodeList"
    "params": []
  }'
  
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": [
      {
        "addr": "zltc_hWA6XfYQGTPxYaF96QLdxgAcZbfw5Rhse",
        "SignatureCount": 0,
        "SignatureFailCount": 0,
        "ShouldSignatureCount": 0,
        "Online": true
      }
    ]
  }
  ```

- 错误码

  - 无错误码

# 