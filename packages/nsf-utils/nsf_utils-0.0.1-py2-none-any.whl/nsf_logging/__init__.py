# -*- coding:utf-8 -*-
import logging
import logging.handlers
import os

FORMAT = '[%(asctime)s](%(levelname)s) {pid:%(process)d, tid:%(thread)d, %(filename)s}, %(module)s.%(funcName)s %(' \
         'lineno)d: %(message)s '


def getLogger(logDir, logFile, logLevel="debug", stdin=False):
    """
    :param logDir:日志输出目录
    :param logFile:日志输出文件
    :param stdin:是否将日志输出到控制台
    :return:日志记录器
    """
    # 提取日志路径
    if logDir == "":
        raise TypeError("The logDir param can't be empty")
    if not os.path.exists(logDir):
        os.mkdir(logDir)
    if logFile == "":
        raise TypeError("The logFile param can't be empty")
    logFile = logFile if os.path.isabs(logFile) else os.path.join(logDir, logFile)
    
    # 后缀名判断
    if os.path.splitext(logFile)[1] != ".log":
        logPath = ".".join([logFile, "log"])
    else:
        logPath = logFile
    
    nsfLogger = NsfLogger(logPath, logLevel, stdin)
    return nsfLogger


class NsfLogger(logging.Logger):
    global FORMAT
    
    def __init__(self, logPath, logLevel, stdin):
        super(NsfLogger, self).__init__("")
        for handler in self.handlers:
            self.removeHandler(handler)
        self.logLevel = logLevel.upper()
        self.setLevel(self.logLevel)
        
        # 设置滚动日志，文件大小为10M,编码为utf-8，最大文件个数为30个，如果日志文件超过30个，则会覆盖最早的日志
        fileHandler = logging.handlers.RotatingFileHandler(logPath, mode='a', maxBytes=1024 * 1024 * 10,
                                                           backupCount=30, encoding="utf-8")
        fileHandler.setLevel(self.logLevel)
        fileHandler.setFormatter(logging.Formatter(FORMAT))
        self.addHandler(fileHandler)
        
        # 是否输出到控制台
        if stdin:
            stdHandler = logging.StreamHandler()
            stdHandler.setLevel(self.logLevel)
            stdHandler.setFormatter(logging.Formatter(FORMAT))
            self.addHandler(stdHandler)


if __name__ == '__main__':
    logger = getLogger("/home/ec2-user/", "app.log", stdin=True)
    logger.info("this is a test")
