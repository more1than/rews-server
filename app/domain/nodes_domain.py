import logging

from app.models.account import Account
from app.models.alert_logs import AlertLogs
from app.models.peoples import *
from app.models.nodes import *
from app.models.disk import *
from app.models.network import *
from flask import make_response
from pkg.create_con import create_con
from pkg.cloud_provider.ctyun import Node
from pkg.resource_query import query_vms

vm_status = {"RESTARTING": "重启中", "RUNNING": "运行中", "STOPPING": "关机中", "STOPPED": "关机", "STARTING": "开机中",
             "DUEING": "销毁中", "DELETE": "删除", "FREEZING": "冻结", "OPENING": "开通中", "UPDATING": "变更规格中", "Expired": "过期"}
network_status = {"2": "运行中", "5": "已退订", "6": "已到期", "7": "已销毁"}
disk_status = {"creating": "创建中", "available": "未挂载", "in-use": "正在使用", "error": "创建错误", "attaching": "挂载中",
               "detaching": "卸载中", "restoring-backup": "备份恢复中", "error_restoring": "备份恢复错误", "uploading": "上传中",
               "downloading": "下载中", "expired": "过期"}


def get_vms(args=None, page_num=1, page_size=10):
    if int(page_num) <= 0:
        page_num = 1
    if int(page_size) <= 0:
        page_size = 10
    con = create_con()
    nodes, nodes_count = query_vms(con, args, page_num, page_size)
    list1 = []
    try:
        for node in nodes:
            people_list = []
            if node.status:
                node.status = vm_status[node.status]
            if node.alert_peoples and node.alert_peoples != "":
                for people_id in node.alert_peoples.split(','):
                    people = con.query(Peoples).filter_by(id=people_id).first()
                    if people:
                        people_list.append(people.name)
            node_dict = node.to_dict()
            if node.expire_at:
                if node.expire_at.year == 1970:
                    node_dict["expire_at"] = "--"
            for k, v in node_dict.items():
                if getattr(node, k) is None:
                    node_dict[k] = ""
            node_dict["people_names_list"] = people_list
            node_dict["os"] = json.loads(node.os)
            node_dict["platform"] = json.loads(node.platform)
            list1.append(node_dict)
    except Exception as e:
        logging.error(e)
    resp = make_response({'msg': '查询主机列表成功', 'value': list1, 'total': nodes_count}, 200)
    con.close()
    return resp


def get_vm_detail(vm_id):
    con = create_con()
    try:
        node = con.query(Nodes).filter_by(id=vm_id).first()
        if not node:
            resp = make_response({'msg': '查询主机详情失败', 'value': {}, 'errors': [{
                "code": "400",
                "desc": "该主机资源不存在",
                "field": "id"
            }]}, 400)
            return resp
        if node.status:
            node.status = vm_status[node.status]
        disks = con.query(Disks).filter_by(node_id=vm_id).all()
        network_id = node.network_id
        node_dict = node.to_dict()
        if node.expire_at:
            if node.expire_at.year == 1970:
                node_dict["expire_at"] = "--"
        for k, v in node_dict.items():
            if getattr(node, k) is None:
                node_dict[k] = ""
        node_dict["network"] = []
        if network_id:
            network = con.query(NetWorks).filter_by(id=network_id).first()
            network_dict = network.to_dict()
            network_dict["status"] = network_status[network.status]
            node_dict["network"] = network_dict
        disks_list = []
    except Exception as e:
        logging.error(e)
        resp = make_response({'msg': '查询主机详情失败', 'value': {}, 'errors': e}, 400)
        return resp
    for disk in disks:
        if disk.status:
            disk.status = disk_status[disk.status]
        disks_list.append(disk.to_dict())
    node_dict["disks"] = disks_list
    people_list = []
    if node.alert_peoples and node.alert_peoples != "":
        for people_id in node.alert_peoples.split(','):
            people = con.query(Peoples).filter_by(id=people_id).first()
            if people:
                people_data = {
                    "people_id": people_id,
                    "people_name": people.name,
                }
                people_list.append(people_data)
    node_logs = con.query(AlertLogs).filter_by(node_id=vm_id).order_by(desc(AlertLogs.created_at))
    node_logs = [logs.to_dict() for logs in node_logs]
    node_dict["log_info"] = node_logs
    node_dict["people_names_list"] = people_list
    node_dict["os"] = json.loads(node.os)
    node_dict["platform"] = json.loads(node.platform)
    resp = make_response({'msg': '查询主机详情成功', 'value': node_dict}, 200)
    con.close()
    return resp


