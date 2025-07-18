# 链相关

## latc_startZLattice

### 启动链

- 请求参数

    - 无参数

- 返回值

    - 启动失败的error信息或空（为空则启动成功）

- 实例

  ```bash
  curl 127.0.0.1:3004 -X POST -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1234567890",
    "method": "latc_startZLattice",
    "params": []
  }'
  ```

- 返回结果

  ```json
  {
    "jsonrpc": "2.0",
    "id": "1234567890",
    "result": null
  }
  ```
