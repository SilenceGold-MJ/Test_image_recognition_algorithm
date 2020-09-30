from ctypes import *
import os, json
def testdll(SrcPath):
    os.environ['path'] += ';D:\Program Files (x86)\python3\opencv_dll'  # 添加dll依赖库目录到系统环境或把所依赖dll文件存放python环境的安装目录中
    dll = CDLL(os.getcwd()+"/"+"tool"+"/"+"DoorStatusJudgmentDLL1.dll")#初始化dll,加载dll
    dll.DoorStatusJudgment.argtypes = [POINTER(c_char)] #定义dll入参类型
    dll.DoorStatusJudgment.restype = c_int   #定义dll出参类型，不定义程序不知道类型会报错
    SrcPath = (c_char * 300)(*bytes(SrcPath, 'utf-8'))  # 把一组300个的字符定义为STR
    pchar = dll.DoorStatusJudgment( SrcPath)
    dics = {"code": 2000, "message": "识别成功！", "topdata": {"top1": int(pchar), "top2": int(pchar), "top3": int(pchar)}}

    return json.dumps(dics)

