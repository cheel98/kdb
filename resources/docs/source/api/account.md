# 账户接口服务

### latc_getBalance

#### 获取账户余额

- 获取账户的余额和未接受的交易总金额，该金额可以认作该账户所有资金

- 请求参数

  - `address`:`string` 账户链的账户地址

- 返回值

  - `balance`:`big.Int` 账户余额

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "latc_getBalance",
    "params": [
      "zltc_Z2x79qTEbKVakBWQGjvpVgjAt4DTix7tx"
    ]
  }'
  ```

- 返回结果

  ```json
  {
    "jsonRpc": "2.0",
    "id": "1234567890",
    "result": 0
  }
  ```

- 错误码

  - `3601`：地址格式不合法或地址不存在，请检查地址是否错误

### latc_getTBlockByHash

#### 根据区块 hash 获取账户区块

- 获取区块哈希获取的账户区块,如果该哈希值是守护区块哈希,查询失败

- 请求参数

  - `hash`:`string` 区块哈希的 16 进制编码

- 返回值

  - `TBlock`（账户区块）

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "latc_getTBlockByHash",
    "params": ["0x0000000000000000000000000000000000000000000000000000000000000000"]
  }'
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": {
      "amount": "0",
      "balance": "0",
      "code": "0x",
      "codeHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
      "daemonHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
      "deposit": "0",
      "difficulty": 0,
      "hash": "0xd445ff7381b54cfadd3c25de06e23117259828ff3b6cd1e7fb1cae6d7920cef4",
      "hub": [],
      "income": "0",
      "joule": 0,
      "linker": "zltc_",
      "number": 0,
      "owner": "zltc_",
      "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
      "payload": "0x",
      "pow": "0",
      "record": 0,
      "size": 0,
      "timestamp": "1583289456",
      "type": "genesis"
    }
  }
  ```

- 错误码

  - `2004`: 没有找到守护区块，请检查 hash 是否有误

### latc_getPendingTBlock

#### 获取当前账户未接受交易（缺乏具体案例）

- 获取当前账户所有未接受交易，未进行分页操作

- 请求参数

  - `address`:`string` 账户链的账户地址

- 返回值

  - `TBlock`[]：`array`当前账户未接受交易的交易列表
    - `Tblock`:账户区块

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "latc_getPendingTBlock",
    "params": [
      "zltc_Z2x79qTEbKVakBWQGjvpVgjAt4DTix7tx"
    ]
  }'
  ```

- 返回结果

  ```json
  {
    "jsonRpc": "2.0",
    "id": "1234567890",
    "result": null
  }
  ```

- 错误码

  - `3601`:地址格式不合法或地址不存在，请检查地址是否错误

### latc_getCurrentTBlock

#### 获取账户链当前账户区块

- 获取该节点的当前守护区块，如果节点未同步完成，则不一定是链最新的区块

- 请求参数

  - `address`:`string` 账户链的账户地址

- 返回值

  - `TBlock`（账户区块）

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "latc_getCurrentTBlock",
    "params": ["zltc_aXnttsR8f4ZUZge4AoAH2DDt3AXEBNJXL"]
  }'
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": {
      "amount": "0",
      "balance": "0",
      "code": "0x",
      "codeHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
      "daemonHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
      "deposit": "0",
      "difficulty": 0,
      "hash": "0xd445ff7381b54cfadd3c25de06e23117259828ff3b6cd1e7fb1cae6d7920cef4",
      "hub": [],
      "income": "0",
      "joule": 0,
      "linker": "zltc_",
      "number": 0,
      "owner": "zltc_",
      "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
      "payload": "0x",
      "pow": "0",
      "record": 0,
      "size": 0,
      "timestamp": "1583289456",
      "type": "genesis"
    }
  }
  ```

- 错误码

  - `2004`: 没有找到守护区块，暂无当前用户信息，如以发送过交易，请检查交易是否上链

### latc_getTBlockState

