from pkg.cloud_provider.ctyun.session.session import Session


class Image(Session):
    def __init__(self, name, access_key, security_key):
        Session.__init__(self, name, access_key, security_key)

    # 查询镜像列表
    def query_images(self):
        param_dic = {
            "regionId": self.region_id,
            "imageType": "private"
        }
        content_md5_source = "%s\n%s" % (self.region_id, "private")
        service_path = "/apiproxy/v3/order/getImages"  # 查询公网IP列表 1.37
        return self.send_request(content_md5_source, service_path, param_dic)
