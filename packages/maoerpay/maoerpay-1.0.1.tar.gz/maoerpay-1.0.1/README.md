### 通过pip安装扩展，简单快速方便！

#### 安装(仅Python 3.x) - 开发版
> pip install maoerpay

#### 示例
先安装maoerpay （pip install maoerpay），注意仅支持Python 3.x版本，Python2.7即将被官方放弃，还在使用Python2.7的开发者建议升级到Python 3.x
~~~
from maoerpay import MaoerPay

PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
你的私钥
-----END RSA PRIVATE KEY-----''' # 注意头尾不要删除，把一行私钥粘贴在此处。

test = MaoerPay(mch_id='你的商户号',PRIVATE_KEY=PRIVATE_KEY)

result = test.order_query({'out_trade_no':'MaoerPay54938767'}) # 订单查询，传递字典类型参数

print(result)
~~~
