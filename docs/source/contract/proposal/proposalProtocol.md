# 如何使用统一规范新增一类提案

## 1.新建一个xxxProposal继承AbstractProposal

AbstractProposal的方法

|      | 方法名                                                       | 有默认实现 |      |
| ---- | ------------------------------------------------------------ | ---------- | ---- |
| 1    | ExecuteProposal(zvm *ZVM) (bool, error)                      | ×          |      |
| 2    | RejectProposal(zvm *ZVM) (bool, error)                       | ×          |      |
| 3    | GetProposalType() Proposal                                   | ×          |      |
| 4    | GetProposalResult() ProposalResult                           | ×          |      |
| 5    | IsLaunchPermissioned(caller common.Address, zvm *ZVM) (bool, error) | ×          |      |
| 6    | IsVotePermissioned(caller common.Address, zvm *ZVM) (bool, error) | ×          |      |
| 7    | GetVotersCount(zvm *ZVM) int                                 | ×          |      |
| 8    | Decode([]byte) error                                         | ×          |      |
| 9    | Encode() ([]byte, error)                                     | ×          |      |
| 10   | SetProposalId(string)                                        | √          |      |
| 11   | GetProposalId() string                                       | √          |      |
| 12   | GetProposalState() ProposalState                             | √          |      |
| 13   | SetStatus(status ProposalState, zvm *ZVM) error              | √          |      |
| 14   | GetProposalAddress() common.Address                          |            |      |
| 15   | ReStore(zvm *ZVM) error                                      | √          |      |
| 16   | InitStore                                                    | √          |      |
| 17   | ToByte                                                       | √          |      |
| 18   | GetNonce                                                     | √          |      |



| 字段名        | 字段类型             | 备注     |
| ------------- | -------------------- | -------- |
| ProposalId    | string               | 提案Id   |
| ProposalState | PrososalState(uint8) | 提案状态 |

```go

	ProposalId    string         `json:"proposalId"` //提案id
	ProposalState `json:"proposalState"`
```

## 2. 在Proposal.go文件中向ProposalImplementMap中添加该提案

``` go
var ProposalImplementMap = map[int]map[string]Proposal{
	update.Nuwa: {
		"zvm.ContractInnerManagerProposal": &ContractInnerManagerProposal{},
        "*zvm.ContractInnerManagerProposal": &ContractInnerManagerProposal{},
	},
}
```

ProposalImplementMap，用来通过ProposalId拿到Proposal的字节码后反序列化为对应的实现类。

## 3. 新建一个xxxProposalResult实现AbstractProposalResult接口

```
type ContractInnManProposalResult struct {
	AbstractProposalResult
}
```

| 方法名                                       | 有默认实现 |      |
| -------------------------------------------- | ---------- | ---- |
| Contains(common.Address) bool                | √          |      |
| Agree(common.Address, Proposal, *ZVM) bool   | ×          |      |
| Against(common.Address, Proposal, *ZVM) bool | ×          |      |

## 4. 新建发起特定提案的预编译合约LaunchProposalPrecompile

须调用proposal.InitStore()将proposal持久化，否则在投票阶段会出错
