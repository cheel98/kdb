# 区块版本变更历史

## 盘古

版本号： 1.0

区块数据结构

### TBlock

```go
type TBlock struct {
	header *THeader
	body   *TBody

	hash    atomic.Value
	size    atomic.Value
	chainId *big.Int
	wp      *big.Int

	ReceivedAt time.Time
}
```

### TBlock区块头

```go
type THeaderPangu struct {
	Number      *big.Int       `json:"Number" gencodec:"required"`
	Type        uint8          `json:"Type" gencodec:"required"`
	ParentHash  common.Hash    `json:"parentHash" gencodec:"required"`
	DaemonHash  common.Hash    `json:"daemonHash" gencodec:"required"`
	CodeHash    common.Hash    `json:"codeHash" gencodec:"required"`
	Owner       common.Address `json:"owner" gencodec:"required"`
	Linker      common.Address `json:"linker"`
	Hub         []common.Hash  `json:"hub"`
	Amount      *big.Int       `json:"value"`
	Income      *big.Int       `json:"income"`
	Joule       uint64         `json:"joule"`
	Difficulty  uint64         `json:"difficulty" gencodec:"required"`
	ProofOfWork *big.Int       `json:"proofOfWork" gencodec:"required"`
	Payload     []byte         `json:"payload" gencodec:"required"`
	Timestamp   uint64         `json:"timestamp" gencodec:"required"`

	// Signature values
	E *big.Int `json:"e"   gencodec:"required"`
	V *big.Int `json:"v"   gencodec:"required"`
	R *big.Int `json:"r"   gencodec:"required"`
	S *big.Int `json:"s"   gencodec:"required"`
}
```

### TBlock 区块体

```go
type TBodyPangu struct {
	Code    *Code    `json:"code"`
	Balance *big.Int `json:"balance" gencodec:"required"`
	Deposit *big.Int `json:"deposit" gencodec:"required"`
	Record  uint64   `json:"record" gencodec:"required"`
	Nonce   *big.Int `json:"nonce" gencodec:"required"`
	Td      *big.Int `json:"td" gencodec:"required"`
}
```

### DBlock

```go
type DBlockNuwa struct {
	Header *DHeader
	Body   *DBody
}
```

### DBlock 区块头

```go
type DHeaderPangu struct {
	Number      *big.Int       `json:"Number" gencodec:"required"`
	Coinbase    common.Address `json:"miner" gencodec:"required"`
	ParentHash  common.Hash    `json:"parentHash" gencodec:"required"`
	LedgerHash  common.Hash    `json:"ledgerRoot" gencodec:"required"`
	ReceiptHash common.Hash    `json:"receiptHash" gencodec:"required"`
	Difficulty  *big.Int       `json:"difficulty" gencodec:"required"`
	Pow         *big.Int       `json:"pow" gencodec:"required"`
	Extra       []byte         `json:"extra" gencodec:"required"`
	Timestamp   uint64         `json:"timestamp" gencodec:"required"`
}
```

### DBlock区块体

```go
type DHeaderPangu struct {
	Number      *big.Int       `json:"Number" gencodec:"required"`
	Coinbase    common.Address `json:"miner" gencodec:"required"`
	ParentHash  common.Hash    `json:"parentHash" gencodec:"required"`
	LedgerHash  common.Hash    `json:"ledgerRoot" gencodec:"required"`
	ReceiptHash common.Hash    `json:"receiptHash" gencodec:"required"`
	Difficulty  *big.Int       `json:"difficulty" gencodec:"required"`
	Pow         *big.Int       `json:"pow" gencodec:"required"`
	Extra       []byte         `json:"extra" gencodec:"required"`
	Timestamp   uint64         `json:"timestamp" gencodec:"required"`
}
```

## 女娲

下面展示的为与盘古版本的结构区别，其中version字段为固定值 2

### TBlock

```go
type TBlock struct {
	...
}

```

### TBlock区块头

```
type THeader struct {
	...

    Version uint32 `json:"version"`
}
```

### TBlock区块体

```go
type TBody struct {
	...
    
	IdentityHash common.Hash `json:"identityHash" gencodec:"required"`
	Version      uint32
}
```

### DBlock区块头

```json
type DHeader struct {
	...
    
	Version     uint32         `json:"version" gencodec:"required"`
}
```

### DBlock区块体

```go
type DBody struct {
	...
    
	Version   uint32
}
```

## 太乙

与女娲结构一样，Version字段为固定值3
