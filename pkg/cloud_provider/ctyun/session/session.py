from pkg.cloud_provider.ctyun.option.option import Option
import base64
import hashlib
import hmac
import logging
import requests
import datetime
import json


class Session(Option):
    def get_content_md5(self, content_md5_source):
        m = hashlib.md5()
        m.update(content_md5_source.encode("utf-8"))
        data_digest = m.digest()
        content_md5 = base64.b64encode(data_digest).decode()
        return content_md5

    def get_request_date(self):
        request_date = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S CS")
        return request_date

    def get_hmac(self, message):
        hmac_digest = hmac.new(self.SecurityKey.encode("utf-8"), message.encode("utf-8"), hashlib.sha1).digest()
        hmac_str = base64.b64encode(hmac_digest).decode()
        return hmac_str

    def send_request(self, content_md5_source, service_path, param_dic, method="get"):
        logging.info("请求数据: service_path = %s , param_dic = %s " % (service_path, json.dumps(param_dic)))
        content_md5 = self.get_content_md5(content_md5_source)
        request_date = self.get_request_date()
        message = '%s\n%s\n%s' % (content_md5, request_date, service_path)
        hmac_str = self.get_hmac(message)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "accessKey": self.AccessKey,
            "contentMD5": content_md5,
            "requestDate": request_date,
            "hmac": hmac_str,
            "platform": "3",
        }
        if method == "post":
            url = "%s%s" % (self.url, service_path)
            result = requests.post(url, headers=headers, data=param_dic)
        else:
            headers.update(param_dic)
            url = "%s%s" % (self.url, service_path)
            result = requests.get(url, headers=headers)
        return result.json()
