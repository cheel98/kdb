# 接口说明

### latc_getDBlockProof

获取守护区块的证明

入参：

`int` 

请求示例：

```bash
curl --location 'http://192.168.1.185:41001' \
--header 'Content-Type: application/json' \
--data '{
    "jsonrpc": "2.0",
    "method": "latc_getDBlockProof",
    "params": [
       151
    ],
    "id": 481
}'
```

返回值：

| 参数名        |      | 含义                       |
| ------------- | ---- | -------------------------- |
| Hash          |      | 对该hash签名               |
| Owner         |      | 签名的所有者               |
| DaemonHash    |      | 守护区块的hash             |
| Number        |      |                            |
| EndNumber     |      |                            |
| Expect        |      | 预料中有其证明的DBlock高度 |
| Signers       |      | 区块见证的签名者           |
| VerifySigners |      | 区块验证的签名者           |

示例：

```
{
    "jsonRpc": "2.0",
    "id": 481,
    "result": {
        "Hash": "0x69c5cd625d241581f4128ab751b18591a058926293e500cb06e5b950d78c166b",
        "Owner": "zltc_RTUbadrrZ9tGSnKtP74JeFHwJ8sWWkBik",
        "DaemonHash": "0x165312fd573fb9655062a02d435db06e1635025ce5eb85937944fd5925c56085",
        "Number": 151,
        "EndNumber": 151,
        "Expect": null,
        "Signers": [
        ],
        "VerifySigners": [
        ]
    }
}
```

