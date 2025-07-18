# 预编译合约地址查询

|            | version           | 预置合约                         | 作用           | abi.json | 合约地址（zltc格式）                   | 合约地址（16进制格式）                     |
|------------------------------|--------------| -------- | -------------------------------------- | ------------------------------------------ |------------------------------|------------------------------|
| 1         | Pangu          | ecRecover                    | 处理签名         | 无       | zltc_QLbz7JHiBTspS962RLKV8GndWFwvRkSQw | 0x0000000000000000000000000000000000000001 |
| 2                  |                    | sha256hash                   | sha256有关     | 无       | zltc_QLbz7JHiBTspS962RLKV8GndWFwzymNiD | 0x0000000000000000000000000000000000000002 |
| 3                    |                      | revokeCA                     | 吊销证书         | 无       | zltc_Zg7ABDjrPiwGuLxjJPyrJsXq4pEzjQWDc | 0x66696361746541757468656E7469636174696f6e |
| 4                        |                          | Vote                         | 合约投票         | 无       | zltc_QLbz7JHiBTt54PGNLvRebZ5hpzzWfkPAj | 0x0000000000000000766f7465436F6E7472616374 |
| 5          |            | LaunchContractVote           | 发起合约冻结 解冻 吊销 | 无       | zltc_QLcLqfuBGSfrqt9kt8DHEVNFB4JSdQxhb | 0x00004C61756E6368436F6e7472616374566f7465 |
| 6            |              | transGenesisNode             | 布道者节点转移      | 无       | zltc_QLbz7KuobbCCQQBBY7JMsXsvFZH7jDnd7 | 0x000000007472616e7347656E657369734E6f6465 |
| 7         | Nuwa          | Credibility                  | 存证溯源         | 有       | zltc_QLbz7JHiBTspUvTPzLHy5biDS9mu53mmv | 0x000000000000000000637265646962696C697479 |
| 8                  |                    | BusinessId                   | 生成业务地址       | 无       | zltc_QLbz7JHiBTspS9WTWJUrbNsB5wbENMweQ | 0x00000000000000000000427573696e6573734964 |
| 9                      |                        | Oracle                       | 预言机合约        | 有       | zltc_amPge82fy3fJsLD1eSerqCBEfgjpU43S4 | 0x7261636C65436f6E747261637441646472657373 |
| 10                   |                      | Identity                     | 身份合约         | 有       | zltc_aQdmesGLjoJ5FJ65t2F7Nf9tTAT2C3dxA | 0x6e74697479436F6e747261637441646472657373 |
| 11                   |                      | Peekaboo                     | 哈希隐藏         | 有       | zltc_a8Nx2gcs2XHye7MKVWykdanumqDkWXqRH | 0x6B61626f6f436f6E747261637441646472657373 |
| 12 |  | DistributedStroage |  |  | zltc_ZwptHk17UU4wojKDwywJ3hfB9ihvUhjAq | 0x6962757465645374726f61676541646472657373 |
| 13          |             | BaseCrossContract            | 基础跨链业务合约     | 无       | zltc_WVEM51V8cbusa32mqQs2qABrt4KdQNToB | 0x43726f7373436F6E747261637441646472657373 |
| 14 |  | paymentOnBehalf |  |  | zltc_QLbz7JJ4kjfD2SKmKXbbNvA6QBFWmCsLy | 0x00000000007061796d656E744f6E426568616c66 |
| 15 | Taiyi | ContractInnerManagerProposal | 合约内部管理提案     | 有       | zltc_ZDdPo8P72X7dtMNTxBeKU8pT7bDXb7NtV | 0x6167655f70726f706F73616C5F61646472657373 |
| 16  |     | ContractLifecycleProposal | 合约生命周期提案     | 有       | zltc_ZQJjaw74CKMjqYJFMKdEDaNTDMq5QKi3T | 0x636c655f70726F706f73616C5F61646472657373 |
| 17       |          | ModifyConfigProposal | 链配置更改提案      | 有       | zltc_ZwuhH4dudz2Md2h6NFgHc8yrFUhKy2UUZ | 0x6966795f70726F706f73616c5F61646472657373 |
| 18               |                  | ProposalVote     | 提案投票         | 有       | zltc_amgWuhifLRUoZc3GSbv9wUUz6YUfTuWy5 | 0x726f706f73616c5F766f74655F61646472657373 |
| 19       |          | ChainByChainProposal | 以链建链提案       | 有       | zltc_ZDfqCd4ZbBi4WA7uG4cGpFWRyTFqzyHUn | 0x61696e5f62795f636861696E5f61646472657373 |
| 20 |  | Tpre | []() |  | zltc_QLbz7JHiBTspVQ2d8UCmyL1PGWzZnrVHJ | 0x0000000000000000007470726541646472657373 |
| 21          |              | NodeCertContract | 节点证书合约       | 有       | zltc_QLbz7JHxYJDL9LAguz9rKrwNtmfY2UoAZ | 0x00000000004e6f64654365727441646472657373 |

