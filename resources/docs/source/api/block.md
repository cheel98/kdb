# 区块接口服务

### latc_getGenesis

#### 获取创世区块

- 获取当前节点所在链的创世区块信息

- 请求参数

  - 无参数

- 返回值

  - `TBlock`（账户区块）

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "latc_getGenesis",
    "params": []
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

  - 无错误码

### latc_getDBlockByNumber

#### 根据区块高度获取守护区块

- 获取对应高度下守护链区块的信息，返回 `DBlock`

- 请求参数

  - `number`:`int` 区块高度

- 返回值

  - `DBlock`（守护区块）

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "latc_getDBlockByNumber",
    "params": [1]
  }'
  ```

- 返回结果

  ```json
  {
    "jsonRpc": "2.0",
    "id": "1234567890",
    "result": {
      "anchors": [],
      "coinbase": "zltc_ndTXvhdEiUfJnBF6mVAu5jMajPNjucTCq",
      "contracts": [],
      "difficulty": 0,
      "extra": "0x000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000000590037eca4e90d8b29a43080729b101c8608be872361dfcb430ca375c7d326af2bb8219af2246ead986b61b644a4f5878690eefbbb462ae888c5de6b5534a3a901",
      "hash": "0x9c0df715a1b60325cccfbf9c450f0b151fb80859c3192fa0bdaa78802e1db9ea",
      "ledgerHash": "0x37f5c35f355617ca6dd4442f30d1b8ce1b72892c03190ebf15bc08d079899c92",
      "number": 12,
      "parentHash": "0x4a1956f85745c08847ba48e735ea99e7188e9df566b44d716b8caa50ccdf1289",
      "pow": 0,
      "receiptHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
      "receipts": null,
      "signer": "zltc_ndTXvhdEiUfJnBF6mVAu5jMajPNjucTCq",
      "size": 259,
      "snapshot": "{\"ID\":0,\"number\":12,\"hash\":\"0x9c0df715a1b60325cccfbf9c450f0b151fb80859c3192fa0bdaa78802e1db9ea\",\"signers\":{\"zltc_ndTXvhdEiUfJnBF6mVAu5jMajPNjucTCq\":{}},\"recents\":{\"12\":\"zltc_ndTXvhdEiUfJnBF6mVAu5jMajPNjucTCq\"},\"votes\":[],\"tally\":{},\"loser\":{},\"switchTally\":{},\"switchLoser\":{},\"currentVote\":null,\"finalProposal\":null}",
      "td": 0,
      "timestamp": 1682559324,
      "ttd": 0,
      "version": 2
    }
  }
  ```

- 错误码

  - `2003`: 守护区块为空，没有找到守护区块，请检查高度是否有误

### latc_getCurrentDBlock

#### 获取当前守护区块

- 获取该节点的当前守护区块，如果节点未同步完成，则不一定是链最新的区块

- 请求参数

  - 无参数

- 返回值

  - `DBlock`（守护区块）

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "latc_getCurrentDBlock",
    "params": []
  }'
  ```

- 返回结果

  ```json
  {
    "jsonRpc": "2.0",
    "id": "1234567890",
    "result": {
      "anchors": [],
      "coinbase": "zltc_ndTXvhdEiUfJnBF6mVAu5jMajPNjucTCq",
      "contracts": [],
      "difficulty": 0,
      "extra": "0x00000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000000074afa150f54d17ef2c08e4334b1cb6b9b24af65541922ffa8673934515f5b6a5736d444321b444b37065ba3ec37590f487538f6f1ac2e072d8b24e728a54d1fa00",
      "hash": "0xbc4ec021077c7efd049263121b736fbfd506194a7b253dc5e4f02048b0ee1bf1",
      "ledgerHash": "0xd33f0f2db6ceefa7347ee4b9de9306bdabfef42c3bc408f193979317b856d36f",
      "number": 513,
      "parentHash": "0x4a1e9ce44351694f55261ff08eac4a7bc7bf9f053ff12fa52d9a692d0190f116",
      "pow": 0,
      "receiptHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
      "receipts": null,
      "signer": "zltc_ndTXvhdEiUfJnBF6mVAu5jMajPNjucTCq",
      "size": 261,
      "snapshot": "{\"ID\":0,\"number\":513,\"hash\":\"0xbc4ec021077c7efd049263121b736fbfd506194a7b253dc5e4f02048b0ee1bf1\",\"signers\":{\"zltc_ndTXvhdEiUfJnBF6mVAu5jMajPNjucTCq\":{}},\"recents\":{\"513\":\"zltc_ndTXvhdEiUfJnBF6mVAu5jMajPNjucTCq\"},\"votes\":[],\"tally\":{},\"loser\":{},\"switchTally\":{},\"switchLoser\":{},\"currentVote\":null,\"finalProposal\":null}",
      "td": 0,
      "timestamp": 1683180188,
      "ttd": 0,
      "version": 2
    }
  }
  ```

