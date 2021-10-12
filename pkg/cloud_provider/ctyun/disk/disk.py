from pkg.cloud_provider.ctyun.session.session import Session


class Disk(Session):
    def __init__(self, name, access_key, security_key):
        Session.__init__(self, name, access_key, security_key)

    # 查询磁盘列表
    def query_volumes(self):
        param_dic = {
            "regionId": self.region_id
        }
        content_md5_source = self.region_id
        service_path = "/apiproxy/v3/ondemand/queryVolumes"  # 查询磁盘列表 1.34
        return self.send_request(content_md5_source, service_path, param_dic)

    def query_volumes_detail(self, id):
        param_dic = {
            "volumeId": id,
        }
        content_md5_source = id
        service_path = "/apiproxy/v3/queryDataDiskDetail"  # 根据资源池ID查询磁盘列表 2.4
        return self.send_request(content_md5_source, service_path, param_dic)

    def query_resource(self, id):
        param_dic = {
            "masterOrderId": id,
        }
        content_md5_source = id
        service_path = "/apiproxy/v3/order/queryResourceInfoByMasterOrderId"  # 根据订单ID查询资源信息
        return self.send_request(content_md5_source, service_path, param_dic)
