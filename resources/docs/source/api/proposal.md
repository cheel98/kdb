# 1. 提案管理API

## 1.1 提案查询

### wallet_getPermissionList

#### 获取合约权限列表

- 获取指定合约的黑白名单管理员名单等信息

- 请求参数

    - 合约地址

- 返回值

    - 权限列表[PermissionList](#dcPermissionList)

- 实例

  ```bash
  curl --location --request GET '192.168.2.12:9001' \
  --header 'Content-Type: text/plain' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getPermissionList",
      "params": [
          "zltc_V7WT2NE191FJf7rUjHoKPbTaKHbKCR8En"
      ],
      "id": 481
  }'
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": {
          "permissionMode": 1,
          "threshold": 7,
          "blackList": [],
          "whiteList": [
              "zltc_TbMJndAHmi4Z8WDnCEQX2uPzNctNFqPJd",
              "zltc_cSGdEJWw5r17uvBe8MLGQHKY4QJsfodfg",
              "zltc_j8XPWoakQzGRk4NPYheNeJFAiDBgQ25W8",
              "zltc_X9mYCE7BPTw6VGmn2SsPnifZ6JqjroYww"
          ],
          "managerList": {
              "zltc_fnvthyf8pcXeraTpqk4GM5Sa5E7TBC8ZR": 10,
              "zltc_j8XPWoakQzGRk4NPYheNeJFAiDBgQ25W8": 10
          }
      }
  }
  ```

- 错误码

    - 2571 提案状态错误，合约不存在, 请确认合约地址是否正确，或者合约是否已经部署

### wallet_getProposalById

#### 获取提案详细内容

- 根据提案ID获取提案详细信息

- 请求参数

    - 提案ID

- 返回值

    - 提案内容和提案结果

      ``` json
      {
          "proposalContent": {}, // proposal具体内容
          "proposalResult": {
             "agreeCollection": [
                 "",
                 ""
             ],
             "againstCollection": []
          }
      }
      ```

    - proposalContent 的结构参考具体提案介绍

    - proposalResult中的agreeCollection和againstCollection的类型是 `地址字符串列表`

- 实例

  ```bash
  curl --location --request GET 'http://192.168.2.12:5001' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getProposalById",
      "params": [
          "0x030000000070726f706f73616c5f616464726573736d000000000000003230323430373130"
      ],
      "id": 481
  }'
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": {
          "proposalContent": {
              "proposalId": "0x027eb68d749ce348b2be25d56cc6c48b625801f8420000000000000000",
              "proposalState": 1,
              "nonce": 0,
              "contractAddress": "zltc_btbpFhmMV88ZakUDEK45KwvSzuoSHGU68",
              "isRevoke": 3,
              "period": 0
          },
          "proposalResult": {
              "agreeCollection": [
                  "address",
                  "address"
              ],
              "againstCollection": []
          }
      }
  }
  ```

- 错误码

    - 无错误码

### wallet_getProposal

#### 获取提案

- 获取提案

- 请求参数

    - ```json
      {
          "proposalId":  提案id，为空则按后续规则查询
          "proposalType": 提案类型，为空则返回所有类型 
          "proposalState": 提案状态，为空则返回所有状态 
          "proposalAddress": 指定地址查询特定类型的提案
        	"dateStart"：开始时间（必填项）
      	"dateEnd": 结束时间（必填项）
      }

- 返回值

    - 提案列表

      ```json
      [
          {
              "proposalContent": {}, // 提案具体内容 见附件2.2
              "ProposalType":        // 提案类型，int类型
          }
      ]
      ```

      [proposalContent 见附件2.2](#dcProposalConent)

- 示例

  ```bash
  curl --location --request GET 'http://192.168.2.12:5001' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getProposal",
      "params": [
          {
              "proposalId": "",
              "proposalType": 2,
              "proposalAddress": "zltc_YsBiB4CrsFHXMmS9my5HZWswSR7jpaS6M",
          	"dateStart"："20250101",
  			"dateEnd": "20250101",
          }
      ],
      "id": 485
  }'
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 485,
      "result": [
          {
              "proposalContent": {
                  "proposalId": "0x025d89a33667109e145cdcadcf33462d358d472d170000000000000000",
                  "proposalState": 1,
                  "Nonce": 0,
                  "contractAddress": "zltc_YsBiB4CrsFHXMmS9my5HZWswSR7jpaS6M",
                  "isRevoke": 3,
                  "period": 0
              },
              "ProposalType": 2
          }
      ]
  }
  ```

- 错误码

    - 无错误码

### wallet_getAllProposalId

#### 获取合约权限列表

- 获取所有提案的ID

- 请求参数

  {
      "dateStart"：开始时间（必填项）
  	"dateEnd": 结束时间（必填项）
  }

- 返回值

  - 提案ID列表

- 实例

  ```bash
  curl --location --request GET '192.168.2.12:9001' \
  --header 'Content-Type: text/plain' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getAllProposalId",
      "params": [
          {
         		"dateStart"："20250101",
  			"dateEnd": "20250101",
          }
      ],
      "id": 481
  }'
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": 
          [
              "0xc066797d84c2ec41b6e5dfa114ca84b57e51b19b2908222ba40cfd3cad09b814",
              "0xcf70c2238ab4bab2a1c83ee9ea31768d3070f5092f7019c650f3aac4e503bf68",
              "0xb704557725e81ad068007fd1d37fab257794bad0223c3042b89eeef3886889cb",
              "0xf6f697e652e0fbb3a4e405c44a53611799b58cce8fff8818459f4fb0ae486fda",
              "0x560574d55b96fe50c919950b8d5dc91d35edc17b3e882a6512833f16104c794d",
              "0x6076c5274ea4b13a61290bb579862ed3175e19d8cef91d7de35610cd1f8fbf3a",
              "0x966afb8b564173c54a8a674e573b16e109ead0c642b7c7f7228ae9496c696e25",
              "0x9d38707fba3328d6bbda44f6009310d2b3e4b6ee90441f50fb8687d33ab95d0b",
              "0xb516e728eae5121ac1fd7df52c6d2ea793bb7a9d3b4a206bd7ac57b57f294ea2",
              "0xf6184690a964067f28017287c7eb1503d476fa60a925a1d6f1efafdde41d9635"，
              "0x698922b82faf3d6befaa610ecadb46d45acd160dc5a5dcf8087831d760222b37"，
              "0x007e42cfc0e477e5af8f8e2841d13c5c9aa99d36e015e21fa96e19181c8cc3de"
          ]
      
  }
  ```

- 错误码

  - 无错误码

### wallet_getVoteById

#### 根据投票ID获取投票详细

- 请求参数

  {
      "voteId":  0x1234
  }

- 返回值

  - 投票详情

- 实例

  ```bash
  curl --location --request GET 'http://127.0.0.1:54006' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getVoteById",
      "params": [     			"0x04015188e430e42a9c14be15b1515465d0aa4382996400000000000000013230323430393034"
      ],
      "id": 481
  }'
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": {
          "voteId": "",
          "proposalId": "",
          "voteSuggestion": "",
          "address": "",
          "proposalType": "",
          "nonce": "",
          "createAt": ""
      }    
  }
  ```

- 错误码

  - 无错误码

### wallet_getVote

#### 根据投票ID获取投票详细

- 请求参数

  ```json
  {
      "owner":  账户地址（必填项）
      "suggestion": 投票建议（必填项，0：反对票 1：同意票 2：所有）
    	"dateStart"：开始时间（必填项）
  	"dateEnd": 结束时间（必填项）
  }
  ```

- 实例

  ```bash
  curl --location --request GET 'http://127.0.0.1:54006' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getVote",
      "params": [
          {
              "owner": "zltc_Xw6WF5iFFA2ujhj12DN6HRZ5wk2azEc1R",
              "suggestion": 2,
              "dateStart": "20240711",
              "dateEnd": "20240712"
          }
      ],
      "id": 485
  }'
  ```

- 返回值

  - 符合条件的投票id列表
  
- 返回值示例

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": [
          "0x04015188e430e42a9c14be15b1515465d0aa4382996400000000000000013230323430393034".
          "0x04015188e430e42a9c14be15b1515465d0aa4382996400000000000000013230323430393034"
      ]   
  }
  ```

