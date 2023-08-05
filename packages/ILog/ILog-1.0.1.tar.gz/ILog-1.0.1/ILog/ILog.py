# -*- coding: utf-8 -*-
import os
import re
import json
import logging
import logging.handlers
import datetime


REMOVE_ATTR = ["module", "exc_text", "stack_info", "created", "msecs", "relativeCreated", "exc_info", "msg", "args",
               "thread", "threadName", "processName", "process", "levelno", "name"]

LOG_STYLE = os.getenv("LOG_STYLE", "pretty")


class JSONFormatter(logging.Formatter):

    def format(self, record):
        extra = self.build_record(record)
        self.set_format_time(extra)  # set time
        extra["level"] = extra["levelname"]
        extra["source"] = extra["pathname"]
        extra.pop("levelname")
        extra.pop("pathname")
        extra.pop("funcName")

        msg = record.msg
        if isinstance(msg, dict):
            msg_data = msg['msg']
            if 'Traceback' in msg_data:
                extra['exception'] = msg_data
                extra['msg'] = re.findall(r"(.*\S)", msg_data)[-1]

            else:
                extra['exception'] = None
                extra['msg'] = msg_data

        else:
            if 'Traceback' in msg:
                extra['exception'] = msg
                extra['msg'] = re.findall(r"(.*\S)", msg)[-1]
            else:
                extra['exception'] = None
                extra['msg'] = msg

        if self._fmt == 'pretty':
            return json.dumps(extra, indent=1, ensure_ascii=False)
        else:
            return json.dumps(extra, ensure_ascii=False)

    @classmethod
    def build_record(cls, record):
        return {
            attr_name: record.__dict__[attr_name]
            for attr_name in record.__dict__
            if attr_name not in REMOVE_ATTR
        }

    @classmethod
    def set_format_time(cls, extra):
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        format_time = now.strftime("%Y-%m-%dT%H:%M:%S" + ".%03d" % (now.microsecond / 1000) + "Z")
        extra['time'] = format_time
        return format_time


def haveLogDir(dirname):
    '''
    检查是否含有log文件夹
    :param dirname: 文件夹名
    '''
    dir_path = dirname
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)


def ILog(file_name=None, file_dir=None, display=None, save_file=True, log_level=None, maxBytes=None, backupCount=None):
    '''
    创建日志对象
    :param file_name: 日志文件名称
    :param file_dir: 存放日志文件的文件夹名称
    :param display: 控制台输出格式，None不输出任何内容，string输出字符串类型json，dict输出格式化json
    :param save_file: False不生成log文件， True生成log文件
    :param log_level: 日志等级
    :param maxBytes: log文件分割大小
    :param backupCount: log文件分割数量
    :return: logger
    '''

    assert file_name is not None and type(file_name) is str, '请输入字符串类型日志文件名。'
    assert file_dir is not None and type(file_dir) is str, '请输入字符串类型日志文件保存路径。'
    assert display is None or str.upper(display) == 'STRING' or str.upper(
        display) == 'DICT', '请输入正确的display，string或者dict或者None。'
    assert save_file is True or save_file is False, '请输入正确的save_file, True或者False'
    assert log_level is None or str.upper(log_level) == 'INFO' or str.upper(log_level) == 'DEBUG' or \
           str.upper(log_level) == 'WARNING' or str.upper(
        log_level) == 'ERROR', '请输入正确的log_level, info或者debug或者warning或者error或者None。'
    assert maxBytes is None or type(maxBytes) is int, '请输入正确的日志文件大小，必须是整数。'
    assert backupCount is None or type(backupCount) is int, '请输入正确的日志文件数量，必须是整数。'

    if not log_level:
        log_level = logging.INFO
    elif str.upper(log_level) == 'INFO':
        log_level = logging.INFO
    elif str.upper(log_level) == 'ERROR':
        log_level = logging.ERROR
    elif str.upper(log_level) == 'DEBUG':
        log_level = logging.DEBUG
    elif str.upper(log_level) == 'WARNING':
        log_level = logging.WARNING
    else:
        log_level = logging.INFO

    if not maxBytes:
        maxBytes = (1024 * 1024) * 1
    else:
        maxBytes = (1024 * 1024) * int(maxBytes)

    if not backupCount:
        backupCount = 3

    # 初始化log
    logger = logging.getLogger(file_name)
    logger.setLevel(log_level)

    # 判断是否应该保存日志文件
    if save_file:
        # 检查是否含有log文件夹, 没有就创建
        haveLogDir(file_dir)
        # 设置log日志文件
        filename = "{}/{}.log".format(file_dir, file_name)
        handler = logging.handlers.RotatingFileHandler(filename, maxBytes=maxBytes, backupCount=backupCount)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)

    # 判断是否应该格式化输出日志
    if not display:
        logging.basicConfig(
            level=logging.DEBUG,
            filename='/dev/null',
            filemode='w')

    elif str.upper(display) == 'STRING':
        handler_console = logging.StreamHandler()
        handler_console.setLevel(log_level)
        handler_console.setFormatter(JSONFormatter())
        logger.addHandler(handler_console)

    elif str.upper(display) == 'DICT':
        handler_console = logging.StreamHandler()
        handler_console.setLevel(log_level)
        handler_console.setFormatter(JSONFormatter("pretty"))
        logger.addHandler(handler_console)

    return logger
