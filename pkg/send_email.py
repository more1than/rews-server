import logging
import smtplib
import threading
from email.header import Header
from email.mime.text import MIMEText
from app.models.alert_logs import AlertLogs
from pkg.create_con import create_con
from pkg.is_expire import is_expire
from pkg.template.logging_template import logging_template
from pkg.util.setting import setting

mail_msg = setting.get_email_config()
mail_host = mail_msg.get("mail_host")
sender = mail_msg.get("sender")


def save_loggin(people, error=None):
    logging_template('vm', people.result_vm, people.id, error)
    logging_template('disk', people.result_disk, people.id, error)
    logging_template('net', people.result_new_work, people.id, error)
    logging_template('ext', people.result_external_resource, people.id, error)


def send_email(people):
    lock = threading.Lock()
    lock.acquire()
    html = '<html><body>'
    html += '<table><tr><th>'
    html += '资源种类'
    html += '</th>'
    html += '<th>'
    html += '资源名称'
    html += '</th>'
    html += '<th>'
    html += '资源id'
    html += '</th>'
    html += '<th>'
    html += '资源规格'
    html += '</th>'
    html += '<th>'
    html += '资源类型'
    html += '</th>'
    html += '<th>'
    html += '剩余时间(/天)'
    html += '</th>''</tr>'
    for i in people.result_vm:
        html += '<tr><td>'
        html += "云主机"
        html += '</td>'
        html += '<td>'
        html += i.hostname
        html += '</td>'
        html += '<td>'
        html += i.id
        html += '</td>'
        html += '<td>'
        html += i.instance_type
        html += '</td>'
        html += '<td>'
        html += i.cloud_type
        html += '</td>'
        html += '<td>'
        html += str(int(is_expire(str(i.expire_at)) / 24 / 60 / 60))
        html += '</td>''</tr>'
    for i in people.result_disk:
        html += '<tr><td>'
        html += "云盘"
        html += '</td>'
        html += '<td>'
        html += ""
        html += '</td>'
        html += '<td>'
        html += i.id
        html += '</td>'
        html += '<td>'
        html += i.instance_type
        html += '</td>'
        html += '<td>'
        html += i.cloud_type
        html += '</td>'
        html += '<td>'
        html += str(int(is_expire(str(i.expire_at)) / 24 / 60 / 60))
        html += '</td>''</tr>'
    for i in people.result_new_work:
        html += '<tr><td>'
        html += "带宽"
        html += '</td>'
        html += '<td>'
        html += ""
        html += '</td>'
        html += '<td>'
        html += i.id
        html += '</td>'
        html += '<td>'
        html += i.instance_type
        html += '</td>'
        html += '<td>'
        html += i.cloud_type
        html += '</td>'
        html += '<td>'
        html += str(int(is_expire(str(i.expire_at)) / 24 / 60 / 60))
        html += '</td>''</tr>'
    for i in people.result_external_resource:
        html += '<tr><td>'
        html += "外置资源"
        html += '</td>'
        html += '<td>'
        html += i.name
        html += '</td>'
        html += '<td>'
        html += i.id
        html += '</td>'
        html += '<td>'
        html += i.instance_type
        html += '</td>'
        html += '<td>'
        html += i.desc
        html += '</td>'
        html += '<td>'
        html += str(int(is_expire(str(i.expire_at)) / 24 / 60 / 60))
        html += '</td>''</tr>'
    html += '</table></body></html>'
    message = MIMEText(html, 'html', 'utf-8')
    message['From'] = sender
    message['To'] = people.mail
    subject = '告警邮件'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)
        smtpObj.login(sender, 'preuofrbwwsfdgdd')
        smtpObj.sendmail(sender, people.mail, message.as_string())
        logging.info('email send success')
    except smtplib.SMTPException as e:
        logging.error('email send error')
        save_loggin(people, e)
        lock.release()
    save_loggin(people)
    lock.release()
