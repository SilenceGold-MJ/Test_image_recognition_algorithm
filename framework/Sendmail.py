import smtplib,os,configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from framework.logger import Logger

logger = Logger(logger="SendEmail").getlog()

proDir = os.getcwd()
configPath = os.path.join(proDir, "config\config.ini")
cf = configparser.ConfigParser()
cf.read(configPath, encoding="utf-8-sig")

class SendEmail():
    def send_attach(self, file＿name):
        # msg_from ="huo888hyh@163.com"# "3"#
        # pwd = "DY*******HK"   #"授权码"
        # to = ["hu*****g245@163.com"]#发送["hua****5@163.com","397****766@qq.com","1****8@qq.com"]
        # Cc= ["17*****8@qq.com"]#抄送

        msg_from =cf.get("Email", 'msg_from')# "3"#
        pwd = cf.get("Email", 'pwd')   #"授权码"
        to = cf.get("Email", 'to').split(",")#发送["huangpeng245@163.com","397135766@qq.com","178999718@qq.com"]
        Cc= cf.get("Email", 'Cc').split(",")#抄送

        receiver = to + Cc
        message = MIMEMultipart()
        message['From'] =Header("自动化测试平台", 'utf-8')
        message['To'] =";".join(to)#收件人Header(";".join(to) , 'utf-8')
        message["Cc"]=";".join(Cc)#Header(";".join(Cc) , 'utf-8') #抄送人";".join(Cc)

        subject = file＿name.split('\\')[-1].split('.')[0]#标题
        message['Subject'] = Header(subject, 'utf-8')
        message.attach(MIMEText(file＿name.split('\\')[-1].split('.')[0]+',已测试完成！测试详情如附件！', 'plain', 'utf-8'))
        att = MIMEText(open(file＿name, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        #att["Content-Disposition"] = ('attachment; filename=' + file＿name.split('\\')[-1])  #英文名称
        att.add_header('Content-Disposition', 'attachment', filename=Header(file＿name.split('\\')[-1], 'utf-8').encode())#中、英文名称
        message.attach(att)

        try:
            smtpObj = smtplib.SMTP('smtp.163.com')  #smtplib.SMTP_SSL("smtp.qq.com", 465)
            smtpObj.login(msg_from, pwd)
            smtpObj.sendmail(msg_from, receiver, message.as_string())
            logger.info('邮件发送成功')
        except smtplib.SMTPException as e:
            logger.error(" 无法发送邮件，" +str( e.strerror))

    def send_normal(self,  contect):
        # msg_from = 'huo****@163.com'
        # passward = 'DYT****XXZMHK'  # 授权码
        # to = ["3****66@qq.com"]  # 发送["hu****g245@163.com","39****6@qq.com","17****18@qq.com"]
        # Cc = ["17****18@qq.com"]  # 抄送

        msg_from =cf.get("Email", 'msg_from')# "3"#
        passward = cf.get("Email", 'pwd')   #"授权码"
        to = cf.get("Email", 'to').split(",")#发送["huangpeng245@163.com","397135766@qq.com","178999718@qq.com"]
        Cc= cf.get("Email", 'Cc').split(",")#抄送

        receiver = to + Cc

        subject = '自动化测试结果'#标题
        content =  (str(contect))
        msg = MIMEText(content)
        msg['From'] = Header("自动化测试平台系统", 'utf-8')#msg['From'] = msg_from
        msg['Subject'] = subject
        msg['To'] = ";".join(to)  # Header("相关", 'utf-8')  #收件人
        msg["Cc"] = ";".join(Cc)  # 抄送人
        try:
            s = smtplib.SMTP('smtp.163.com', 25)   #smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(msg_from, passward)
            s.sendmail(msg_from, receiver, msg.as_string())
            logger.info('邮件发送成功')
        except smtplib.SMTPException as e:
            logger.error("Error: 无法发送邮件" + format(e))
            #print('发送失败' + format(e))

#
# if __name__ == '__main__':
#     path=r'F:\python\AR\AR算法准确率测试.xlsx'
#     SendEmail=SendEmail()
#     SendEmail.send_attach(path)
#     #SendEmail.send_normal("哈哈")
