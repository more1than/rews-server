from pkg.cloud_provider.ctyun import Ctyun


class Provider():
    def __init__(self, type, name, access_key, security_key):
        self.type = type
        self.AccessKey = access_key
        self.SecurityKey = security_key
        self.name = name

    def get_cloud_provider(self):
        if self.type == 'ctyun':
            return Ctyun(self.name, self.AccessKey, self.SecurityKey)
        elif self.type == 'aliyun':
            pass  # TODO 阿里云
        elif self.type == 'ydyun':
            pass  # todo 移动
        else:
            pass  # TODO 其他的云平台供应商
