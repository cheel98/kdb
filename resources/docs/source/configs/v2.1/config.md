# 节点配置文件

<script setup>
// 定义版本列表，适用于所有配置文件页面
const configVersions = [
  { name: 'v2.1', link: '/docs/source/configs/v2.1/config' },
  { name: 'v2.2', link: '/docs/source/configs/v2.2/config' }
];
</script>

<VersionSwitcher 
  currentVersion="v2.1" 
  :versions="configVersions"
/>

本文档描述了晶格链 v2.1 版本的节点配置文件格式和参数说明。

## 配置文件结构

```json
{
  "Node": {
    "DataDir": "/path/to/data",
    "KeyFile": "/path/to/key",
    "P2P": {
      "ListenAddress": "0.0.0.0:26656",
      "Seeds": ["seed1.example.com:26656", "seed2.example.com:26656"]
    }
  },
  "Log": {
    "Level": "info",
    "Format": "json"
  }
}
```

## 参数说明

### Node 部分

| 参数 | 说明 | 默认值 |
| --- | --- | --- |
| DataDir | 数据存储目录 | ./data |
| KeyFile | 节点密钥文件路径 | ./nodekey |

### P2P 部分

| 参数 | 说明 | 默认值 |
| --- | --- | --- |
| ListenAddress | P2P 监听地址 | 0.0.0.0:26656 |
| Seeds | 种子节点列表 | [] |

### Log 部分

| 参数 | 说明 | 可选值 |
| --- | --- | --- |
| Level | 日志级别 | debug, info, warn, error |
| Format | 日志格式 | text, json |
