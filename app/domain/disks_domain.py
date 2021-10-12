from app.models.account import Account
from app.models.alert_logs import AlertLogs
from app.models.peoples import *
from app.models.disk import *
from flask import make_response
from pkg.create_con import create_con
from pkg.cloud_provider.ctyun import Disk
from pkg.resource_query import query_disks

disk_status = {"creating": "创建中", "available": "未挂载", "in-use": "正在使用", "error": "创建错误", "attaching": "挂载中",
               "detaching": "卸载中", "restoring-backup": "备份恢复中", "error_restoring": "备份恢复错误", "uploading": "上传中",
               "downloading": "下载中", "expired": "过期"}


def get_disks(args=None, page_num=1, page_size=10):
    if int(page_num) <= 0:
        page_num = 1
    if int(page_size) <= 0:
        page_size = 10
    con = create_con()
    disks, disks_count = query_disks(con, args, page_num, page_size)
    list1 = []
    for disk in disks:
        people_list = []
        disk.status = disk_status[disk.status]
        disk_dict = disk.to_dict()
        if disk.expire_at:
            if disk.expire_at.year == 1970:
                disk_dict["expire_at"] = "--"
        for k, v in disk_dict.items():
            if getattr(disk, k) is None:
                disk_dict[k] = ""
        if disk.alert_peoples and disk.alert_peoples != "":
            for people_id in disk.alert_peoples.split(','):
                people = con.query(Peoples).filter_by(id=people_id).first()
                if people:
                    people_list.append(people.name)
        disk_dict["people_names_list"] = people_list
        list1.append(disk_dict)
    resp = make_response({'msg': '查询磁盘列表成功', 'value': list1, "total": disks_count}, 200)
    con.close()
    return resp


def get_disk_detail(volume_id):
    con = create_con()
    disk_info = con.query(Disks).filter_by(id=volume_id).first()
    if not disk_info:
        resp = make_response({'msg': '查询磁盘详情失败', 'value': {}, 'errors': [{
            "code": "400",
            "desc": "该磁盘信息不存在",
            "field": "id"
        }]}, 400)
        return resp
    people_list = []
    disk_dict = disk_info.to_dict()
    for k, v in disk_dict.items():
        if getattr(disk_info, k) is None:
            disk_dict[k] = ""
    if disk_info.alert_peoples and disk_info.alert_peoples != "":
        for people_id in disk_info.alert_peoples.split(','):
            people = con.query(Peoples).filter_by(id=people_id).first()
            if people:
                people_data = {
                    "people_id": people_id,
                    "people_name": people.name,
                }
                people_list.append(people_data)
    disk_logs = con.query(AlertLogs).filter_by(disk_id=volume_id).order_by(desc(AlertLogs.created_at))
    disk_logs = [logs.to_dict() for logs in disk_logs]
    disk_dict["log_info"] = disk_logs
    disk_dict["people_names_list"] = people_list
    disk_dict["status"] = disk_status[disk_info.status]
    if disk_info.expire_at:
        if disk_info.expire_at.year == 1970:
            disk_dict["expire_at"] = "--"
    resp = make_response({'msg': '查询磁盘详情成功', 'value': disk_dict}, 200)
    con.close()
    return resp


def put_disks(args, volume_id):
    con = create_con()
    disk = con.query(Disks).filter_by(id=volume_id).first()
    if not disk:
        resp = make_response({'msg': '修改磁盘详情失败', 'value': {}, 'errors': [{
            "code": "400",
            "desc": "该磁盘信息不存在",
            "field": "id"
        }]}, 400)
        return resp
    for k, v in args.items():
        if v is not None and k == 'alert_disable':
            setattr(disk, k, v)
            if v is True and disk.sms_status is False:
                disk.sms_status = True
        elif v and k == 'alert_peoples':
            setattr(disk, k, ','.join(v))
        elif v and k == 'alert_level':
            setattr(disk, k, v)
        elif v is not None and k == 'sms_status':
            if disk.alert_disable is not True:
                setattr(disk, k, v)
            else:
                resp = make_response({'msg': '修改磁盘信息失败', 'value': {}, 'errors': [{
                    "code": "400",
                    "desc": "告警关闭时无法开启短信告警",
                    "field": "alert_level"
                }]}, 400)
                return resp
    people_list = []
    if disk.alert_peoples and disk.alert_peoples != "":
        for people_id in disk.alert_peoples.split(','):
            people = con.query(Peoples).filter_by(id=people_id).first()
            if people:
                people_list.append(people.name)
    con.merge(disk)
    con.commit()
    disk_dict = disk.to_dict()
    for k, v in disk_dict.items():
        if getattr(disk, k) is None:
            disk_dict[k] = ""
    disk_dict["status"] = disk_status[disk.status]
    disk_dict["people_names_list"] = people_list
    resp = make_response({'msg': '修改磁盘详情成功', 'value': disk_dict}, 200)
    con.close()
    return resp


def post_disks(args):
    con = create_con()
    disk = con.query(Disks).filter_by(id=args.get("id")).first()
    account = con.query(Account).filter_by(name=disk.account_name).first()
    disk = Disk(account.name, account.api_key, account.api_sec)
    result = disk.query_volumes()
    if result['statusCode'] != 800:
        resp = make_response({'msg': '手动更新磁盘详情失败', 'value': {}, 'errors': [{
            "code": "400",
            "desc": "tyy接口未返回数据",
            "field": "tyy"
        }]}, 400)
        return resp
    volumes = result.get('returnObj').get("volumes")
    volume_status = ""
    for volume in volumes:
        if volume.get("id") == args.get("id"):
            volume_status = volume.get("status")
    disk_info = con.query(Disks).filter_by(id=args.get("id")).first()
    if disk_info.status == "expired":
        pass
    else:
        disk_info.status = volume_status
    people_list = []
    if disk_info.alert_peoples and disk_info.alert_peoples != "":
        for people_id in disk_info.alert_peoples.split(','):
            people = con.query(Peoples).filter_by(id=people_id).first()
            if people:
                people_list.append(people.name)
    con.merge(disk_info)
    con.commit()
    disk_dict = disk_info.to_dict()
    if disk_info.status == "expired":
        disk_dict["status"] = "过期"
    else:
        disk_dict["status"] = disk_status[volume_status]
    disk_dict["key"] = args.get("key")
    disk_dict["people_names_list"] = people_list
    resp = make_response({'msg': '手动更新磁盘详情成功', 'value': disk_dict}, 200)
    con.close()
    return resp