#### 获取账户区块状态

- 获取当前节点的账户链状态，如果该节点和其他节点断开，则不一定是链的实际状态

- 请求参数

  - `hash`：账户区块哈希

- 返回值

  - `TBlock state`:`enum`
    - `notExist`: 不存在
    - `inPool`: 在交易池中
    - `witnessing`: 见证中
    - `onChain`: 以上链
    - `deamon`: 以被守护（执行/部署）

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
  	"jsonrpc": "2.0",
  	"id": "1234567890",
  	"method": "latc_getTBlockState",
  	"params": [
   	 "0x959640415fe52107d1d4af36ed381b2469181c159db5c75235de0806387ea2ef"
  	]
  }'
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": "daemon"
  }
  ```

- 错误码

  - 无错误码

### wallet_newAccount

#### 创建新账户

- 根据用户输入的密码创建新账户

- 请求参数

  - `password`:`string` 密码

- 返回值

  - `address`:`string` 账户地址

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "wallet_newAccount",
    "params": [
        "123"
    ]
  }'
  
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": "zltc_WHnoGBp3tfknaevggb9e8QfaZEsP5UjPk"
  }
  ```

- 错误码

  - `32000`: 密码不能为空

### wallet_lockAccount

#### 锁定账户

- 根据用户的地址和密码锁定账户

- 请求参数

  - `address`:`string` 账户地址
  - `password`:`string` 密码

- 返回值

  - `result`:`bool` 成功与否

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "wallet_lockAccount",
    "params": [
        "zltc_WHnoGBp3tfknaevggb9e8QfaZEsP5UjPk",
        "123"
    ]
  }'
  
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": "true"
  }
  ```

- 错误码

  - 无错误码

### wallet_unlockAccount

#### 解锁账户

- 根据用户的地址和密码解锁一定时间的账户

- 请求参数

  - `address`:`string` 账户地址
  - `password`:`string` 密码
  - `time`:`uint64` 解锁时间

- 返回值

  - `result`:`bool` 成功与否

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
  "jsonrpc": "2.0",
  "id": "1234567890",
  "method": "wallet_unlockAccount",
  "params": [
      "zltc_WHnoGBp3tfknaevggb9e8QfaZEsP5UjPk",
      "123",
      3000
  ]
  }'
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": "true"
  }
  ```

- 错误码

  - 无错误码

### wallet_lockSaint（应该对错误做处理）

#### 锁定见证账户

- 根据密码锁定见证账户

- 请求参数

  - `password`:`string` 见证密码

- 返回值

  - `result`:`bool` 成功与否

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "wallet_lockSaint",
    "params": [
        "123"
    ]
  }'
  
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": "true"
  }
  ```

- 错误码

  - 无错误码

### wallet_unlockSaint

#### 解锁见证账户

- 根据密码解锁一定时间的见证账户

- 请求参数

  - `password`:`string` 密码
  - `time`:`uint64` 解锁时间

- 返回值

  - `result`:`bool` 成功与否

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
  "jsonrpc": "2.0",
  "id": "1234567890",
  "method": "wallet_unlockSaint",
  "params": [
      "123",
      3000
  ]
  }'
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": "true"
  }
  ```

- 错误码

  - `3901`: 根据密码无法解析出私钥，请检查密码

### wallet_unlockSaintForever

#### 永久解锁见证账户

- 根据密码永久解锁见证账户

- 请求参数

  - `password`:`string` 密码

