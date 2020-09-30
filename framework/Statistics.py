import openpyxl
import configparser, os
from framework.ExportExcle import *
from framework.logger import Logger

logger = Logger(logger="Statistics").getlog()
proDir = os.getcwd()
configPath = os.path.join(proDir, "config\config.ini")
cf = configparser.ConfigParser()
cf.read(configPath, encoding="utf-8-sig")


def excel_row_value_dice(file_name, title):
    wb = openpyxl.load_workbook(file_name)
    # ws = wb.active#打开当前页
    ws = wb[title]  # 打开指定页
    # 取出每行的值，以list方式存放
    rows_list = []
    for row in ws.rows:
        row_list = []
        for cell in row:
            row_list.append(cell.value)
        rows_list.append(row_list)
    # print(rows_list)
    # 结果转换成键值对的形式存放
    result = []
    codelist = []
    for i in range(len(rows_list) - 1):
        row_dict = {}
        for j in range(len(rows_list[0])):
            row_dict[rows_list[0][j]] = rows_list[i + 1][j]
        result.append(row_dict)
        codelist.append(row_dict['Code'])
    # print(reslut)
    codelist = list(set(codelist))
    return [result, codelist]


def Statistics(filepath, title, threshold):
    case = excel_row_value_dice(filepath, '测试记录')

    SumNumbers = []
    SumPass = []
    SumFail = []
    Standard = []
    UnStandard = []
    for x in range(len(case[1])):
        Numbertests = []
        passlist = []
        faillist = []
        errorlist = []

        i = case[1][x]
        for n in case[0]:
            if i == n['Code']:
                Numbertests.append(n)
                if n['Result'] == 'PASS':
                    passlist.append(n)
                elif n['Result'] == 'FAIL':
                    faillist.append(n)
                elif n['Result'] == 'ERROR':
                    errorlist.append(n)
        Accuracy = round(len(passlist) / len(Numbertests), 3)
        if Accuracy >= threshold:
            Accuracylist = ["%.2f%%" % (Accuracy * 100), ['c6efce','006100']]
            Standard.append(Accuracy)
        else:
            Accuracylist = ["%.2f%%" % (Accuracy * 100), ['ffc7ce', '9c0006']]
            UnStandard.append(Accuracy)
        dic = {
            'ID': x + 1,
            'Name': cf.get("Data", str(i)),
            'Code': i,
            'Numbertest': len(Numbertests),
            'PASS': len(passlist),
            "FAIL": len(faillist),
            'ERROR': len(errorlist),
            'Accuracy': Accuracylist
        }
        SumNumbers.append(len(Numbertests))
        SumPass.append(len(passlist))
        SumFail.append(len(faillist))
        SummaryExcle(filepath, dic, title, 7)  # excle文件路径、输入数据，写入工作表名称，结果颜色列
        logger.info(dic)
    dic_hz = {
        'Totaltype': '%s识别测试类别数：%s' % (cf.get("Config", 'TestName'),len(SumNumbers)),
        'SumNumbers': '识别总数(次数、图片总数)：%s' % sum(SumNumbers),
        'SumPass': '识别准确数：%s' % sum(SumPass),
        'SumFail': '识别不准确数：%s' % sum(SumFail),
        'Standard': '识别准确率达标数：%s' % len(Standard),
        'UnStandard': '识别准确率未达标数：%s' % len(UnStandard),
        'threshold': '准确率标准为不低于%s' % "%.2f%%" % ( threshold* 100),
        'StandardRate': cf.get("Config", 'TestName')+'识别准确率满足标准的达标率：%s' % "%.2f%%" % (len(Standard) / len(SumNumbers) * 100),
        'summary': '本次'+cf.get("Config", 'TestName')+'识别共计测试%s件，准确率达标%s件，剩余%s件未达标，达标率为：%s' % (
        len(SumNumbers), len(Standard), len(UnStandard), "%.2f%%" % (len(Standard) / len(SumNumbers) * 100))
    }
    VerticalExcle(filepath, dic_hz, title, 10)
    logger.info(dic_hz)