def put_vms(args, vm_id):
    con = create_con()
    node = con.query(Nodes).filter_by(id=vm_id).first()
    if not node:
        resp = make_response({'msg': '修改主机详情失败', 'value': {}, 'errors': [{
            "code": "400",
            "desc": "该主机资源不存在",
            "field": "id"
        }]}, 400)
        return resp
    for k, v in args.items():
        if v is not None and k == 'alert_disable':
            setattr(node, k, v)
            if v is True and node.sms_status is False:
                node.sms_status = True
        elif v and k == 'alert_peoples':
            setattr(node, k, ','.join(v))
        elif v and k == 'alert_level':
            setattr(node, k, v)
        elif v is not None and k == 'sms_status':
            if node.alert_disable is not True:
                setattr(node, k, v)
            else:
                resp = make_response({'msg': '修改主机详情失败', 'value': {}, 'errors': [{
                    "code": "400",
                    "desc": "告警关闭时无法开启短信告警",
                    "field": "alert_disable"
                }]}, 400)
                return resp
    people_list = []
    if node.alert_peoples and node.alert_peoples != "":
        for people_id in node.alert_peoples.split(','):
            people = con.query(Peoples).filter_by(id=people_id).first()
            if people:
                people_list.append(people.name)
    con.merge(node)
    con.commit()
    node_dict = node.to_dict()
    if node.expire_at:
        if node.expire_at.year == 1970:
            node_dict["expire_at"] = "--"
    for k, v in node_dict.items():
        if getattr(node, k) is None:
            node_dict[k] = ""
    node_dict["status"] = vm_status[node.status]
    node_dict["people_names_list"] = people_list
    node_dict["os"] = json.loads(node.os)
    node_dict["platform"] = json.loads(node.platform)
    resp = make_response({'msg': '修改主机详情成功', 'value': node_dict}, 200)
    con.close()
    return resp


def post_vms(args):
    con = create_con()
    node = con.query(Nodes).filter_by(id=args.get("id")).first()
    account = con.query(Account).filter_by(name=node.account_name).first()
    node = Node(account.name, account.api_key, account.api_sec)
    result = node.query_vm_detail(args.get("id"))
    if result['statusCode'] != 800:
        resp = make_response({'msg': '手动更新主机详情失败', 'value': {}, 'errors': [{
            "code": "400",
            "desc": "tyy接口未返回数据",
            "field": "tyy"
        }]}, 400)
        return resp
    return_objs = result.get('returnObj')
    node_status = return_objs.get('vmStatus')
    node_info = con.query(Nodes).filter_by(id=args.get("id")).first()
    if not node_status:
        node_status = "FREEZING"
    node_info.status = node_status
    people_list = []
    if node_info.alert_peoples and node_info.alert_peoples != "":
        for people_id in node_info.alert_peoples.split(','):
            people = con.query(Peoples).filter_by(id=people_id).first()
            if people:
                people_list.append(people.name)
    con.merge(node_info)
    con.commit()
    node_dict = node_info.to_dict()
    if node_info.expire_at:
        if node_info.expire_at.year == 1970:
            node_dict["expire_at"] = "--"
    node_dict["status"] = vm_status[node_status]
    node_dict["people_names_list"] = people_list
    node_dict["key"] = args.get("key")
    node_dict["os"] = json.loads(node_info.os)
    node_dict["platform"] = json.loads(node_info.platform)
    resp = make_response({'msg': '手动更新主机详情成功', 'value': node_dict}, 200)
    con.close()
    return resp
