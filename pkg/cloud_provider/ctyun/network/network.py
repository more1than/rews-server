from pkg.cloud_provider.ctyun.session.session import Session


class Network(Session):
    def __init__(self, name, access_key, security_key):
        Session.__init__(self, name, access_key, security_key)

    # 查询公网IP列表
    def query_ips(self):
        param_dic = {
            "regionId": self.region_id
        }
        content_md5_source = "%s" % self.region_id
        service_path = "/apiproxy/v3/ondemand/queryIps"  # 查询公网IP列表 1.37
        return self.send_request(content_md5_source, service_path, param_dic)

    # 根据主机ID查询带宽信息
    def query_network_by_vm_id(self, vm_id):
        param_dic = {
            "VMId": vm_id,
        }
        content_md5_source = "%s" % vm_id
        service_path = "/apiproxy/v3/queryNetworkByVMId"  # 2.16 根据主机ID查询带宽信息
        return self.send_request(content_md5_source, service_path, param_dic)

    # 查询共享带宽
    def query_networks(self):
        param_dic = {
            "regionId": self.region_id
        }
        content_md5_source = self.region_id
        service_path = "/apiproxy/v3/queryShareBandwidth"  # 查询共享带宽  1.79
        return self.send_request(content_md5_source, service_path, param_dic)

    # 查询共享带宽
    def query_networks_page(self, page_num):
        param_dic = {
            "regionId": self.region_id,
            "pageNo": str(page_num + 1)
        }
        content_md5_source = "%s\n%s" % (self.region_id, str(page_num + 1))
        service_path = "/apiproxy/v3/queryShareBandwidth"
        result_details = self.send_request(content_md5_source, service_path, param_dic)
        return result_details
