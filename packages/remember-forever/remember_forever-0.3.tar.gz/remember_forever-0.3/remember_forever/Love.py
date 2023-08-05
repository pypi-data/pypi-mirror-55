# coding=utf-8
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import time
# 第三方 SMTP 服务
mail_host = "smtp.yeah.net"  # 设置服务器
mail_user = "justdoit2019@yeah.net"  # 用户名
mail_pass = "K9L3D8bEMVACrsVe"  # 口令,输入授权码，在邮箱设置 里用验证过的手机发送短信获得，不含空格

sender = 'justdoit2019@yeah.net'
receivers = ['weixiao917@foxmail.com']  # 接收邮件

def sendmail(text):
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = '冬儿的树洞'  # 邮件标题
    msgRoot['From'] = sender
    msgRoot['To'] = ';'.join(receivers)
    msgText = MIMEText(text, 'html', 'utf-8')  # 你所发的文字信息将以html形式呈现
    msgRoot.attach(msgText)
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, msgRoot.as_string())
    smtpObj.quit()

class Love():

    def get_birthday(self):
        print('冬儿，祝你生日快乐')

    def tired(self):
        print('抱抱')

    def thirsty(self):
        print('亲亲')

    def miss(self):
        print('宝贝，我也想你')

    def sleep(self):
        print('晚安宝贝')

    def getup(self):
        print('快起床，太阳晒屁屁了')

    def tell(self, text):
        print('嗯嗯，我知道啦')
        try:
            sendmail(text)
        except:
            pass
