# 1.Value include Proof数据存在证明

## 1.1 接口说明

### wallet_getValueProof

#### 获取MPT证明路径

- 获取存证数据的MPT证明路径

- 请求参数

    - addr：业务地址
    - key: 存证数据dataId

- 返回值

    - 证明路径

- 实例

  ```bash
  curl --location --request GET 'http://112.26.202.82:16001' \
  --header 'Content-Type: application/json' \
  --data '{
      "id": 481,
      "jsonrpc": "2.0",
      "method": "wallet_getValueProof",
      "params": [
          {"addr": "zltc_YBomBNykwMqxm719giBL3VtYV4ABT9a8D",
      "key": "0xA98F6k5QgrIuI7NzSglK0IvCKAJc5fHrSmAMMq6C92PgfV2scpMlK4DOZ9CH1yuT"
      }]
  }'
  ```

- 返回结果

  ```json
  {
      "jsonRpc": "2.0",
      "id": 481,
      "result": {
          "flag": true,
          "rootHash": "0x1174c72b3701bd90a7df9aa989ee067afda0d41e41e38dd4b982b3a35e35c619",
          "address": "zltc_YBomBNykwMqxm719giBL3VtYV4ABT9a8D",
          "accountProof": [
              {
                  "Node": "1174c72b3701bd90a7df9aa989ee067afda0d41e41e38dd4b982b3a35e35c619",
                  "NodeData": "f89180808080a08555957871998317532466b862da8693d0fcfe4facc1d1da9c52b91f1d0ea6a0808080a0d1759d45e4730fb83490fb57c6eae9cc4e4e5b1718cd34159ea899c00b364ec78080a02e1077c1b90f8f20df0f5eb426f564318200cf9688fc0723d63aad5f8034df09808080a0315da79d5637c1a4bd93d92ca849eb6584c4183d64ba726f578f2aeb4767de6180"
              },
              {
                  "Node": "d1759d45e4730fb83490fb57c6eae9cc4e4e5b1718cd34159ea899c00b364ec7",
                  "NodeData": "f851808080808080808080a047f588875fe392380a21d2a5b00bcae5cfbeb970f18a6863537dcd538995cb6a80a0fd15a9ee40b6996d32e67cb8e8902307cd3cf2c94d5f1cee5ef0fe13b7575cc88080808080"
              },
              {
                  "Node": "47f588875fe392380a21d2a5b00bcae5cfbeb970f18a6863537dcd538995cb6a",
                  "NodeData": "f876a020ab51c7e514a97c8de4e7d92c4ba19aeceac72e9eacb9ad6c2d6a8e3d299a2fb853f85103b84ef84c808080e1a0e0d173b4b1c75053dc19ca4ad58298de909964c40f5233815d7d4221709610df8080e1a023a40d9f445921d8fb9e9b31f222fac76678edd59d68fec5dc7c03dbb3588eef808003"
              }
          ],
          "storageHash": "0xe0d173b4b1c75053dc19ca4ad58298de909964c40f5233815d7d4221709610df",
          "storageProof": {
              "Key": "0xA98F6k5QgrIuI7NzSglK0IvCKAJc5fHrSmAMMq6C92PgfV2scpMlK4DOZ9CH1yuT",
              "Value": "0xf828353545629dbc3e31520e5f07274fced954f641db7e827f7e95c1365d1ab7",
              "Proof": [
                  {
                      "Node": "e0d173b4b1c75053dc19ca4ad58298de909964c40f5233815d7d4221709610df",
                      "NodeData": "f844a120507a7540b608705d950a8e87932c7f8f69983eab83d76e6be51b68eb428a2f78a1a0f828353545629dbc3e31520e5f07274fced954f641db7e827f7e95c1365d1ab7"
                  }
              ]
          },
          "value": "https://t7.baidu.com/it/u=2168645659,3174029352&fm=193&f=GIF",
          "evidence": [
              {
                  "Number": 198,
                  "Protocol": 98784247809,
                  "Updater": "zltc_Xmk6g2Lgxitrx4xEPUZgF4hHdnHwDcBuU",
                  "Data": [
                      [
                          
                      ]
                  ]
              }
          ]
      }
  }
  ```