- 错误码

  - 无错误码

## 1.2 提案发起（获取发起提案的code）

>通过下面这些接口获取Code后，通过code调用预置合约生产->提案ID

## 合约内部管理

### <span id="1">wallet_getContractInnerManagerCode</span>

#### 获取发起合约内部管理决策的Code

- 请求参数（顺序不能变）

    - 合约地址
    - 操作命令（3.2有详细说明操作命令）

- 返回值

    - code

- 实例

  ```bash
  curl --location --request GET '192.168.2.12:5001' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getContractInnerManagerCode",
      "params": [
          "zltc_RQ24mGatWkocpVEhWNS3Q6Q9xSBQ3Qkc6",
          "CWzltc_TbMJndAHmi4Z8WDnCEQX2uPzNctNFqPJd"
      ],
      "id": 481
  }'
  ```

- 返回值

  - code
  
- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": "0x65aba7570000000000000000000000000b9d798fe5a6df07f93a7a8a3e106b5ed5aa800a0000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000002843577a6c74635f54624d4a6e6441486d69345a3857446e434551583275507a4e63744e4671504a64000000000000000000000000000000000000000000000000"
  }
  ```

- 错误码

    - 无错误码

### <span id="1">wallet_getContractInnerManagerCode</span>

#### 获取发起初始化合约内部管理的code

- 请求参数（顺序不能变）

  ```
  {
      "contractAddress": "合约地址",
      "permissionList": {
          "permissionMode": 1,
          "threshold": 0,
          "blackList": [],
          "whiteList": [],
          "managerList": [
              {
                  "address": "zltc_Xmk6g2Lgxitrx4xEPUZgF4hHdnHwDcBuU",
                  "weight": 10
              }
          ]
      }
  }
  ```

- 实例

  ```bash
  curl --location --request GET 'http://127.0.0.1:54006' \
  --header 'chainId: 123' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getInitContractInnerManagerCode",
      "params": [
          {
              "contractAddress": "zltc_TArLkGjatNkY8X8uJTDwjw7qC2LR1rHcR",
              "permissionList": {
                  "permissionMode": 1,
                  "threshold": 0,
                  "blackList": [],
                  "whiteList": [],
                  "managerList": [
                     {
                          "address": "zltc_Xmk6g2Lgxitrx4xEPUZgF4hHdnHwDcBuU",
                          "weight": 10
                      }
                  ]
              }
          }
      ],
      "id": 481
  }'
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": "0x65aba7570000000000000000000000000b9d798fe5a6df07f93a7a8a3e106b5ed5aa800a0000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000002843577a6c74635f54624d4a6e6441486d69345a3857446e434551583275507a4e63744e4671504a64000000000000000000000000000000000000000000000000"
  }
  ```

- 错误码

  - 无错误码

## 合约生命周期

### <span id="2">wallet_getNewSuspendCode</span>

#### 获取合约生命周期的相关code

> eg. 吊销，解冻，冻结

- 请求参数（顺序不能变）

    - 合约地址
    - 0/1/2（4.2有详细说明操作命令）

- 返回值

    - code

- 实例

  ```bash
  curl --location --request GET '192.168.2.12:5001' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getNewSuspendCode",
      "params": [
          "zltc_RQ24mGatWkocpVEhWNS3Q6Q9xSBQ3Qkc6",
          1
      ],
      "id": 481
  }'
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": "0x65d4b8b50000000000000000000000000b9d798fe5a6df07f93a7a8a3e106b5ed5aa800a0000000000000000000000000000000000000000000000000000000000000001"
  }
  ```

- 错误码

    - 无错误码

## 链配置更改

### <span id="3">wallet_getChangePeriodCode</span>

#### 获取更改出块间隔的code

- 请求参数

    - 出块间隔（字符串）

- 返回值

    - code

- 实例

  ```bash
  curl --location --request GET '192.168.2.12:5001' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getChangePeriodCode",
      "params": [
          "3000"
      ],
      "id": 481
  }'
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": "0xa4bf13610000000000000000000000000000000000000000000000000000000000000bb8"
  }
  ```

- 错误码

    - 无错误码

### <span id="4">wallet_getAddLatcSaintCode</span>

#### 获取添加共识节点的code

- 请求参数

    - 合约地址的数组

- 返回值

    - code

- 实例

  ```bash
  curl --location --request GET '192.168.2.12:5001' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getAddLatcSaintCode",
      "params": [
          ["zltc_RQ24mGatWkocpVEhWNS3Q6Q9xSBQ3Qkc6"]
      ],
      "id": 481
  }'
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": "0x8bd24adc000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000b9d798fe5a6df07f93a7a8a3e106b5ed5aa800a"
  }
  ```

- 错误码

    - 无错误码

### <span id="5">wallet_getDelLatcSaintCode</span>

#### 获取删除共识节点的code

- 请求参数

    - 合约地址的数组

- 返回值

    - code

- 实例

  ```bash
  curl --location --request GET '192.168.2.12:5001' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getDelLatcSaintCode",
      "params": [
          ["zltc_RQ24mGatWkocpVEhWNS3Q6Q9xSBQ3Qkc6"]
      ],
      "id": 481
  }'
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": "0x08ce76a7000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000b9d798fe5a6df07f93a7a8a3e106b5ed5aa800a"
  }
  ```

- 错误码

    - 无错误码

### <span id="apiGetReplaceLatcSaintCode">wallet_getReplaceLatcSaintCode</span>

#### 获取替换共识节点的code

- 请求参数

  | 参数名   | 参数类型 |                  |
    | -------- | -------- | ---------------- |
  | oldSaint | 地址     | 原共识节点地址   |
  | newSaint | 地址     | 新的共识节点地址 |

- 返回值

    - code

- 实例

  ```bash
  curl --location --request GET 'http://192.168.2.12:5001' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getReplaceLatcSaintCode",
      "params": [
         {
           "oldSaint": "zltc_g2L1GFdBZW6wHRBs1uZNDWeHjvMErzwri",
           "newSaint": "zltc_Xmk6g2Lgxitrx4xEPUZgF4hHdnHwDcBuU"
         }
      ],
      "id": 481
  }'
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": "0x08ce76a7000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000b9d798fe5a6df07f93a7a8a3e106b5ed5aa800a"
  }
  ```

- 错误码

    - 无错误码

### <span id="apiGetReplaceLatcSaintCode">wallet_getReplacePreacherCode</span>

#### 获取替换盟主的code

- 请求参数

  | 参数名   | 参数类型 |                    |
    | -------- | -------- | ------------------ |
  | oldSaint | 地址     | 原盟主节点地址     |
  | newSaint | 地址     | 新的原盟主节点地址 |

- 返回值

    - code

- 实例

  ```bash
  curl --location --request GET 'http://192.168.2.12:5001' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getReplacePreacherCode",
      "params": [
         {
           "oldSaint": "zltc_g2L1GFdBZW6wHRBs1uZNDWeHjvMErzwri",
           "newSaint": "zltc_Xmk6g2Lgxitrx4xEPUZgF4hHdnHwDcBuU"
         }
      ],
      "id": 481
  }'
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": "0x08ce76a7000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000b9d798fe5a6df07f93a7a8a3e106b5ed5aa800a"
  }
  ```

- 错误码

    - 无错误码

### <span id="apiChangeNoEmptyAnchor">wallet_getChangeNoEmptyAnchor</span>

#### 获取更改合约无交易增加出块时间开关的code

- 请求参数

    - true/false (开启或关闭无交易增加出块时间)

- 返回值

    - code

- 实例

  ```bash
  {
      "jsonrpc": "2.0",
      "method": "wallet_getChangeNoEmptyAnchor",
      "params": [
          true
      ],
      "id": 481
  }
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": "0x4864b6ef0000000000000000000000000000000000000000000000000000000000000001"
  }
  ```

- 错误码

    - 无错误码

### <span id="apiGetSwitchContractPermission">wallet_getSwitchContractPermission</span>

#### 获取开关合约内部管理的code

- 请求参数

    - true/false

- 返回值

    - code

- 实例

  ```bash
  {
      "jsonrpc": "2.0",
      "method": "wallet_getSwitchContractPermission",
      "params": [
          true
      ],
      "id": 481
  }
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": "0x6bbb4f0a0000000000000000000000000000000000000000000000000000000000000001"
  }
  ```

- 错误码

    - 无错误码

### <span id="apiGetChangeContractLifecycleRule">wallet_getChangeContractLifecycleRule</span>

#### 获取修改合约生命周期规则的code

- 请求参数

    - 规则值（整数）

- 返回值

    - code

- 实例

  ```bash
  curl --location --request GET 'http://192.168.2.12:5001' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getChangeContractLifecycleRule",
      "params": [
          2
      ],
      "id": 481
  }'
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": "0x12345678000000000000000000000000000000000000000000000000000000000000002"
  }
  ```

- 错误码

    - 无错误码

### <span id="apiGetChangeContractFreezeRule">wallet_getChangeContractFreezeRule</span>

#### 获取修改合约冻结规则的code

- 请求参数

    - 规则值（整数）

- 返回值

    - code

- 实例

  ```bash
  curl --location --request GET 'http://192.168.2.12:5001' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getChangeContractFreezeRule",
      "params": [
          1
      ],
      "id": 481
  }'
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": "0x87654321000000000000000000000000000000000000000000000000000000000000001"
  }
  ```

- 错误码

    - 无错误码

## 1.3 提案决策

### <span id="7">wallet_getVoteCode</span>

#### 获取提案投票code

- 请求参数

    - 提案ID（字符串）
    - 0/1 （反对/同意）

- 返回值

    - code

- 实例

  ```bash
  curl --location --request GET '192.168.2.12:5001' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getVoteCode",
      "params": [
          "123132131",
          1
      ],
      "id": 481
  }'
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": "0x90ca27f30000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000093132333133323133310000000000000000000000000000000000000000000000"
  }
  ```

- 错误码

    - 无错误码

### <span id="8">wallet_getRefreshCode</span>

#### 获取提案投票刷新的code，用来刷新提案的结果

- 请求参数

    - 提案ID（字符串）

- 返回值

    - code

- 实例

  ```bash
  curl --location --request GET '192.168.2.12:5001' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getVoteCode",
      "params": [
          "123132131"
      ],
      "id": 481
  }'
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": "0x90ca27f30000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000093132333133323133310000000000000000000000000000000000000000000000"
  }
  ```

- 错误码

    - 无错误码

### <span id="apiGetCancelCode">wallet_getCancelCode</span>

#### 获取取消提案的code

- 请求参数

    - 提案ID（字符串）

- 返回值

    - code

- 实例

  ```bash
  curl --location --request GET 'http://192.168.2.12:5001' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getCancelCode",
      "params": [
          "0x025d89a33667109e145cdcadcf33462d358d472d170000000000000000"
      ],
      "id": 481
  }'
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": "0x90ca27f30000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000093132333133323133310000000000000000000000000000000000000000000000"
  }
  ```

- 错误码

    - 无错误码

### <span id="apiGetChangeProposalExpireTime">wallet_getChangeProposalExpireTime</span>

#### 获取修改提案过期时间的code

- 请求参数

    - 过期时间 （单位：天）

- 返回值

    - code

- 实例

  ```bash
  curl --location --request GET 'http://192.168.31.26:5001' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_getChangeProposalExpireTime",
      "params": [
          1
      ],
      "id": 481
  }'
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": "0x90ca27f30000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000000093132333133323133310000000000000000000000000000000000000000000000"
  }
  ```

- 错误码

    - 无错误码