- 返回值

  - `result`:`bool` 成功与否

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
  "jsonrpc": "2.0",
  "id": "1234567890",
  "method": "wallet_unlockSaintForever",
  "params": [
      "123",
      3000
  ]
  }'
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": "true"
  }
  ```

- 错误码

  - `3901`: 根据密码无法解析出私钥，请检查密码

### wallet_importRawKey

#### 导入账户

- 根据用户的私钥、密码导入账户

- 请求参数

  - `hash`:`string` 账户私钥（私钥是一个 32 位长的 16 进制编码字符串，与 hash 相同）
  - `password`:`string` 密码

- 返回值

  - `address`:`string` 私钥对应的地址

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
        "jsonrpc": "2.0",
        "id": "1234567890",
        "method": "wallet_importRawKey",
        "params": [
            "0x9de0607322c7fd61f3a13d116662077e5d7ce176bd51a8a5c4b858ec9270a05c",
            "123"
        ]
    }'
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": "zltc_cBW14SpRxjV2dWxfsnxu518QZpEdspxYZ"
  }
  ```

- 错误码

  - `1`: InvalidCredentials，无效证件

### wallet_importFileKey

#### 导入 FileKey 文件

- 根据用户的 FileKey 文件中的内容（json 字符串格式）导入账户

- 请求参数

  - `filekey`:`json` filekey 的 json 字符串

- 返回值

  - `address`:`string` 私钥对应的地址

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "wallet_importFileKey",
    "params": [
        "{\"uuid\":\"96939b22-4593-472e-b7d6-1450e380fc50\",\"address\":\"zltc_Zdf7mCcXYxs6uD227gNMXQxTrL89onusk\",\"cipher\":{\"aes\":{\"cipher\":\"aes-128-ctr\",\"cipherText\":\"4d013cd4328b5989f3854c2582e6ea1901883aed92c6cd9c071c186f47bc4a80\",\"iv\":\"595d1f99d5a0830545db493f9a6c1a78\"},\"kdf\":{\"kdf\":\"scrypt\",\"kdfParams\":{\"DKLen\":32,\"n\":262144,\"p\":1,\"r\":8,\"salt\":\"0a47c6da35b63aee6f4fb24c89d7b9b40b3f8a78ecdc7d218723f2070c87ec51\"}},\"cipherText\":\"4d013cd4328b5989f3854c2582e6ea1901883aed92c6cd9c071c186f47bc4a80\",\"mac\":\"e7de416bc96c136cbf1869f0fa2272deb92dddc4ae91ffce2966da30e40addcb\"},\"isGM\":true}"
    ]
    }'
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": "zltc_cBW14SpRxjV2dWxfsnxu518QZpEdspxYZ"
  }
  ```

- 错误码

  - `1`: InvalidCredentials，无效证件

### wallet_accountList

#### 获取账户列表

- 获取钱包所连接节点中的账户列表

- 请求参数

  - 无参数

- 返回值

  - `address`:`array` 地址列表
    - `address`:`string` 账户地址

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "wallet_accountList",
    "params": []
    }'
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": [
      "zltc_cBW14SpRxjV2dWxfsnxu518QZpEdspxYZ",
      "zltc_TT4Sb87cF67mKFkN3QLLPMZFdDcMhVeKC"
    ]
  }
  ```

- 错误码

  - 无错误码

### wallet_sign

#### 获取账户列表

- 消息签名

- 请求参数

  - `params[0]`:`string` 待签名的消息
  - `params[1]`:`string` 账户地址
  - `params[2]`:`string` 账户密码

- 返回值

  - `hash`:`string` 消息的签名

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "wallet_sign",
    "params": [
        "abc",
        "zltc_jkz9BAX19WyTAmiVXcbK5HRGow3d9tWSV",
        "123"
    ]
    }'
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": "0x064ab3b28ff2f788e13224fae4b2aeead47ac6d1333b7103a6fca29701cfdbaa13b50b1d790480c61144b0cc23d2f90f8583125a39a208a62d26b614bdab18201c"
  }
  ```

- 错误码

  - `3901`: 根据密码无法解析出私钥，请检查密码.

### wallet_signVerify

#### 验证消息签名

- 根据数据及签名数据验证签名

- 请求参数

  - `params[0]`:`string` 未签名的消息
  - `params[1]`:`string` 以签名的消息（16 进制哈希值）

- 返回值

  - `address`:`string` 返回签名者的账户地址（需进一步根据地址判断签名是否正确）

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "wallet_signVerify",
    "params": [
        "abc",
        "0x064ab3b28ff2f788e13224fae4b2aeead47ac6d1333b7103a6fca29701cfdbaa13b50b1d790480c61144b0cc23d2f90f8583125a39a208a62d26b614bdab18201c"
    ]
    }'
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": "zltc_jkz9BAX19WyTAmiVXcbK5HRGow3d9tWSV"
  }
  ```

