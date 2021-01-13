import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from config.globalVars import BaseConfig

config = BaseConfig()


def send_mail(sendto):
    mail_host = 'smtp.sohu.com'
    username = 'test@sohu.com'
    password = 'test'
    receivers = sendto

    message = MIMEMultipart()
    message['From'] = Header(u'UI自动化', 'utf-8')
    message['subject'] = Header(u'UI自动化测试结果', 'utf-8')
    message.attach(MIMEText(u'测试结果详见附件', 'plain', 'utf-8'))
    report_root = config.report_path  # 获取报告路径
    report_file = 'report.html'  # 报告文件名称
    att1 = MIMEText(open(report_root + report_file, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    att1["Content-Disposition"] = 'attachment; filename={}'.format(report_file)
    message.attach(att1)

    try:
        smtp = smtplib.SMTP()
        smtp.connect(mail_host, 25)
        smtp.login(username, password)
        smtp.sendmail(username, receivers, message.as_string())
        print('邮件发送成功')
    except Exception as e:
        print('邮件发送失败')
        raise e
