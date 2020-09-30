import requests
import base64
import json
import os, time, datetime
import configparser
from framework.Getimage import *
from framework.ExportExcle import *
from framework.logger import Logger
from multiprocessing import Process, Lock
from multiprocessing import Pool,Lock,Manager
import multiprocessing
from framework.Algor import *

logger = Logger(logger="TestValue").getlog()
proDir = os.getcwd()
configPath = os.path.join(proDir, "config\config.ini")
cf = configparser.ConfigParser()
cf.read(configPath, encoding="utf-8-sig")

def API(imagefile_path):  # 给接口图片地址返回top3的值
    with open(imagefile_path, "rb") as f:
        # b64encode是编码，b64decode是解码
        base64_data = base64.b64encode(f.read())
        str_base64 = str(base64_data, 'utf-8')
        try:
            url = "https://*********.com:8445/****s/b**c/hpTest.html"
            payload = {
                "file": str_base64, "fileName": imagefile_path.split('\\')[-1]
            }
            headers = {
                'Content-Type': "application/json",
            }
            payload = json.dumps(payload)  # 将字典类型转换为 JSON 对象，序列化
            r = requests.post(url, data=payload, headers=headers)
            r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
            top = r.text.split(',')
            dics = {"code": 2000, "message": "识别成功！", "topdata": {"top1": int(top[0]), "top2": int(top[1]), "top3": int(top[2])}}
            return json.dumps(dics)
        except Exception as e:
            dics = {"code": 4000, "message": "服务可能未开启，" + str(e), "topdata": {'top1': -99, 'top2': -99, 'top3': -99}}
            return json.dumps(dics)


def API2(imagefile_path):
    with open(imagefile_path, "rb") as f:
        # b64encode是编码，b64decode是解码
        base64_data = base64.b64encode(f.read())
        str_base64 = str(base64_data, 'utf-8')
        try:
            url = "http://192.168.1.182:8888/Disc"
            # querystring = {"image_base64":str_base64,"image_name":imagefile_path.split('\\')[-1]}#imagefile_path.split('\\')[-1]#, params=querystring
            payload = {"image_base64": str_base64,
                       "image_name": imagefile_path.split('\\')[-1]}  # imagefile_path.split('\\')[-1]
            response = requests.request("post", url, data=(payload))
            return (response.text)
        except Exception as e:
            return ("服务可能未开启，" + str(e))


def Summary(imagefile_path, i):
    now = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))  # 获取当前时间
    code = int(imagefile_path.split('\\')[-2])
    TestChart = imagefile_path.split('\\')[-1]

    try:
        T1 = datetime.datetime.now()
        topdata = json.loads(testdll(imagefile_path))['topdata']

        T2 = datetime.datetime.now()
        T = round((T2 - T1).total_seconds(), 3)  # 检索耗时

    except Exception as e:
        logger.error('报错:%s' % str(e))
        topdata = {'top1': -88, 'top2': -88, 'top3': -88}
        T = 0  # 检索耗时

    TestValue1, TestValue2, TestValue3 = topdata['top1'], topdata['top2'], topdata['top3'],
    if TestValue1 == code:
        Result = ["PASS", ['c6efce','006100']]
    elif TestValue1 in [-88, -99]:
        Result = ["ERROR", ['ffeb9c', '9c6500']]
        Failimgae(imagefile_path, code)
    else:
        Result = ["FAIL", ['ffc7ce', '9c0006']]
        Failimgae(imagefile_path, code)
    dic = {
        'ID': i + 1,
        'TestTime': now,
        'Name': cf.get("Data", str(code)),
        'TestChart': TestChart,
        'Code': code,
        "ExpectedValue": code,
        'TimeConsuming': T,
        'top1': TestValue1,
        'top2': TestValue2,
        'top3': TestValue3,
        'Result': Result,
        'imagefile': imagefile_path

    }

    return dic


def TestValue(rootdir, addr, title):#单进程
    listPath = Pathlsit(rootdir)
    Total = (len(listPath))
    A = getnum(addr, title)
    for i in range(A - 1, Total):

        dic = Summary(listPath[i], i)
        if os.path.exists(os.getcwd() + '\\' + addr):
            SummaryExcle(addr, dic, title, 10)
            logger.info('测试进度：%s/%s；测试图：%s；编号：%s；耗时：%s；top3：%s、%s、%s；测试结果：%s。' % (
            i + 1, Total, dic['TestChart'], dic['Code'], dic['TimeConsuming'], dic['top1'], dic['top2'],
            dic['top3'], dic['Result'][0]))

        else:
            ExportExcle(addr, dic, title, 10)
            logger.info('测试进度：%s/%s；测试图：%s；编号：%s；耗时：%s；top3：%s、%s、%s；测试结果：%s。' % (
            i + 1, Total, dic['TestChart'], dic['Code'], dic['TimeConsuming'], dic['top1'], dic['top2'],
            dic['top3'], dic['Result'][0]))

def TestValue2(rootdir, addr, title,proce):#支持多进程
    manager = Manager()
    lock = manager.Lock()  # 产生钥匙
    listPath = Pathlsit(rootdir)
    Total = (len(listPath))
    A = getnum(addr, title)
    pool = multiprocessing.Pool(processes=proce)
    for i in range(A - 1, Total):
        pool.apply_async(func=process, args=(listPath[i],addr, title,Total,i,lock))
    pool.close()
    pool.join()  # 在join之前一定要调用close，否则报错

def process(imagefile_path,addr, title,Total,i,lock):

    dic = Summary(imagefile_path, i)
    if os.path.exists(os.getcwd() + '\\' + addr):
        lock.acquire()  ##拿到钥匙进门,其他进程阻塞, acqurie和release之间的代码只能被一个进程执行
        SummaryExcle(addr, dic, title, 10)
        lock.release()  # 释放钥匙
        logger.info('测试进度：%s/%s；测试图：%s；编号：%s；耗时：%s；top3：%s、%s、%s；测试结果：%s。' % (
            i + 1, Total, dic['TestChart'], dic['Code'], dic['TimeConsuming'], dic['top1'], dic['top2'],
            dic['top3'], dic['Result'][0]))

    else:
        lock.acquire()  ##拿到钥匙进门,其他进程阻塞, acqurie和release之间的代码只能被一个进程执行
        ExportExcle(addr, dic, title, 10)
        lock.release()  # 释放钥匙
        logger.info('测试进度：%s/%s；测试图：%s；编号：%s；耗时：%s；top3：%s、%s、%s；测试结果：%s。' % (
            i + 1, Total, dic['TestChart'], dic['Code'], dic['TimeConsuming'], dic['top1'], dic['top2'],
            dic['top3'], dic['Result'][0]))