- 错误码

    - -32000 数据不存在

      ```json
      {
          "jsonRpc": "2.0",
          "id": 481,
          "error": {
              "code": -32000,
              "message": "Value is not exists: [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]"
          }
      }
      ```

### wallet_verifyProof

#### 获取MPT证明路径

- 验证MPT证明路径

- 请求参数

    - rootHash：MPT树 根hash
    - address:  业务地址
    - accountProof： 账户证明路径
    - storageHash：存储树 根hash
    - storageProof：存储树证明路径

- 返回值

    - 数据存储Hash

- 实例

  ```bash
  curl --location --request GET '112.26.202.82:16001' \
  --header 'Content-Type: application/json' \
  --data '{
      "jsonrpc": "2.0",
      "method": "wallet_verifyProof",
      "params": [
          {
           "rootHash": "0x1174c72b3701bd90a7df9aa989ee067afda0d41e41e38dd4b982b3a35e35c619",
          "address": "zltc_YBomBNykwMqxm719giBL3VtYV4ABT9a8D",
          "accountProof": [
              {
                  "Node": "1174c72b3701bd90a7df9aa989ee067afda0d41e41e38dd4b982b3a35e35c619",
                  "NodeData": "f89180808080a08555957871998317532466b862da8693d0fcfe4facc1d1da9c52b91f1d0ea6a0808080a0d1759d45e4730fb83490fb57c6eae9cc4e4e5b1718cd34159ea899c00b364ec78080a02e1077c1b90f8f20df0f5eb426f564318200cf9688fc0723d63aad5f8034df09808080a0315da79d5637c1a4bd93d92ca849eb6584c4183d64ba726f578f2aeb4767de6180"
              },
              {
                  "Node": "d1759d45e4730fb83490fb57c6eae9cc4e4e5b1718cd34159ea899c00b364ec7",
                  "NodeData": "f851808080808080808080a047f588875fe392380a21d2a5b00bcae5cfbeb970f18a6863537dcd538995cb6a80a0fd15a9ee40b6996d32e67cb8e8902307cd3cf2c94d5f1cee5ef0fe13b7575cc88080808080"
              },
              {
                  "Node": "47f588875fe392380a21d2a5b00bcae5cfbeb970f18a6863537dcd538995cb6a",
                  "NodeData": "f876a020ab51c7e514a97c8de4e7d92c4ba19aeceac72e9eacb9ad6c2d6a8e3d299a2fb853f85103b84ef84c808080e1a0e0d173b4b1c75053dc19ca4ad58298de909964c40f5233815d7d4221709610df8080e1a023a40d9f445921d8fb9e9b31f222fac76678edd59d68fec5dc7c03dbb3588eef808003"
              }
          ],
          "storageHash": "0xe0d173b4b1c75053dc19ca4ad58298de909964c40f5233815d7d4221709610df",
          "storageProof": {
              "Key": "0xA98F6k5QgrIuI7NzSglK0IvCKAJc5fHrSmAMMq6C92PgfV2scpMlK4DOZ9CH1yuT",
              "Value": "0xf828353545629dbc3e31520e5f07274fced954f641db7e827f7e95c1365d1ab7",
              "Proof": [
                  {
                      "Node": "e0d173b4b1c75053dc19ca4ad58298de909964c40f5233815d7d4221709610df",
                      "NodeData": "f844a120507a7540b608705d950a8e87932c7f8f69983eab83d76e6be51b68eb428a2f78a1a0f828353545629dbc3e31520e5f07274fced954f641db7e827f7e95c1365d1ab7"
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
      "result": {
          "value": "0xf828353545629dbc3e31520e5f07274fced954f641db7e827f7e95c1365d1ab7"
      }
  }
  ```

- 错误码

    - -32000 数据不存在

      ```json
      {
          "jsonRpc": "2.0",
          "id": 481,
          "error": {
              "code": -32000,
              "message": "value is nil"
          }
      }
      ```
