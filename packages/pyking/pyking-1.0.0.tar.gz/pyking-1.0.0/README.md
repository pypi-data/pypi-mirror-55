# pyking

King代码包，富含很多乱七八糟的东西。

## 安装方式

环境Python3

安装
```
pip3 install pyking
```

更新
```
pip3 install --upgrade pyking
```

## 使用方法

### 导入库文件
```Python
#tushare股票查询与py文件创建接口
from pyking.tushare import creat, getinfo
```

### 调用函数
#### tushare模块
```python
getinfo.Search('参数A','参数B')
```
<font size=4>功能与参数</font>

功能: 获得股票ts_code值

参数1：查询方式

&emsp;&emsp;可选项:'symbol'或'name'

&emsp;&emsp;symbol:以股票代码方式查询

&emsp;&emsp;name:以股票名称方式查询

参数2：参数值 

&emsp;&emsp;例:'603696'或'中联重科'
***
```python
getinfo.Refresh()
```
<font size=4>功能与参数</font>

功能: 刷新数据库中的股票数据
***
```python
creat.creat()
```

<font size=4>功能与参数</font>

功能: 在当前目录下创建文档文件
***