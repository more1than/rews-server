from app.models.disk import Disks
from app.models.network import NetWorks
from app.models.nodes import Nodes
from pkg.create_con import create_con


def account_delete(account):
    con = create_con()
    node_response = con.query(Nodes).filter_by(account_name=account.name).delete()
    # if node_response == 0:
    #     resp = make_response({'msg': '删除账号的主机信息失败', 'value': [], 'errors': [{
    #         "code": "400",
    #         "desc": "该告警人员不存在",
    #         "field": "id"
    #     }]}, 400)
    #     return resp
    disk_response = con.query(Disks).filter_by(account_name=account.name).delete()
    # if disk_response == 0:
    #     resp = make_response({'msg': '删除账号的磁盘信息失败', 'value': [], 'errors': [{
    #         "code": "400",
    #         "desc": "该告警人员不存在",
    #         "field": "id"
    #     }]}, 400)
    #     return resp
    network_response = con.query(NetWorks).filter_by(account_name=account.name).delete()
    # if network_response == 0:
    #     resp = make_response({'msg': '删除账号的带宽信息失败', 'value': [], 'errors': [{
    #         "code": "400",
    #         "desc": "该告警人员不存在",
    #         "field": "id"
    #     }]}, 400)
    #     return resp
    con.commit()
    con.close()
