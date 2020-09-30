# XX项目识别算法准确率测试

1.功能  
基于AI深度学习、OpenCV图像检测或识别技术形成的各类算法，进行对算法识别准确率自动化测试的测试框架。


2.详细流程场景  
1）.给算法一张图片，得给出一个值；算法可以在本地调用封装后使用，也可形成http接口请求调用  
2）.核对这个值是否和期望值一致  
3）.大量的图片进行批量测试，支持多进程并发执行，支持测试过程中停止终断后再接着已测试部分继续测试  
4）.测试过程中会把识别不准确的挑出来保存在failimgae文件夹下  
5）.最终统计形成测试报告Excel文档  
6）.测试完成后，发送邮件到指定收件  
7）.邮件发送完成后，自动处置是否自动关机  

2.运行之前请安装下面库，已安装过的不用安装  
openpyxl==2.6.3  
requests==2.22.0



3.更新  
2020-09-30上传  
