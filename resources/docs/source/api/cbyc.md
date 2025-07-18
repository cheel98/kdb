# 以链建链API

## **cbyc_getChildChainId**

### 获取已有子链的ID

示例

`cbyc17_getChildChainId`, 查询链Id为17的所有子链

``` 
{

  "jsonrpc": "2.0",

  "method": "cbyc17_getChildChainId",

  "params": [ 

  ],

  "id": 1

}
```

## **cbyc_getChainStatus**

###  获取链运行状态 （running/stop）

```json
{

  "jsonrpc": "2.0",

  "method": "cbyc17_getChainStatus",

  "params": [ 

  ],

  "id": 1

}
```

返回值: running/stop

## cbyc_getCreatedAllChains

### 获取当前链创建的所有子链

```json
{
    "jsonrpc": "2.0",
    "method": "latc_getProtocols",
    "params": [
    ],
    "id": 1
}
```

## cbyc_selfJoinChain

### 让当前节点加入某条链

参数：

- 链id
- 网络id
- 已知已经有该链的节点的Inode

```json
{
    "jsonrpc": "2.0",
    "method": "cbyc_selfJoinChain",
    "params": [
        1213,
        12,
        "xxxx"
    ],
    "id": 1
}
```

返回值：成功或错误信息

## cbyc_stopSelfChain

### 停止当前节点的链服务

```json
{
    "jsonrpc": "2.0",
    "method": "cbyc_stopSelfChain",
    "params": [
    ],
    "id": 1
}
```

返回值：成功或错误信息

## cbyc_startSelfChain

### 开启当前节点的链服务

```json
{
    "jsonrpc": "2.0",
    "method": "cbyc_startSelfChain",
    "params": [
    ],
    "id": 1
}
```

返回值：成功或错误信息

## cbyc_restartSelfChain

### 重启当前节点的链服务

```json
{
    "jsonrpc": "2.0",
    "method": "cbyc_restartSelfChain",
    "params": [
    ],
    "id": 1
}
```

返回值：成功或错误信息

## cbyc_delSelfChain

### 删除当前节点的链服务及数据

> 不能撤销，成功请求后，节点关与此链的链账本会被删除。

```json
{
    "jsonrpc": "2.0",
    "method": "cbyc_delSelfChain",
    "params": [
    ],
    "id": 1
}
```

返回值：成功或错误信息

## node_getAllChainId

### 返回该节点维护的链ID

``` json
{
    "jsonrpc": "2.0",
    "method": "node_getAllChainId",
    "params": [
    ],
    "id": 1
}
```

## latc_latcInfo

``` json
{
    "jsonrpc": "2.0",
    "method": "latc_latcInfo",
    "params": [
    ],
    "id": 481
}
```