## Credibility

```
				"internalType": "bytes32",
				"name": "_requestId",
				"type": "bytes32"
			},
			{
				"internalType": "bytes",
				"name": "_input",
				"type": "bytes"
			},
			{
				"internalType": "string",
				"name": "_data",
				"type": "string"
			}
		],
		"name": "responseOracle",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			},
			{
				"internalType": "bytes",
				"name": "data",
				"type": "bytes"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]
```



## Identity


```
[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_oldAddress",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "_newAddress",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "_data",
				"type": "string"
			}
		],
		"name": "changeIdentity",
		"outputs": [],
		"stateMutability": "pure",
		"type": "function"
	}
]
```



## Peekaboo

```
[
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "_hash",
				"type": "bytes32"
			}
		],
		"name": "addHash",
		"outputs": [],
		"stateMutability": "pure",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "_hash",
				"type": "bytes32"
			}
		],
		"name": "delHash",
		"outputs": [],
		"stateMutability": "pure",
		"type": "function"
	}
]
```

## ContractInnerManagerProposal

```json
[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "Address",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "operation",
				"type": "string"
			}
		],
		"name": "launch",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "pure",
		"type": "function"
	},
 {
    "inputs": [
      {
        "internalType": "address",
        "name": "Address",
        "type": "address"
      },
      {
        "components": [
          {
            "internalType": "uint8",
            "name": "permissionMode",
            "type": "uint8"
          },
          {
            "internalType": "uint64",
            "name": "threshold",
            "type": "uint64"
          },
          {
            "internalType": "address[]",
            "name": "blackList",
            "type": "address[]"
          },
          {
            "internalType": "address[]",
            "name": "whiteList",
            "type": "address[]"
          },
          {
            "components": [
              {
                "internalType": "address",
                "name": "Address",
                "type": "address"
              },
              {
                "internalType": "uint8",
                "name": "weight",
                "type": "uint8"
              }
            ],
            "internalType": "struct chainbychain.Manager[]",
            "name": "managerList",
            "type": "tuple[]"
          }
        ],
        "internalType": "struct chainbychain.Args",
        "name": "permissionList",
        "type": "tuple"
      }
    ],
    "name": "init",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
```

## ContractLifecycleProposal

```json
[
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "Period",
                "type": "uint256"
            }
        ],
        "name": "changePeriod",
        "outputs": [
            {
                "internalType": "bytes",
                "name": "",
                "type": "bytes"
            }
        ],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address[]",
                "name": "LatcSaint",
                "type": "address[]"
            }
        ],
        "name": "addLatcSaint",
        "outputs": [
            {
                "internalType": "bytes",
                "name": "",
                "type": "bytes"
            }
        ],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [
            {
            "components": [
			  {
				"internalType": "bytes",
				"name": "publicKey",	
				"type": "bytes"
  			  }
            ],
            "internalType": "struct UploadKeyParam[]",
            "name": "nodes",
            "type": "tuple[]"
          }
        ],
        "name": "addLatcSaintNew",
        "outputs": [
            {
                "internalType": "bytes",
                "name": "",
                "type": "bytes"
            }
        ],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address[]",
                "name": "LatcSaint",
                "type": "address[]"
            }
        ],
        "name": "delLatcSaint",
        "outputs": [
            {
                "internalType": "bytes",
                "name": "",
                "type": "bytes"
            }
        ],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "oldSaint",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "newSaint",
                "type": "address"
            }
        ],
        "name": "replaceLatcSaint",
        "outputs": [
            {
                "internalType": "bytes",
                "name": "",
                "type": "bytes"
            }
        ],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "oldSaint",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "newSaint",
                "type": "address"
            }
        ],
        "name": "replacePreacher",
        "outputs": [
            {
                "internalType": "bytes",
                "name": "",
                "type": "bytes"
            }
        ],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "oldSaint",
                "type": "address"
            },
			{
				"internalType": "bytes",
				"name": "publicKey",	
				"type": "bytes"
		}
        ],
        "name": "replaceLatcSaintNew",
        "outputs": [
            {
                "internalType": "bytes",
                "name": "",
                "type": "bytes"
            }
        ],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bool",
                "name": "contractPermission",
                "type": "bool"
            }
        ],
        "name": "switchContractPermission",
        "outputs": [
            {
                "internalType": "bytes",
                "name": "",
                "type": "bytes"
            }
        ],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "Consensus",
                "type": "string"
            }
        ],
        "name": "switchConsensus",
        "outputs": [
            {
                "internalType": "bytes",
                "name": "",
                "type": "bytes"
            }
        ],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bool",
                "name": "noEmptyAnchor",
                "type": "bool"
            }
        ],
        "name": "switchNoEmptyAnchor",
        "outputs": [
            {
                "internalType": "bytes",
                "name": "",
                "type": "bytes"
            }
        ],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint64",
                "name": "emptyAnchorPeriodMul",
                "type": "uint64"
            }
        ],
        "name": "changeEmptyAnchorPeriodMul",
        "outputs": [],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint64",
                "name": "proposalExpireTime",
                "type": "uint64"
            }
        ],
        "name": "changeProposalExpireTime",
        "outputs": [],
        "stateMutability": "pure",
        "type": "function"
    },
    {
		"inputs": [
		  {
			"internalType": "uint8",
			"name": "chainByChainVote",
			"type": "uint8"
		  }
		],
		"name": "changeChainByChainVote",
		"outputs": [],
		"stateMutability": "pure",
		"type": "function"
	},
    {
		"inputs": [
		  {
			"internalType": "uint8",
			"name": "rule",
			"type": "uint8"
		  }
		],
		"name": "changeContractLifecycleRule",
		"outputs": [],
		"stateMutability": "pure",
		"type": "function"
	},
    {
		"inputs": [
		  {
			"internalType": "uint8",
			"name": "rule",
			"type": "uint8"
		  }
		],
		"name": "changeContractFreezeRule",
		"outputs": [],
		"stateMutability": "pure",
		"type": "function"
	}
]
```

