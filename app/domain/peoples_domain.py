from app.models.disk import Disks
from app.models.external_resource import ExternalResources
from app.models.network import NetWorks
from app.models.nodes import Nodes
from app.models.peoples import *
from flask import make_response
from pkg.create_con import create_con
from pkg.put_people_info import put_people_ids
from pkg.resource_query import query_peoples, get_content
from pkg.util.setting import setting


def get_peoples(args=None, page_num=1, page_size=10):
    if int(page_num) <= 0:
        page_num = 1
    if int(page_size) <= 0:
        page_size = 10
    con = create_con()
    people_info, people_info_count = query_peoples(con, args, page_num, page_size)
    list1 = []
    for people in people_info:
        all_info_list = get_content(con, people.id)
        people_dict = people.to_dict()
        for k, v in people_dict.items():
            if getattr(people, k) is None:
                people_dict[k] = ""
        people_dict["associated_id"] = all_info_list
        list1.append(people_dict)
    resp = make_response({'msg': '查询告警人员列表成功', 'value': list1, 'total': people_info_count}, 200)
    con.close()
    return resp


def get_people_details(people_id):
    resp = make_response({'msg': '查询告警人员详情失败', 'value': {}, 'errors': [{
        "code": "400",
        "desc": "暂不支持查询告警人员详细信息",
        "field": "id",
    }]}, 200)
    return resp


def post_people(args):
    con = create_con()
    people = Peoples()
    check_phone = con.query(Peoples).filter_by(phone=args.phone).first()
    if check_phone:
        resp = make_response({'msg': '添加告警人员信息失败', 'value': {}, 'errors': [{
            "code": "400",
            "desc": "该手机号码已经被注册",
            "field": "phone"
        }]}, 400)
        return resp
    check_mail = con.query(Peoples).filter_by(mail=args.mail).first()
    if check_mail:
        resp = make_response({'msg': '添加告警人员信息失败', 'value': {}, 'errors': [{
            "code": "400",
            "desc": "该邮箱已经被注册",
            "field": "mail"
        }]}, 400)
        return resp
    check_ding = con.query(Peoples).filter_by(im_ding=args.im_ding).first()
    if check_ding and args.im_ding:
        resp = make_response({'msg': '添加告警人员信息失败', 'value': {}, 'errors': [{
            "code": "400",
            "desc": "该钉钉账号已经被注册",
            "field": "im_ding"
        }]}, 400)
        return resp
    check_wechat = con.query(Peoples).filter_by(im_wechat=args.im_wechat).first()
    if check_wechat and args.im_wechat:
        resp = make_response({'msg': '添加告警人员信息失败', 'value': {}, 'errors': [{
            "code": "400",
            "desc": "该微信号码已经被注册",
            "field": "wechat"
        }]}, 400)
        return resp
    for k, v in args.items():
        setattr(people, k, v)
    con.add(people)
    con.commit()
    people_dict = people.to_dict()
    for k, v in people_dict.items():
        if getattr(people, k) is None:
            people_dict[k] = ""
    resp = make_response({'msg': '添加告警人员信息成功', 'value': people_dict}, 200)
    con.close()
    return resp


def put_peoples(args, people_id):
    con = create_con()
    try:
        people_info = con.query(Peoples).filter_by(id=people_id).first()
        if not people_info:
            resp = make_response({'msg': '修改告警人员信息失败', 'value': {}, 'errors': [{
                "code": "400",
                "desc": "该告警人员不存在",
                "field": "id"
            }]}, 400)
            return resp
        for k, v in args.items():
            if v is not None and k == 'alert_disable':
                setattr(people_info, k, v)
            elif v and k == 'alert_peoples':
                setattr(people_info, k, ','.join(v))
            elif v:
                setattr(people_info, k, v)
            if v and k == "nodes":
                for node_id in v:
                    node = con.query(Nodes).filter_by(id=node_id).first()
                    if not node.alert_peoples:
                        node.alert_peoples = people_id
                    else:
                        node.alert_peoples = node.alert_peoples + "," + people_id
                    con.merge(node)
                    con.commit()
            if v and k == "disks":
                for disk_id in v:
                    disk = con.query(Disks).filter_by(id=disk_id).first()
                    if not disk.alert_peoples:
                        disk.alert_peoples = people_id
                    else:
                        disk.alert_peoples = disk.alert_peoples + "," + people_id
                    con.merge(disk)
                    con.commit()
            if v and k == "networks":
                for network_id in v:
                    network = con.query(NetWorks).filter_by(id=network_id).first()
                    if not network.alert_peoples:
                        network.alert_peoples = people_id
                    else:
                        network.alert_peoples = network.alert_peoples + "," + people_id
                    con.merge(network)
                    con.commit()
            if v and k == "externals":
                for external_id in v:
                    external = con.query(ExternalResources).filter_by(id=external_id).first()
                    if not external.alert_peoples:
                        external.alert_peoples = people_id
                    else:
                        external.alert_peoples = external.alert_peoples + "," + people_id
                    con.merge(external)
                    con.commit()
        con.merge(people_info)
        con.commit()
    except Exception as e:
        if "phone" in str(e.args) and "1062" in str(e.args):
            resp = make_response({'msg': '修改告警人员信息失败', 'value': {}, 'errors': [{
                "code": "400",
                "desc": "该手机号码已经被注册",
                "field": "phone"
            }]}, 400)
            return resp
        if "mail" in str(e.args) and "1062" in str(e.args):
            resp = make_response({'msg': '修改告警人员信息失败', 'value': {}, 'errors': [{
                "code": "400",
                "desc": "该邮箱地址已经被注册",
                "field": "mail"
            }]}, 400)
            return resp
        if "im_ding" in str(e.args) and "1062" in str(e.args):
            resp = make_response({'msg': '修改告警人员信息失败', 'value': {}, 'errors': [{
                "code": "400",
                "desc": "该钉钉账号已经被注册",
                "field": "im_ding"
            }]}, 400)
            return resp
        if "im_wechat" in str(e.args) and "1062" in str(e.args):
            resp = make_response({'msg': '修改告警人员信息失败', 'value': {}, 'errors': [{
                "code": "400",
                "desc": "该微信号码已经被注册",
                "field": "im_wechat"
            }]}, 400)
            return resp
    people_dict = people_info.to_dict()
    for k, v in people_dict.items():
        if getattr(people_info, k) is None:
            people_dict[k] = ""
    resp = make_response({'msg': '修改告警人员信息成功', 'value': people_dict}, 200)
    con.close()
    return resp


def del_peoples(people_id):
    con = create_con()
    mail_msg = setting.get_email_config()
    mail_user = mail_msg.get("mail_user")
    people_info = con.query(Peoples).filter_by(id=people_id).first()
    if people_info and people_info.mail == mail_user:
        resp = make_response({'msg': '删除告警人员信息失败', 'value': {}, 'errors': [{
            "code": "400",
            "desc": "无法删除默认告警人员",
            "field": "id"
        }]}, 400)
        return resp
    response = con.query(Peoples).filter_by(id=people_id).delete()
    if response == 0:
        resp = make_response({'msg': '删除告警人员信息失败', 'value': {}, 'errors': [{
            "code": "400",
            "desc": "该告警人员不存在",
            "field": "id"
        }]}, 400)
        return resp
    con.commit()
    put_people_ids(people_id)
    resp = make_response({'msg': '删除告警人员信息成功', 'value': []}, 200)
    con.close()
    return resp
