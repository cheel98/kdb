# 证书

## bug表现:
    
    节点证书报未知高度异常

## 分析:
    
    1.异常节点的证书确实是由节点自签名颁发的
    
    2.证书的高度信息存放在cert.Subject.Locadity[]中,正常情况下，证书高度应该在L[0]。异常的证书其高度信息在L[1]

## 排查:
    
    1.调用正常节点的latc_publishCert接口颁发证书，得到的证书是异常的。
    
    2.启动一个没有历史数据的节点，颁发证书，得到的证书是正常的。

==> 错误是由历史数据导致的。

    3.L 中共有三个信息，type,height,addr。他们会被按字典顺序排列,> 表示顺序在前。
    则:
        ① type>addr 是确定的
        ② height>=type (height=<k)
          height<type (height>k)  
            k 为一个固定高度。
    当height转为string时如果其长度大于type，则height<type，否则 height>=type
    因此当区块增长到一定高度就会出现这个bug。

## 解决：
    
    asn1 编码时遵循DER规则, 会对证书中的数组进行字典排序，当区块高度信息过高或过低时，其在数组的索引位置会不同，导致证书失效。将证书高度这个会影响数组排序的元素单独放在Subject的SerialNumber字段。