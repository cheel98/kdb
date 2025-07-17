# 合约API

## wallet_getContractState

## 获取合约状态

参数：

```
{
 "合约地址"
}
```

请求示例：

```json
curl --location --request GET 'http://127.0.0.1:54006' \
--header 'Content-Type: application/json' \
--data '{
    "jsonrpc":"2.0",
    "method":"wallet_getContractState",
    "params":[
        "zltc_YKuag6aXVEquYLMnURfXorD69KKVytSUk"
    ],
    "id":1
} '
```

返回值：

```
{
    "address": 合约地址,
    "state": 合约状态,
    "votingProposalId": 投票中的提案id,
    "deploymentAddress": 部署者地址,
    "createAt": 创建时间,
    "modifiedAt": 更新时间
}
```

## wallet_getPermissionList

## 查询合约权限列表状态

参数： 

- 合约地址
- 高度

 ```
{
    "jsonrpc": "2.0",
    "method": "wallet_getPermissionList",
    "params": [
        "zltc_TArLkGjatNkY8X8uJTDwjw7qC2LR1rHcR",
        -1
    ],
    "id": 481
}
 ```

示例：

```
curl --location --request GET 'http://172.22.0.23:10332' \
--header 'chainId: 123' \
--header 'Content-Type: application/json' \
--data '{
    "jsonrpc": "2.0",
    "method": "wallet_getPermissionList",
    "params": [
        "zltc_TArLkGjatNkY8X8uJTDwjw7qC2LR1rHcR",
        -1
    ],
    "id": 481
}'
```

返回值：



返回示例：

## wallet_getFreezeCode

## 获取冻结合约的code

参数：

- 合约地址

请求示例：

```json
curl --location --request GET 'http://127.0.0.1:54006' \
--header 'Content-Type: application/json' \
--data '{
    "jsonrpc":"2.0",
    "method":"wallet_getFreezeCode",
    "params":[
        "zltc_YKuag6aXVEquYLMnURfXorD69KKVytSUk"
    ],
    "id":1
}'
```

返回值：

- code字符串

返回示例：

```json
{
    "jsonRpc": "2.0",
    "id": 1,
    "result": "0x65d4b8b50000000000000000000000000b9d798fe5a6df07f93a7a8a3e106b5ed5aa800a0000000000000000000000000000000000000000000000000000000000000001"
}
```

使用示例：

获取到code后，可通过wallet_sendTBlockE发送交易提交冻结合约的提案：

```json
{
    "jsonrpc": "2.0",
    "method": "wallet_sendTBlockE",
    "params": [
    {
       "owner": "调用者地址",
       "linker": "zltc_ZQJjaw74CKMjqYJFMKdEDaNTDMq5QKi3T",
       "code": "获取到的code",
       "joule": 0
    },
    "密码"
    ],
    "id": 1
}
```

## wallet_getUnfreezeCode

## 获取解冻合约的code

参数：

- 合约地址

请求示例：

```json
curl --location --request GET 'http://127.0.0.1:54006' \
--header 'Content-Type: application/json' \
--data '{
    "jsonrpc":"2.0",
    "method":"wallet_getUnfreezeCode",
    "params":[
        "zltc_YKuag6aXVEquYLMnURfXorD69KKVytSUk"
    ],
    "id":1
}'
```

返回值：

- code字符串

返回示例：

```json
{
    "jsonRpc": "2.0",
    "id": 1,
    "result": "0x65d4b8b50000000000000000000000000b9d798fe5a6df07f93a7a8a3e106b5ed5aa800a0000000000000000000000000000000000000000000000000000000000000002"
}
```

使用示例：

获取到code后，可通过wallet_sendTBlockE发送交易提交解冻合约的提案：

```json
{
    "jsonrpc": "2.0",
    "method": "wallet_sendTBlockE",
    "params": [
    {
       "owner": "调用者地址",
       "linker": "zltc_ZQJjaw74CKMjqYJFMKdEDaNTDMq5QKi3T",
       "code": "获取到的code",
       "joule": 0
    },
    "密码"
    ],
    "id": 1
}
```