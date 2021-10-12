import threading
from app.models.account import Account
from flask import make_response
from app.models.disk import Disks
from app.models.network import NetWorks
from app.models.nodes import Nodes
from pkg.Timertask.get_datas import update_database
from pkg.account_delete import account_delete
from pkg.create_con import create_con
from pkg.resource_query import query_account
from pkg.util.setting import setting


def get_accounts(args=None, page_num=1, page_size=10):
    if int(page_num) <= 0:
        page_num = 1
    if int(page_size) <= 0:
        page_size = 10
    con = create_con()
    accounts, account_count = query_account(con, args, page_num, page_size)
    list1 = []
    for account in accounts:
        account_dict = account.to_dict()
        for k, v in account_dict.items():
            if getattr(account, k) is None:
                account_dict[k] = ""
        key = account.api_key[:4] + (len(account.api_key)-4)*"*"
        sec = account.api_sec[:4] + (len(account.api_sec)-4)*"*"
        account_dict["api_key"] = key
        account_dict["api_sec"] = sec
        list1.append(account_dict)
    resp = make_response({'msg': '查询账号列表成功', 'value': list1, "total": account_count}, 200)
    con.close()
    return resp


def get_account_detail(account_id):
    con = create_con()
    account = con.query(Account).filter_by(id=account_id).first()
    if not account:
        resp = make_response({'msg': '查询账号详情失败', 'value': {}, 'errors': [{
            "code": "400",
            "desc": "该账号信息不存在",
            "field": "id"
        }]}, 400)
        return resp
    account_dict = account.to_dict()
    for k, v in account_dict.items():
        if getattr(account_dict, k) is None:
            account_dict[k] = ""
    resp = make_response({'msg': '查询账号详情成功', 'value': account_dict}, 200)
    con.close()
    return resp


def put_account(args, account_id):
    con = create_con()
    account = con.query(Account).filter_by(id=account_id).first()
    if not account:
        resp = make_response({'msg': '修改账号详情失败', 'value': [], 'errors': [{
            "code": "400",
            "desc": "该账号信息不存在",
            "field": "id"
        }]}, 400)
        return resp
    have_name = con.query(Account).filter_by(name=args.get("name")).first()
    if account.name != args.get("name") and have_name is not None:
        resp = make_response({'msg': '修改账号信息失败', 'value': [], 'errors': [{
            "code": "400",
            "desc": "该账号名称已存在",
            "field": "name"
        }]}, 400)
        return resp
    nodes = con.query(Nodes).filter_by(account_name=account.name).all()
    for node in nodes:
        node.account_name = args.get("name")
        con.merge(node)
    disks = con.query(Disks).filter_by(account_name=account.name).all()
    for disk in disks:
        disk.account_name = args.get("name")
        con.merge(disk)
    networks = con.query(NetWorks).filter_by(account_name=account.name).all()
    for network in networks:
        network.account_name = args.get("name")
        con.merge(network)
    for k, v in args.items():
        if v is not None:
            setattr(account, k, v)
    con.merge(account)
    con.commit()
    account_dict = account.to_dict()
    for k, v in account_dict.items():
        if getattr(account, k) is None:
            account_dict[k] = ""
    resp = make_response({'msg': '修改账号详情成功', 'value': account_dict}, 202)
    con.close()
    t = threading.Thread(target=update_database, args=[account])
    t.start()
    return resp


def post_account(args):
    con = create_con()
    account = Account()
    have_name = con.query(Account).filter_by(name=args.get("name")).first()
    if have_name:
        resp = make_response({'msg': '添加账号信息失败', 'value': [], 'errors': [{
            "code": "400",
            "desc": "该账号名称已存在",
            "field": "name"
        }]}, 400)
        return resp
    for k, v in args.items():
        setattr(account, k, v)
    con.add(account)
    con.commit()
    account_dict = account.to_dict()
    for k, v in account_dict.items():
        if getattr(account, k) is None:
            account_dict[k] = ""
    resp = make_response({'msg': '添加账号信息成功', 'value': account_dict}, 202)
    con.close()
    t = threading.Thread(target=update_database, args=[account])
    t.start()
    return resp


def del_account(account_id):
    con = create_con()
    tyy_info = setting.get_tty_config()
    username = tyy_info.get("AccountName")
    account = con.query(Account).filter_by(id=account_id).first()
    if account and account.name == username:
        resp = make_response({'msg': '删除账号信息失败', 'value': [], 'errors': [{
            "code": "400",
            "desc": "无法删除默认账号",
            "field": "id"
        }]}, 400)
        return resp
    response = con.query(Account).filter_by(id=account_id).delete()
    if response == 0:
        resp = make_response({'msg': '删除账号信息失败', 'value': [], 'errors': [{
            "code": "400",
            "desc": "该账号不存在",
            "field": "id"
        }]}, 400)
        return resp
    con.commit()
    resp = make_response({'msg': '删除账号信息成功', 'value': []}, 202)
    t = threading.Thread(target=account_delete, args=[account])
    t.start()
    con.close()
    return resp
