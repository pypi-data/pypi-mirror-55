### 实现了日志按大小分割的模块

### 使用方法
```python
import os
import wylog

ilog = wylog.ILog(
    file_name='demo', # 日志文件的名字叫demo
    file_dir=os.path.dirname(__file__) + os.sep + "../Log/", # 日志文件存储到当前文件所在目录的上级Log文件夹中，Log文件夹名称可自定义，没有会自动创建
    display='string', # 如果设置为None，则终端不会打印日志内容；如果设置为string, 则终端打印str类型日志内容；如果设置为dict，则终端打印格式化dict类型日志内容；
    save_file=True, # 如果设置为True，则日志内容保存到文件；如果设置为False，则不会保存日志到文件；
    log_level='info', # 日志等级，目前支持：debug、info、error、warning；
    maxBytes=30, # 设置单个log日志的文件大小，必须是整数，单位是M，此样例设置文件大小为30M；
    backupCount=3, # 设置日志切分数量，此样例设置文件数量为3个
)

ilog.info('this is info log')
ilog.error('this is error log')
ilog.debug('this is debug log')
ilog.warning('this is warning log')
```
