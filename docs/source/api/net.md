# 网络API

## latc_peers

## 获取链的对等节点

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

```json
{"jsonrpc":"2.0","method":"latc_peers","params":[],"id":1}
```

返回值：

```json
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

## node_peers

## 获取P2P网络的连接情况

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

```json
{"jsonrpc":"2.0","method":"node_peers","params":[],"id":1}
```

返回值：

```json
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

## node_connectNode

## 连接新的节点

异步接口，是否连接成功需要借助node_peers 判断

参数：

-  节点的INodeInfo

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

```json
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

```json
{
    "jsonRpc": "2.0",
    "id": 1,
    "result": null
}
```

## node_disconnectNode

## 断开节点连接

异步接口，是否断开连接成功需要借助node_peers 判断

参数：

-  节点的INodeInfo

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

```json
{
    "jsonRpc": "2.0",
    "id": 1,
    "result": null
}
```

## latc_connectPeer

## 连接新的链的对等节点

异步接口，是否连接成功需要借助latc_peers 判断

参数：

-  节点的Id(hash): 如：16Uiu2HAkysPjzQtLrru7WfcB5XGjgZ42sPZemMoHTmavM93EoyXF

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

```json
{
    "jsonRpc": "2.0",
    "id": 1,
    "result": null
}
```

## latc_disconnectPeer

## 断开对等节点

异步接口，是否断开连接成功需要借助latc_peers 判断

参数：

-  节点的Id(hash): 如：16Uiu2HAkysPjzQtLrru7WfcB5XGjgZ42sPZemMoHTmavM93EoyXF

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

```json
{
    "jsonRpc": "2.0",
    "id": 1,
    "result": null
}
```

