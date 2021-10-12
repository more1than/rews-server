import logging
from logging.handlers import RotatingFileHandler

import yaml


class ParserYaml(object):
    def __init__(self):
        self.yaml_result = self.parser_yaml()

    def parser_yaml(self):
        f = open("config/config.yaml", encoding="utf-8")
        yaml_result = yaml.load(f.read(), Loader=yaml.FullLoader)
        return yaml_result

    def get_tty_config(self):
        tyy_config_data = self.yaml_result.get("TyyConfig")
        return tyy_config_data

    def get_mysql_config(self):
        # mysql配置读取
        mysql_config = self.yaml_result.get("Database")
        mysql_host = mysql_config["MysqlHost"]
        mysql_user = mysql_config["MysqlUser"]
        mysql_password = mysql_config["MysqlPassword"]
        mysql_port = mysql_config["MysqlPort"]
        mysql_db = mysql_config["MysqlDb"]
        SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8" % (
            mysql_user, mysql_password, mysql_host, mysql_port, mysql_db
        )
        return SQLALCHEMY_DATABASE_URI

    def get_email_config(self):
        email_config = self.yaml_result.get("Email")
        mail_msg = {
            "mail_host": email_config["MailHost"],
            "mail_user": email_config["MailUser"],
            "mail_pass": email_config["MailPass"],
            "mail_name": email_config["MailName"],
            "sender": email_config["Sender"],
            "phone": email_config["Phone"],
        }
        return mail_msg

    def get_log_config(self):
        # log配置读取
        LogConfig = self.yaml_result.get("LogConfig")
        LogFilePath = LogConfig.get("LogFilePath")
        MaxBackups = LogConfig.get("MaxBackups")
        MaxSize = LogConfig.get("MaxSize")
        logPath = "%s/log.log" % LogFilePath
        # 按文件大小分割
        handler = RotatingFileHandler(logPath, maxBytes=MaxSize * 1024 * 1024, backupCount=MaxBackups)
        # 按天分割
        handler.setLevel(logging.INFO)
        logging_format = logging.Formatter(
            '[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s')
        handler.setFormatter(logging_format)
        logging.root.setLevel(logging.INFO)
        return handler

    def get_time_config(self):
        time_config = self.yaml_result.get("TimeConfig")
        time_msg = {
            "start_time": time_config["StartTime"],
            "end_time": time_config["EndTime"],
        }
        return time_msg

    def get_sms_config(self):
        sms_config = self.yaml_result.get("SmsConfig")
        sms_msg = {
            "Url": sms_config["Url"],
            "SmsUser": sms_config["SmsUser"],
            "SmsKey": sms_config["SmsKey"],
            "TemplateId": sms_config["TemplateId"],
        }
        return sms_msg

    def send_email_config(self):
        mail_config = self.yaml_result.get("EmailConfig")
        mail_msg = {
            "Url": mail_config["Url"],
            "ApiUser": mail_config["ApiUser"],
            "ApiKey": mail_config["ApiKey"],
            "From": mail_config["From"],
            "FromName": mail_config["FromName"],
            "Subject": mail_config["Subject"],
        }
        return mail_msg

    def get_timer_time(self):
        time_config = self.yaml_result.get("TimerTime")
        time_msg = {
            "Timer1": time_config['timer1'],
            "Timer2": time_config['timer2']
        }
        return time_msg

setting = ParserYaml()