- 错误码

  - 无错误码

### wallet_sendTBlock （这里面则 type 有些意义不明）

#### 发送账户交易区块

```go
var TBlockType = map[string]uint8{
	<!-- "genesis":         GenesisT,  -->
	<!-- "create":          CreateT, -->
	<!-- "send":            SendT, -->
	"receive":         ReceiveT,
	"contract":        ContractT,
	"execute":         ExecuteT,
	"update":          UpdateT,
	"contractRevoke":  ContractRevokeT,
	"contractFreeze":  ContractFreezeT,
	"contractRelease": ContractReleaseT,
	<!-- "createGo":        NativeGoContractT, -->
	<!-- "createJava":      NativeJavaContractT, -->
	<!-- "executeGo":       NativeGoExecuteT, -->
	<!-- "executeJava":     NativeJavaExecuteT, -->
	<!-- "updateGo":        NativeGoUpdateT, -->
	<!-- "updateJava":      NativeJavaUpdateT, -->
}

```

- 根据区块数据及密码发送区块

- 请求参数

  - `TBlock`: 账户区块结构

    - `type`: `enum` 交易类型，默认值为`send`，可省略
      - `send`: 发送交易,创建 sol 合约，执行 sol 合约
      - `updata` 升级 sol 合约
      - `creatGo`: 创建 Go 语言合约
      - `createJava`: 创建 java 合约
      - `executeGo`: 执行 Go 合约
      - `executeJava`: 执行 java 合约
      - `updateGo`: 升级 Go 合约
      - `updateJava`: 升级 Java 合约
    - `owner`:`string` 发送者地址
    - `payload`:`string` 16 进制交易附言，可省略
    - `timestamp`:`uint64` 时间戳，可省略
    - `hub`:`hash[]` 接收的发送交易哈希列表，可省略
    - `linker`:`string` 接收者地址，如果是执行合约则为合约地址
    - `amount`:`big.int` 交易金额
    - `code`: `string` 合约调用码，或合约二进制码，使用 16 进制编码，可省略
    - `joule`: `int` 合约执行费用，可省略

  - `password`:`string` 密码

- 返回值

  - `hash`:`string` 16 进制编码的交易哈希

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
  "jsonrpc": "2.0",
  "id": "1234567890",
  "method": "wallet_sendTBlock",
  "params": [
        {
        "type": "send",
        "owner": "zltc_W92gnen8ft4cNuygmFagMzMmg2kpzkSTM",
        "payload": "0x",
        "timestamp": 1607572085,
        "hub": [
        ],
        "linker": "zltc_jeKstZ3sJxyTyeXXwKWt31YuJTMNJXh6E",
        "amount": 0,
        "joule": 200000
        },
        "123"
    ]
    }'
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": "0x959640415fe52107d1d4af36ed381b2469181c159db5c75235de0806387ea2ef"
  }
  ```

- 错误码

  - `2401`: 该账户的 filekey 并不在节点中,请检查 owner 字段，或连接其他网络节点
  - `3601`: 地址不合法
  - `2001`: 交易区块的类型(type)参数有误
  - `2002`: 签名有误
  - `2008`: 交易区块 code 字段不合法
  - `3015`: 计算 PoW 难度失败
  - `2314`: 无法根据链接的守护区块计算当前区块的标准难度

### wallet_sendRowTBlock （这里面则 type 有些意义不明）

#### 发送已签名区块

```go
var TBlockType = map[string]uint8{
	<!-- "genesis":         GenesisT,  -->
	<!-- "create":          CreateT, -->
	<!-- "send":            SendT, -->
	"receive":         ReceiveT,
	"contract":        ContractT,
	"execute":         ExecuteT,
	"update":          UpdateT,
	"contractRevoke":  ContractRevokeT,
	"contractFreeze":  ContractFreezeT,
	"contractRelease": ContractReleaseT,
	<!-- "createGo":        NativeGoContractT, -->
	<!-- "createJava":      NativeJavaContractT, -->
	<!-- "executeGo":       NativeGoExecuteT, -->
	<!-- "executeJava":     NativeJavaExecuteT, -->
	<!-- "updateGo":        NativeGoUpdateT, -->
	<!-- "updateJava":      NativeJavaUpdateT, -->
}

