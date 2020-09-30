import os
import datetime
#from datetime import datetime
from framework.logger import Logger
logger = Logger(logger="Shutdown").getlog()


def Shutdown(key):#1，判断时间为白天不自动关机，晚上执行关机；0执行完成后关机
    if key==1:
        # 范围时间
        d_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '8:30', '%Y-%m-%d%H:%M')
        d_time1 = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '23:20', '%Y-%m-%d%H:%M')

        # 当前时间
        n_time = datetime.datetime.now()

        # 判断当前时间是否在范围时间内
        if n_time > d_time and n_time < d_time1:
            logger.info('自动化测试已完成，白天时间段不执行自动关机！')
        else:
            logger.info('自动化测试已完成，晚上时间段执行120秒后自动关机！')
            os.system('shutdown -s -t 120')  # 测试完成自动关机

    elif key==0:
        logger.info('自动化测试已完成，执行120秒后自动关机！')
        os.system('shutdown -s -t 120')  # 测试完成自动关机
    elif key==2:
        logger.info('自动化测试已完成，不执行自动关机！')
