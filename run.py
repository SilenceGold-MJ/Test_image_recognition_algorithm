# -*- coding: utf-8 -*-
# !/usr/bin/python3

from framework.Sendmail import SendEmail
from framework.Shutdown import Shutdown
from framework.TestValue import *
from framework.Statistics import *
from framework.logger import Logger

logger = Logger(logger="run").getlog()
proDir = os.getcwd()
configPath = os.path.join(proDir, "config\config.ini")
cf = configparser.ConfigParser()
cf.read(configPath, encoding="utf-8-sig")

if __name__ == '__main__':
    threshold =float(cf.get("Config", 'threshold')) #汇总页达标率阈值
    filepath = '%s识别算法准确率测试.xlsx'%(cf.get("Config", 'TestName'))
    pathimage = cf.get("Config", 'pathimage')#图片地址
    proce=int(cf.get("Config", 'proce') )  #测试进程数
    TestValue2(pathimage,filepath,'测试记录',proce)  #数据测试写入表格
    Statistics(filepath, '汇总页', threshold)  # 汇总测试数据到表格
    SendEmail().send_attach(filepath)  # 发送测试生成的结果Excel
    Shutdown(2)                          #测试完成执行自动关机,key值1，判断时间段是否自动关机；0执行完成后关机；2执行完成后不关机
    input('Press Enter to exit...')
