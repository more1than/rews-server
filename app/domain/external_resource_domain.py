from app.models.alert_logs import AlertLogs
from app.models.disk import Disks
from app.models.nodes import Nodes
from app.models.peoples import *
from app.models.external_resource import ExternalResources
from app.models.network import *
from flask import make_response

from pkg.create_con import create_con
from pkg.resource_query import query_external_resource
from pkg.util.setting import setting


def get_external_resource(args=None, page_num=1, page_size=10):
    if int(page_num) <= 0:
        page_num = 1
    if int(page_size) <= 0:
        page_size = 10
    con = create_con()
    externals, externals_count = query_external_resource(con, args, page_num, page_size)
    list1 = []
    for external in externals:
        people_list = []
        external_dict = external.to_dict()
        if external.expire_at:
            if external.expire_at.year == 1970:
                external_dict["expire_at"] = "--"
        for k, v in external_dict.items():
            if getattr(external, k) is None:
                external_dict[k] = ""
        if external.alert_peoples and external.alert_peoples != "":
            for people_id in external.alert_peoples.split(','):
                people = con.query(Peoples).filter_by(id=people_id).first()
                if people:
                    people_list.append(people.name)
        external_dict["people_names_list"] = people_list
        list1.append(external_dict)
    resp = make_response({'msg': '查询外置资源列表成功', 'value': list1, 'total': externals_count}, 200)
    con.close()
    return resp


def get_external_resource_detail(external_id):
    con = create_con()
    external = con.query(ExternalResources).filter_by(id=external_id).first()
    if not external:
        resp = make_response({'msg': '查询外置资源详情失败', 'value': {}, 'errors': [{
            "code": "400",
            "desc": "该外置资源不存在",
            "field": "id"
        }]}, 400)
        return resp
    people_list = []
    external_dict = external.to_dict()
    for k, v in external_dict.items():
        if getattr(external, k) is None:
            external_dict[k] = ""
    if external.alert_peoples and external.alert_peoples != "":
        for people_id in external.alert_peoples.split(','):
            people = con.query(Peoples).filter_by(id=people_id).first()
            if people:
                people_data = {
                    "people_id": people_id,
                    "people_name": people.name,
                }
                people_list.append(people_data)
    node_info_list = []
    disk_info_list = []
    network_info_list = []
    external_info_list = []
    for acc_id in external_dict.get("related_objects"):
        node_info = con.query(Nodes).filter_by(id=acc_id.get("id")).first()
        disk_info = con.query(Disks).filter_by(id=acc_id.get("id")).first()
        network_info = con.query(NetWorks).filter_by(id=acc_id.get("id")).first()
        external_info = con.query(ExternalResources).filter_by(id=acc_id.get("id")).first()
        if node_info is not None:
            node = {
                "status": node_info.status,
                "hostname": node_info.hostname,
                "id": node_info.id,
                "instance_type": node_info.instance_type,
                "cloud_type": node_info.cloud_type,
                "os": json.loads(node_info.os),
                "ipaddress_lan": node_info.ipaddress_lan,
                "ipaddress_wan": node_info.ipaddress_wan
            }
            node_info_list.append(node)
        if disk_info is not None:
            disk = {
                "size": disk_info.size,
                "status": disk_info.status,
                "disk_type": disk_info.disk_type,
                "id": disk_info.id
            }
            disk_info_list.append(disk)
        if network_info is not None:
            network = {
                "id": network_info.id,
                "size": network_info.size,
                "status": network_info.status,
                "network_type": network_info.network_type,
            }
            network_info_list.append(network)
        if external_info is not None:
            external_main = {
                "id": external_info.id,
                "name": external_info.name,
                "status": external_info.status,
                "instance_type": external_info.instance_type
            }
            external_info_list.append(external_main)
    external_dict["nodes"] = node_info_list
    external_dict["disks"] = disk_info_list
    external_dict["networks"] = network_info_list
    external_dict["externals"] = external_info_list
    external_logs = con.query(AlertLogs).filter_by(external_resource_id=id).order_by(desc(AlertLogs.created_at))
    external_logs = [logs.to_dict() for logs in external_logs]
    external_dict["log_info"] = external_logs
    external_dict["people_names_list"] = people_list
    if external.expire_at:
        if external.expire_at.year == 1970:
            external_dict["expire_at"] = "--"
    resp = make_response({'msg': '查询外置资源详情成功', 'value': external_dict}, 200)
    con.close()
    return resp


def post_external_resource(args):
    con = create_con()
    external = ExternalResources()
    for k, v in args.items():
        setattr(external, k, v)
    due_time = datetime.strptime(str(external.expire_at), "%Y-%m-%d %H:%M:%S")
    local_time = datetime.now()
    difference = local_time - due_time
    if "-" in str(difference):
        external.status = "使用中"
    else:
        external.status = "过期"
    people_list = []
    if external.alert_peoples and external.alert_peoples != "":
        for people_id in external.alert_peoples.split(','):
            people = con.query(Peoples).filter_by(id=people_id).first()
            if people:
                people_list.append(people.name)
    con.add(external)
    con.commit()
    external_dict = external.to_dict()
    for k, v in external_dict.items():
        if getattr(external, k) is None:
            external_dict[k] = ""
    external_dict["people_names_list"] = people_list
    resp = make_response({'msg': '添加外置资源信息成功', 'value': external_dict}, 200)
    con.close()
    return resp


def put_external_resource(args, external_id):
    con = create_con()
    external = con.query(ExternalResources).filter_by(id=external_id).first()
    if not external:
        resp = make_response({'msg': '修改外置资源信息失败', 'value': {}, 'errors': [{
            "code": "400",
            "desc": "该外置资源不存在",
            "field": "id"
        }]}, 400)
        return resp
    for k, v in args.items():
        if v is not None and k == 'alert_disable':
            setattr(external, k, v)
            if v is True and external.sms_status is False:
                external.sms_status = True
        elif v and k == 'alert_peoples':
            setattr(external, k, ','.join(v))
        elif v and k == 'alert_level':
            setattr(external, k, v)
        elif v is not None and k == 'sms_status':
            if external.alert_disable is not True:
                setattr(external, k, v)
            else:
                resp = make_response({'msg': '修改外置资源信息失败', 'value': {}, 'errors': [{
                    "code": "400",
                    "desc": "告警关闭时无法开启短信告警",
                    "field": "alert_level"
                }]}, 400)
                return resp
    people_list = []
    if external.alert_peoples and external.alert_peoples != "":
        for people_id in external.alert_peoples.split(','):
            people = con.query(Peoples).filter_by(id=people_id).first()
            if people:
                people_list.append(people.name)
    con.merge(external)
    con.commit()
    external_dict = external.to_dict()
    for k, v in external_dict.items():
        if getattr(external, k) is None:
            external_dict[k] = ""
    external_dict["people_names_list"] = people_list
    resp = make_response({'msg': '修改外置资源信息成功', 'value': external_dict}, 200)
    con.close()
    return resp


def del_external_resource(external_id):
    con = create_con()
    result = con.query(ExternalResources).filter_by(id=external_id).delete()
    if result == 0:
        resp = make_response({'msg': '删除外置资源信息失败', 'value': {}, 'errors': [{
            "code": "400",
            "desc": "该外置资源不存在",
            "field": "id"
        }]}, 400)
        return resp
    con.commit()
    resp = make_response({'msg': '成功', 'value': ""}, 200)
    con.close()
    return resp


def get_default_people(con):
    people_msg = setting.get_email_config()
    name = people_msg.get("mail_name")
    result = con.query(Peoples).filter_by(name=name).first()
    result = result.to_dict()
    return result