```

- 根据已签名的区块数据发送区块

- 请求参数

  - `number`:`int` 区块高度
  - `type`: `enum` 交易类型，默认值为`send`，可省略
    - `send`: 发送交易,创建 sol 合约，执行 sol 合约
    - `updata` 升级 sol 合约
    - `creatGo`: 创建 Go 语言合约
    - `createJava`: 创建 java 合约
    - `executeGo`: 执行 Go 合约
    - `executeJava`: 执行 java 合约
    - `updateGo`: 升级 Go 合约
    - `updateJava`: 升级 Java 合约
  - `parentHash`:`hash` 父区块哈希
  - `daemonHash`:`hash` 守护区块哈希
  - `pairedHash`:`hash` 连接的守护链区块哈希
  - `owner`:`string` 发送者地址
  - `payload`:`string` 16 进制交易附言，可省略
  - `timestamp`:`uint64` 时间戳，可省略
  - `hub`:`hash[]` 接收的发送交易哈希列表，可省略
  - `linker`:`string` 接收者地址，如果是执行合约则为合约地址
  - `proofOfWork`:`string` PoW 算法的 nonce 值
  - `sign`:`string` 签名

- 返回值

  - `hash`:`string` 16 进制编码的交易哈希

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
  "jsonrpc": "2.0",
  "id": "1234567890",
  "method": "wallet_sendRowTBlock",
  "params": [
    {
        "number": 0,
        "type": "send",
        "parentHash": "0xa4deaf3e4601486bb48a73be6dec1830bf16483e5235b1ac3249b70b07305c0b",
        "daemonHash": "0xa4deaf3e4601486bb48a73be6dec1830bf16483e5235b1ac3249b70b07305c0b",
        "pairedHash": "0xa4deaf3e4601486bb48a73be6dec1830bf16483e5235b1ac3249b70b07305c0b",
        "owner": "zltc_g2aKdYGqJKFnineLtfGkaDTHyVQCRnooU",
        "payload": "0x",
        "timestamp": 1607572085,
        "linker": "zltc_jeKstZ3sJxyTyeXXwKWt31YuJTMNJXh6E",
        "proofOfWork": "0x313233",
        "sign": "0xfdadf44f176e37c8c46af74bce6ff67a877d7ac85ec49950b741112c447fd90250a28de94ee8bddfe36357d79b33da095e7be8306c2bcb683bcf548ee9e53c980b"
        }
    ]
    }'
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": "0x959640415fe52107d1d4af36ed381b2469181c159db5c75235de0806387ea2ef"
  }
  ```

- 错误码

  - `2401`: 该账户的 filekey 并不在节点中,请检查 owner 字段，或连接其他网络节点
  - `3601`: 地址不合法
  - `2001`: 交易区块的类型(type)参数有误
  - `2002`: 签名有误
  - `2008`: 交易区块 code 字段不合法
  - `3015`: 计算 PoW 难度失败
  - `2314`: 无法根据链接的守护区块计算当前区块的标准难度

### wallet_preExecuteContract

