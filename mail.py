# -*- coding: utf-8 -*-#

import smtplib
from email.mime.text import MIMEText
from datetime import datetime


def send_mail(subject, body):
    sender = 'baojiong@box-fairy.com'
    password = 'xyaxeKKV8vXeujmU'  # 腾讯QQ邮箱或腾讯企业邮箱必须使用授权码进行第三方登陆
    receiver = 'shadowbot2@box-fairy.com'
    smtp_server = 'smtp.exmail.qq.com'  # 腾讯服务器地址
    now = datetime.now()
    str_text = now.strftime('%Y-%m-%d %H:%M:%S')

    # 邮件的其它设置三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['from'] = sender  # 设置发送人
    msg['to'] = receiver  # 设置接收人

    # 邮箱配置&发送
    smtp = smtplib.SMTP_SSL(smtp_server, 465)
    smtp.login(sender, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()

    print('Mail Sent OK!')


if __name__ == "__main__":
    send_mail("subject", "body")