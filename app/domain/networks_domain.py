from app.models.account import Account
from app.models.alert_logs import AlertLogs
from app.models.peoples import *
from app.models.nodes import *
from app.models.network import *
from flask import make_response
from pkg.create_con import create_con
from pkg.cloud_provider.ctyun import Network
from pkg.resource_query import query_networks

vm_status = {"RESTARTING": "重启中", "RUNNING": "运行中", "STOPPING": "关机中", "STOPPED": "关机", "STARTING": "开机中",
             "DUEING": "销毁中", "DELETE": "删除", "FREEZING": "冻结", "OPENING": "开通中", "UPDATING": "变更规格中", "Expired": "过期"}
network_status = {"2": "运行中", "5": "已退订", "6": "已到期", "7": "已销毁"}


def get_net_work(args=None, page_num=1, page_size=10):
    if int(page_num) <= 0:
        page_num = 1
    if int(page_size) <= 0:
        page_size = 10
    con = create_con()
    networks, network_count = query_networks(con, args, page_num, page_size)
    list1 = []
    for network in networks:
        people_list = []
        network.status = network_status[network.status]
        if network.alert_peoples and network.alert_peoples != "":
            for people_id in network.alert_peoples.split(','):
                people = con.query(Peoples).filter_by(id=people_id).first()
                if people:
                    people_list.append(people.name)
        network_dict = network.to_dict()
        if network.expire_at:
            if network.expire_at.year == 1970:
                network_dict["expire_at"] = "--"
        for k, v in network_dict.items():
            if getattr(network, k) is None:
                network_dict[k] = ""
        network_dict["people_names_list"] = people_list
        list1.append(network_dict)
    resp = make_response({'msg': '查询带宽列表成功', 'value': list1, 'total': network_count}, 200)
    con.close()
    return resp


def get_net_work_detail(network_id):
    con = create_con()
    network = con.query(NetWorks).filter_by(id=network_id).first()
    if not network:
        resp = make_response({'msg': '查询带宽详情失败', 'value': {}, 'errors': [{
            "code": "400",
            "desc": "该带宽资源不存在",
            "field": "id"
        }]}, 400)
        return resp
    network.status = network_status[network.status]
    vms = con.query(Nodes).filter_by(network_id=network_id).all()
    people_list = []
    network_dict = network.to_dict()
    for k, v in network_dict.items():
        if getattr(network, k) is None:
            network_dict[k] = ""
    if network.alert_peoples and network.alert_peoples != "":
        for people_id in network.alert_peoples.split(','):
            people = con.query(Peoples).filter_by(id=people_id).first()
            if people:
                people_data = {
                    "people_id": people_id,
                    "people_name": people.name,
                }
                people_list.append(people_data)
    vm_list = []
    for vm in vms:
        vm_dict = vm.to_dict()
        vm_dict["status"] = vm_status[vm.status]
        for k, v in vm_dict.items():
            if getattr(vm, k) is None:
                vm_dict[k] = ""
        vm_list.append(vm_dict)
    network_logs = con.query(AlertLogs).filter_by(network_id=network_id).order_by(desc(AlertLogs.created_at))
    network_logs = [logs.to_dict() for logs in network_logs]
    network_dict["log_info"] = network_logs
    network_dict['vms'] = vm_list
    network_dict["people_names_list"] = people_list
    network_dict["status"] = network.status
    if network.expire_at:
        if network.expire_at.year == 1970:
            network_dict["expire_at"] = "--"
    resp = make_response({'msg': '查询带宽详情成功', 'value': network_dict}, 200)
    con.close()
    return resp


def put_net_work(args, network_id):
    con = create_con()
    network = con.query(NetWorks).filter_by(id=network_id).first()
    if not network:
        resp = make_response({'msg': '修改带宽失败', 'value': {}, 'errors': [{
            "code": "400",
            "desc": "该带宽资源不存在",
            "field": "id"
        }]}, 400)
        return resp
    for k, v in args.items():
        if v is not None and k == 'alert_disable':
            setattr(network, k, v)
            if v is True and network.sms_status is False:
                network.sms_status = True
        elif v and k == 'alert_peoples':
            setattr(network, k, ','.join(v))
        elif v and k == 'alert_level':
            setattr(network, k, v)
        elif v is not None and k == 'sms_status':
            if network.alert_disable is not True:
                setattr(network, k, v)
            else:
                resp = make_response({'msg': '修改带宽失败', 'value': {}, 'errors': [{
                    "code": "400",
                    "desc": "告警关闭时无法开启短信告警",
                    "field": "alert_disable"
                }]}, 400)
                return resp
    people_list = []
    if network.alert_peoples and network.alert_peoples != "":
        for people_id in network.alert_peoples.split(','):
            people = con.query(Peoples).filter_by(id=people_id).first()
            if people:
                people_list.append(people.name)
    con.merge(network)
    con.commit()
    network_dict = network.to_dict()
    for k, v in network_dict.items():
        if getattr(network, k) is None:
            network_dict[k] = ""
    network_dict["status"] = network_status[network.status]
    network_dict["people_names_list"] = people_list
    resp = make_response({'msg': '修改带宽成功', 'value': network_dict}, 200)
    con.close()
    return resp


def post_network(args):
    con = create_con()
    network = con.query(NetWorks).filter_by(id=args.get("id")).first()
    account = con.query(Account).filter_by(name=network.account_name).first()
    network = Network(account.name, account.api_key, account.api_sec)
    result = network.query_networks()
    if result['statusCode'] != 800:
        resp = make_response({'msg': '手动更新带宽详情失败', 'value': {}, 'errors': [{
            "code": "400",
            "desc": "tyy接口未返回数据",
            "field": "tyy"
        }]}, 400)
        return resp
    page = result.get('returnObj').get("pageCount")
    net_status = ""
    for page_num in range(page):
        network_info = network.query_networks_page(page_num)
        network_infos = network_info.get('returnObj').get('result')
        if not network_infos:
            resp = make_response({'msg': '手动更新带宽详情失败', 'value': {}, 'errors': [{
                "code": "400",
                "desc": "tyy接口未返回数据",
                "field": "tyy"
            }]}, 400)
            return resp
        for network in network_infos:
            if network.get("resBandwidthId") == args.get("id"):
                net_status = network.get('status')
    network_info = con.query(NetWorks).filter_by(id=args.get("id")).first()
    network_info.status = net_status
    people_list = []
    if network_info.alert_peoples and network_info.alert_peoples != "":
        for people_id in network_info.alert_peoples.split(','):
            people = con.query(Peoples).filter_by(id=people_id).first()
            if people:
                people_list.append(people.name)
    con.merge(network_info)
    con.commit()
    network_dict = network_info.to_dict()
    network_dict["status"] = network_status[net_status]
    network_dict["key"] = args.get("key")
    network_dict["people_names_list"] = people_list
    resp = make_response({'msg': '手动更新带宽详情成功', 'value': network_dict}, 200)
    con.close()
    return resp