## ModifyConfigProposal

```json
[
  {
    "inputs": [
      {
        "internalType": "uint256",
        "name": "Period",
        "type": "uint256"
      }
    ],
    "name": "changePeriod",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address[]",
        "name": "LatcSaint",
        "type": "address[]"
      }
    ],
    "name": "addLatcSaint",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "components": [
          {
            "internalType": "bytes",
            "name": "publicKey",
            "type": "bytes"
          }
        ],
        "internalType": "struct UploadKeyParam[]",
        "name": "nodes",
        "type": "tuple[]"
      }
    ],
    "name": "addLatcSaintNew",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address[]",
        "name": "LatcSaint",
        "type": "address[]"
      }
    ],
    "name": "delLatcSaint",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "oldSaint",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "newSaint",
        "type": "address"
      }
    ],
    "name": "replaceLatcSaint",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "oldSaint",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "newSaint",
        "type": "address"
      }
    ],
    "name": "replacePreacher",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "oldSaint",
        "type": "address"
      },
      {
        "internalType": "bytes",
        "name": "publicKey",
        "type": "bytes"
      }
    ],
    "name": "replaceLatcSaintNew",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bool",
        "name": "IsDictatorship",
        "type": "bool"
      }
    ],
    "name": "isDictatorship",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bool",
        "name": "isContractVote",
        "type": "bool"
      }
    ],
    "name": "switchIsContractVote",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bool",
        "name": "contractPermission",
        "type": "bool"
      }
    ],
    "name": "switchContractPermission",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "Consensus",
        "type": "string"
      }
    ],
    "name": "switchConsensus",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "bool",
        "name": "noEmptyAnchor",
        "type": "bool"
      }
    ],
    "name": "switchNoEmptyAnchor",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint64",
        "name": "emptyAnchorPeriodMul",
        "type": "uint64"
      }
    ],
    "name": "changeEmptyAnchorPeriodMul",
    "outputs": [],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint64",
        "name": "proposalExpireTime",
        "type": "uint64"
      }
    ],
    "name": "changeProposalExpireTime",
    "outputs": [],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint8",
        "name": "chainByChainVote",
        "type": "uint8"
      }
    ],
    "name": "changeChainByChainVote",
    "outputs": [],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint8",
        "name": "rule",
        "type": "uint8"
      }
    ],
    "name": "changeContractLifecycleRule",
    "outputs": [],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint8",
        "name": "rule",
        "type": "uint8"
      }
    ],
    "name": "changeContractFreezeRule",
    "outputs": [],
    "stateMutability": "pure",
    "type": "function"
  }
]
```

## ProposalVote

```json
[
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "ProposalId",
        "type": "string"
      },
      {
        "internalType": "uint8",
        "name": "VoteSuggestion",
        "type": "uint8"
      }
    ],
    "name": "vote",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },{
    "inputs": [
      {
        "internalType": "string",
        "name": "ProposalId",
        "type": "string"
      },
      {
        "internalType": "bytes",
        "name": "sign",
        "type": "bytes"
      },
      {
        "internalType": "address",
        "name": "from",
        "type": "address"
      }
    ],
    "name": "signVote",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },{
    "inputs": [
      {
        "internalType": "string",
        "name": "ProposalId",
        "type": "string"
      }
    ],
    "name": "refresh",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string[]",
        "name": "proposalIds",
        "type": "string[]"
      }
    ],
    "name": "batchRefresh",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "string",
        "name": "proposalId",
        "type": "string"
      }
    ],
    "name": "cancel",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  }
]
```