#### 预执行合约

- 通过预执行合约可以获取到合约消耗，合约返回等信息

- 请求参数

  - `type`: `enum` 交易类型，默认值为`send`，可省略
    - `send`: 发送交易,创建 sol 合约，执行 sol 合约
    - `updata` 升级 sol 合约
    - `creatGo`: 创建 Go 语言合约
    - `createJava`: 创建 java 合约
    - `executeGo`: 执行 Go 合约
  - `owner`:`string` 发送者地址
  - `code`:`string` 16 进制合约执行码
  - `joule`:`int` 合约执行/部署费用
  - `amount`:`big.int` 交易金额
  - `linker`:`string`合约地址

- 返回值

  - `contractAddress`: `string` 合约地址
  - `contractRet`:`string` 合约返回值或错误信息
  - `dblockHash`:`string` 执行该合约的守护区块 hash 值
  - `number`:`int` 执行该合约的守护区块 hash 值
  - `events`:`event` 事件日志列表
    - `event`: 参考 event 结构
  - `jouleUsed`:`int` 合约执行耗费的手续费
  - `receiptIndex`:`int` 合约执行在守护区块中的顺序
  - `success`:`bool` 合约运行是否成功
  - `tblockHash`:`string` 合约账户区块的 hash 值，即交易 hash

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
  "jsonrpc": "2.0",
  "id": "1234567890",
  "method": "wallet_preExecuteContract",
  "params": [
    {
        "type": "contract",
        "owner": "zltc_g2aKdYGqJKFnineLtfGkaDTHyVQCRnooU",
        "code": "0x608060405234801561001057600080fd5b50610134806100206000396000f3fe6080604052348015600f57600080fd5b506004361060325760003560e01c80631122db9a146037578063c6888fa1146076575b600080fd5b606060048036036020811015604b57600080fd5b810190808035906020019092919050505060b5565b6040518082815260200191505060405180910390f35b609f60048036036020811015608a57600080fd5b810190808035906020019092919050505060cb565b6040518082815260200191505060405180910390f35b6000600782026000819055506000549050919050565b60008160005402905091905056fea265627a7a72315820fb8e1458bd3bdfe4c1385508d7a7e2ee7262d6d834c779a219a63886cf2e57cf64736f6c637828302e352e31312d646576656c6f702e323031392e372e32362b636f6d6d69742e34666137383030340058",
        "joule": 200000,
        "amount": 0,
        "linker": "zltc_jeKstZ3sJxyTyeXXwKWt31YuJTMNJXh6E"
        }
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

  - `3601`: 地址不合法
  - `2001`: 交易区块的类型(type)参数有误
  - `2008`: 交易区块 code 字段不合法

### wallet_getContractByteCode

#### 获取合约的 byteCode

- 根据合约地址获取合约的 byteCode

- 请求参数

  - `address`:`string` 合约地址

- 返回值

  - `hex`:`string` 使用 16 进制编码的合约的 byteCode

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "wallet_getContractByteCode",
    "params": [
        "zltc_hWA6XfYQGTPxYaF96QLdxgAcZbfw5Rhse"
    ]
  }'
  
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": "0x6080604052348015600f57600080fd5b506004361060325760003560e01c80631122db9a146037578063c6888fa1146076575b600080fd5b606060048036036020811015604b57600080fd5b810190808035906020019092919050505060b5565b6040518082815260200191505060405180910390f35b609f60048036036020811015608a57600080fd5b810190808035906020019092919050505060cb565b6040518082815260200191505060405180910390f35b6000600782026000819055506000549050919050565b60008160005402905091905056fea265627a7a72315820fb8e1458bd3bdfe4c1385508d7a7e2ee7262d6d834c779a219a63886cf2e57cf64736f6c637828302e352e31312d646576656c6f702e323031392e372e32362b636f6d6d69742e34666137383030340058"
  }
  ```

- 错误码

  - 无错误码