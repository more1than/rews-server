from pkg.cloud_provider.ctyun.session.session import Session


class Node(Session):
    def query_vms(self):
        param_dic = {
            "regionId": self.region_id
        }
        content_md5_source = self.region_id
        service_path = "/apiproxy/v3/ondemand/queryVMs"  # 查询主机列表 1.35
        result_json = self.send_request(content_md5_source, service_path, param_dic)
        return result_json

    def query_vms1(self):
        param_dic = {
            "regionId": self.region_id
        }
        content_md5_source = self.region_id
        service_path = "/apiproxy/v3/queryVMs"  # 查询主机列表 1.35
        result_json = self.send_request(content_md5_source, service_path, param_dic)
        return result_json

    def query_vm_detail(self, vm_id):
        param_dic = {
            "vmId": vm_id,
        }
        content_md5_source = vm_id
        service_path = "/apiproxy/v3/queryVMDetail"  # 查询主机详情信息（融合） 2.5
        result_json = self.send_request(content_md5_source, service_path, param_dic)
        return result_json

    def query_vm(self, vm_id):
        param_dic = {
            "regionId": "cn-sh1",
            "vmId": vm_id,
        }
        content_md5_source = "%s\n%s" % ("cn-sh1", vm_id)
        service_path = "/apiproxy/v3/ondemand/queryVMDetail"  # 查询主机详情 1.36
        return self.send_request(content_md5_source, service_path, param_dic, 'get')