## ChainByChainProposal

```json
[
	{
		"inputs": [
			{
				"internalType": "uint64",
				"name": "chainId",
				"type": "uint64"
			}
		],
		"name": "delChain",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"components": [
					{
						"internalType": "uint8",
						"name": "consensus",
						"type": "uint8"
					},
					{
						"internalType": "bool",
						"name": "tokenless",
						"type": "bool"
					},
					{
						"internalType": "uint256",
						"name": "godAmount",
						"type": "uint256"
					},
					{
						"internalType": "uint64",
						"name": "period",
						"type": "uint64"
					},
					{
						"internalType": "bool",
						"name": "noEmptyAnchor",
						"type": "bool"
					},
					{
						"internalType": "uint64",
						"name": "emptyAnchorPeriodMul",
						"type": "uint64"
					},
					{
						"internalType": "bool",
						"name": "isContractVote",
						"type": "bool"
					},
					{
						"internalType": "bool",
						"name": "isDictatorship",
						"type": "bool"
					},
					{
						"internalType": "uint8",
						"name": "deployRule",
						"type": "uint8"
					},
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "chainId",
						"type": "string"
					},
					{
						"internalType": "address",
						"name": "preacher",
						"type": "address"
					},
					{
						"internalType": "string",
						"name": "bootStrap",
						"type": "string"
					},
					{
						"components": [
							{
								"internalType": "address",
								"name": "member",
								"type": "address"
							},
							{
								"internalType": "uint8",
								"name": "memberType",
								"type": "uint8"
							}
						],
						"internalType": "struct chainbychain.ChainMember[]",
						"name": "chainMemberGroup",
						"type": "tuple[]"
					}
				],
				"internalType": "struct chainbychain.Args",
				"name": "args",
				"type": "tuple"
			}
		],
		"name": "newChain",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint64",
				"name": "chainId",
				"type": "uint64"
			},
			{
				"internalType": "uint64",
				"name": "networkId",
				"type": "uint64"
			},
			{
				"internalType": "string",
				"name": "nodeInfo",
				"type": "string"
			},
			{
				"internalType": "address[]",
				"name": "accessMembers",
				"type": "address[]"
			}
		],
		"name": "oldChain",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint64",
				"name": "chainId",
				"type": "uint64"
			}
		],
		"name": "stopChain",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint64",
				"name": "chainId",
				"type": "uint64"
			}
		],
		"name": "startChain",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]
```

## NodeCertContract

```json
[
  {
    "inputs": [
      {
        "internalType": "uint8",
        "name": "certType",
        "type": "uint8"
      },
      {
        "internalType": "string",
        "name": "orgName",
        "type": "string"
      },
      {
        "components": [
          {
            "internalType": "address",
            "name": "address",
            "type": "address"
          }
        ],
        "internalType": "struct ApplyCert[]",
        "name": "nodes",
        "type": "tuple[]"
      }
    ],
    "name": "apply",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },{
    "inputs": [
      {
        "internalType": "uint8",
        "name": "certType",
        "type": "uint8"
      },
      {
        "internalType": "string",
        "name": "orgName",
        "type": "string"
      },
      {
        "components": [
          {
            "internalType": "address",
            "name": "address",
            "type": "address"
          }
        ],
        "internalType": "struct ApplyCert[]",
        "name": "nodes",
        "type": "tuple[]"
      }
    ],
    "name": "apply",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "uint256[]",
        "name": "serialNumber",
        "type": "uint256[]"
      }
    ],
    "name": "revoke",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "components": [
          {
            "internalType": "bytes",
            "name": "publicKey",
            "type": "bytes"
          }
        ],
        "internalType": "struct UploadKeyParam[]",
        "name": "nodes",
        "type": "tuple[]"
      }
    ],
    "name": "uploadKey",
    "outputs": [
      {
        "internalType": "bytes",
        "name": "",
        "type": "bytes"
      }
    ],
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "inputs": [
      {
        "components": [
          {
            "internalType": "string",
            "name": "OrgName",
            "type": "string"
          },
          {
            "internalType": "uint8",
            "name": "CertType",
            "type": "uint8"
          },
          {
            "components": [
              {
                "internalType": "bytes",
                "name": "PublicKey",
                "type": "bytes"
              }
            ],
            "internalType": "struct nodeCert.UploadKeyParam[]",
            "name": "Applies",
            "type": "tuple[]"
          }
        ],
        "internalType": "struct nodeCert.UpAndApplyParam",
        "name": "param",
        "type": "tuple"
      }
    ],
    "name": "upAndApply",
    "outputs": [],
    "stateMutability": "pure",
    "type": "function"
  }
]
```

