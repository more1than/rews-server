import logging

import requests
import json
from hashlib import md5
from pkg.util.setting import setting

sms_msg = setting.get_sms_config()
url = sms_msg.get("Url")
sms_user = sms_msg.get("SmsUser")
sms_key = sms_msg.get("SmsKey")
template_id = sms_msg.get("TemplateId")


def generate_md5(fp):
    m = md5()
    m.update(fp)
    return m.hexdigest()


def send(phone):
    param = {
        'smsUser': sms_user,
        'templateId': template_id,
        'phone': phone,
        'vars': json.dumps({"%content%": "有资源即将过期"})
    }
    param_keys = list(param.keys())
    param_keys.sort()
    param_str = ""
    for key in param_keys:
        param_str += key + '=' + str(param[key]) + '&'
    param_str = param_str[:-1]
    sign_str = sms_key + '&' + param_str + '&' + sms_key
    sign = generate_md5(sign_str.encode())
    param['signature'] = sign
    res = requests.post(url, data=param)
    logging.info(res.text)