- 错误码

  - 无错误码

### latc_subscribe

#### 订阅区块链信息

- 订阅方法，仅限 `websocket` 使用

  - 根据调用参数不一样，持续返回不同的数据

- 请求参数

  - `args`:`enum`
    - `monitorData`: 监视器数据
    - `chainState`: 监视链状态
    - `nweDBlock`: 监视守护链出快状态
    - `newTBlock`: 监视账户链出快状态

- 返回值

  - `monitorData`: 监视器数据

    - `subapi`:`string` 订阅连接的 api 码
    - `result`: 返回结果

      - `Chainstate`:`enum` 链运行状态
      - `TPS`:`json` 链上 tps 情况
      - `accept_block`:`json` 接受区块信息
      - `block_info`: `json` 链上账户链与守护链的区块信息

  - `chainState`: 监视链状态

    - `state`:`enum` 链状态

  - `nweDBlock`: 监视守护链出快状态

    - `DBlock`: 守护区块

  - `newTBlock`: 监视账户链出快状态

    - `TBlock`: 账户链区块

#### TBlock state：

- 实例

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "latc_getTBlockState",
    "params": [
      "0x959640415fe52107d1d4af36ed381b2469181c159db5c75235de0806387ea2ef"
    ]
  }
  ```

- 返回结果

  - `monitorData`

  ```json
  {
    "jsonRpc": "2.0",
    "method": "latc_subscription",
    "params": {
      "subapi": "0x865aea7331e51e3b65e35bf4a097d543",
      "result": {
        "ChainState": "running",
        "TPS": "{\"maxTBlockPS\":0,\"maxDBlockPS\":1,\"maxWitnessBlockPS\":1,\"TBlockPS\":0,\"DBlockPS\":0,\"WitnessBlockPS\":0}",
        "accept_block": "{\"AcceptTxCount\":0,\"SendTxCount\":0,\"DiffCount\":0}",
        "block_info": "{\"dblockCount\":154,\"confirmCount\":0,\"tblockCount\":0,\"sendCount\":0,\"contractCount\":0,\"executeCount\":0,\"addressCount\":0}"
      }
    }
  }
  ```

  - `newDBlock`

  ```json
  {
    "jsonRpc": "2.0",
    "method": "latc_subscription",
    "params": {
      "subapi": "0xa1a4735e5bbfaeebce2a74d609e644c",
      "result": {
        "Deposit": [
          {
            "address": "zltc_ndTXvhdEiUfJnBF6mVAu5jMajPNjucTCq",
            "deposit": "4865376864",
            "record": 0
          }
        ],
        "TxHashList": [],
        "anchors": [],
        "coinbase": "zltc_ndTXvhdEiUfJnBF6mVAu5jMajPNjucTCq",
        "contracts": [],
        "difficulty": 0,
        "extra": "0x0000000000000000",
        "hash": "0xc3e4b2e2ad2296b8a4d08c73391f8475d678b23f52a4d52425aa36c16d347b93",
        "height": "464",
        "ledgerHash": "0x0185a20c64494c89d67fdef62cb22c86274b08c819552d58a27793fddbe889a5",
        "number": 464,
        "parentHash": "0x7f0e0ba2a75ab1258dafa839d2dd957dc704721f66c784ee1167a0ab9ceb0788",
        "pow": null,
        "receiptHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
        "receipts": null,
        "reward": {
          "zltc_ndTXvhdEiUfJnBF6mVAu5jMajPNjucTCq": 10485726
        },
        "size": 150,
        "snapshot": "",
        "td": 0,
        "time": "1683249501153",
        "timestamp": 1683249501153,
        "ttd": 0,
        "version": 2
      }
    }
  }
  ```

- 错误码

  - `3811`: 不存在订阅方法，请检查方法名是否错误

