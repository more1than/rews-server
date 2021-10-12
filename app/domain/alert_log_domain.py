from app.models.alert_logs import *
from app.models.peoples import *
from flask import make_response
from pkg.create_con import create_con
from pkg.resource_query import query_logs


def get_alert_logs(args=None, page_num=1, page_size=10):
    if int(page_num) <= 0:
        page_num = 1
    if int(page_size) <= 0:
        page_size = 10
    con = create_con()
    log_infos, log_infos_count = query_logs(con, args, page_num, page_size)
    list1 = []
    for log in log_infos:
        people_list = []
        log_dict = log.to_dict()
        for k, v in log_dict.items():
            if getattr(log, k) is None:
                log_dict[k] = ""
        if log.alert_peoples:
            for people_id in log.alert_peoples.split(','):
                people = con.query(Peoples).filter_by(id=people_id).first()
                if people:
                    people_list.append(people.name)
        log_dict["people_names_list"] = people_list
        list1.append(log_dict)
    resp = make_response({'msg': '成功', 'value': list1, 'total': log_infos_count}, 200)
    con.close()
    return resp


def get_alert_logs_detail(log_id):
    con = create_con()
    log_info = con.query(AlertLogs).filter_by(id=log_id).first()
    if not log_info:
        resp = make_response({'msg': '查询日志信息详情失败', 'value': {}, 'errors': [{
            "code": "400",
            "desc": "该日志信息不存在",
            "field": "id"
        }]}, 400)
        return resp
    people_list = []
    log_dict = log_info.to_dict()
    for k, v in log_dict.items():
        if getattr(log_info, k) is None:
            log_dict[k] = ""
    if log_info.alert_peoples:
        for people_id in log_info.alert_peoples.split(','):
            people = con.query(Peoples).filter_by(id=people_id).first()
            if people:
                people_data = {
                    "people_id": people_id,
                    "people_name": people.name,
                }
                people_list.append(people_data)
    log_dict["people_names_list"] = people_list
    resp = make_response({'msg': '查询日志信息详情成功', 'value': log_dict}, 200)
    con.close()
    return resp
