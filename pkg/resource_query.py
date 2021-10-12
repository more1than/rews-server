from app.models.account import Account
from app.models.alert_logs import *
from app.models.disk import *
from app.models.external_resource import *
from app.models.network import *
from app.models.nodes import *
from app.models.peoples import *
from pkg.dict_page import Page


def query_vms(con, args, page_num, page_size):
    nodes = con.query(Nodes)
    if args is not None:
        if args.get("cloud_type") is not None:
            nodes = nodes.filter_by(cloud_type=args.get("cloud_type"))
        if args.get("instance_type") is not None:
            nodes = nodes.filter_by(instance_type=args.get("instance_type"))
        if args.get("hostname") is not None:
            nodes = nodes.filter(or_(Nodes.id.like('%{keyword}%'.format(keyword=args.get("hostname"))),
                                     Nodes.hostname.like('%{keyword}%'.format(keyword=args.get("hostname")))))
        if args.get("os") is not None:
            nodes = nodes.filter(Nodes.os.like('%{keyword}%'.format(keyword=args.get("os"))))
        if args.get("ip") is not None:
            nodes = nodes.filter(or_(Nodes.ipaddress_lan.like('%{keyword}%'.format(keyword=args.get("ip"))),
                                     Nodes.ipaddress_wan.like('%{keyword}%'.format(keyword=args.get("ip")))))
        if args.get("status") is not None:
            nodes = nodes.filter_by(status=args.get("status"))
        if args.get("buy_start") is not None and args.get("buy_end") is not None:
            nodes = nodes.filter(
                Nodes.buy_at.between(args.get("buy_start"), args.get("buy_end")))
        if args.get("expire_start") is not None and args.get("expire_end") is not None:
            nodes = nodes.filter(
                Nodes.expire_at.between(args.get("expire_start"), args.get("expire_end")))
        if args.get("alert_peoples") is not None:
            nodes = nodes.filter_by(alert_peoples=args.get("alert_peoples"))
        if args.get("alert_level") is not None:
            nodes = nodes.filter_by(alert_level=args.get("alert_level"))
        if args.get("alert_disable") is not None:
            if args.get("alert_disable") == "true":
                nodes = nodes.filter_by(alert_disable=True)
            elif args.get("alert_disable") == "false":
                nodes = nodes.filter_by(alert_disable=False)
        if args.get("sms_status") is not None:
            if args.get("sms_status") == "true":
                nodes = nodes.filter_by(sms_status=True)
            elif args.get("sms_status") == "false":
                nodes = nodes.filter_by(sms_status=False)
    return nodes.order_by(desc(Nodes.buy_at)).limit(page_size).offset(
        int(page_size) * (int(page_num) - 1)), nodes.count()


def query_disks(con, args, page_num, page_size):
    disks = con.query(Disks)
    if args is not None:
        if args.get("disk_id") is not None:
            disks = disks.filter(Disks.id.like('%{keyword}%'.format(keyword=args.get("disk_id"))))
        if args.get("cloud_type") is not None:
            disks = disks.filter_by(cloud_type=args.get("cloud_type"))
        if args.get("instance_type") is not None:
            disks = disks.filter_by(instance_type=args.get("instance_type"))
        if args.get("size") is not None:
            disks = disks.filter_by(size=args.get("size"))
        if args.get("buy_start") is not None and args.get("buy_end") is not None:
            disks = disks.filter(
                Disks.buy_at.between(args.get("buy_start"), args.get("buy_end")))
        if args.get("expire_start") is not None and args.get("expire_end") is not None:
            disks = disks.filter(
                Disks.expire_at.between(args.get("expire_start"), args.get("expire_end")))
        if args.get("node_name") is not None:
            disks = disks.filter(
                or_(Disks.node_name.like('%{keyword}%'.format(keyword=args.get("node_name"))),
                    Disks.node_id.like('%{keyword}%'.format(keyword=args.get("node_name")))))
        if args.get("status") is not None:
            disks = disks.filter_by(status=args.get("status"))
        if args.get("alert_level") is not None:
            disks = disks.filter_by(alert_level=args.get("alert_level"))
        if args.get("alert_disable") is not None:
            if args.get("alert_disable") == "true":
                disks = disks.filter_by(alert_disable=True)
            elif args.get("alert_disable") == "false":
                disks = disks.filter_by(alert_disable=False)
        if args.get("sms_status") is not None:
            if args.get("sms_status") == "true":
                disks = disks.filter_by(sms_status=True)
            elif args.get("sms_status") == "false":
                disks = disks.filter_by(sms_status=False)
        if args.get("alert_peoples") is not None:
            disks = disks.filter_by(alert_peoples=args.get("alert_peoples"))
    return disks.order_by(desc(Disks.buy_at)).limit(page_size).offset(
        int(page_size) * (int(page_num) - 1)), disks.count()


def query_networks(con, args, page_num, page_size):
    networks = con.query(NetWorks)
    if args is not None:
        if args.get("id") is not None:
            networks = networks.filter(NetWorks.id.like('%{keyword}%'.format(keyword=args.get("id"))))
        if args.get("cloud_type") is not None:
            networks = networks.filter_by(cloud_type=args.get("cloud_type"))
        if args.get("status") is not None:
            networks = networks.filter_by(status=args.get("status"))
        if args.get("buy_start") is not None and args.get("buy_end") is not None:
            networks = networks.filter(
                NetWorks.buy_at.between(args.get("buy_start"), args.get("buy_end")))
        if args.get("expire_start") is not None and args.get("expire_end") is not None:
            networks = networks.filter(
                NetWorks.expire_at.between(args.get("expire_start"), args.get("expire_end")))
        if args.get("alert_level") is not None:
            networks = networks.filter_by(alert_level=args.get("alert_level"))
        if args.get("alert_disable") is not None:
            if args.get("alert_disable") == "true":
                networks = networks.filter_by(alert_disable=True)
            elif args.get("alert_disable") == "false":
                networks = networks.filter_by(alert_disable=False)
        if args.get("sms_status") is not None:
            if args.get("sms_status") == "true":
                networks = networks.filter_by(sms_status=True)
            elif args.get("sms_status") == "false":
                networks = networks.filter_by(sms_status=False)
        if args.get("alert_peoples") is not None:
            networks = networks.filter_by(alert_peoples=args.get("alert_peoples"))
    return networks.order_by(desc(NetWorks.buy_at)).limit(page_size).offset(
        int(page_size) * (int(page_num) - 1)), networks.count()


def query_external_resource(con, args, page_num, page_size):
    external_resource = con.query(ExternalResources)
    if args is not None:
        if args.get("name") is not None:
            external_resource = external_resource.filter(
                or_(ExternalResources.name.like('%{keyword}%'.format(keyword=args.get("name"))),
                    ExternalResources.id.like('%{keyword}%'.format(keyword=args.get("name")))))
        if args.get("instance_type") is not None:
            external_resource = external_resource.filter(
                ExternalResources.instance_type.like('%{keyword}%'.format(keyword=args.get("instance_type"))))
        if args.get("status") is not None:
            external_resource = external_resource.filter_by(status=args.get("status"))
        if args.get("buy_start") is not None and args.get("buy_end") is not None:
            external_resource = external_resource.filter(
                ExternalResources.buy_at.between(args.get("buy_start"), args.get("buy_end")))
        if args.get("expire_start") is not None and args.get("expire_end") is not None:
            external_resource = external_resource.filter(
                ExternalResources.expire_at.between(args.get("expire_start"), args.get("expire_end")))
        if args.get("alert_level") is not None:
            external_resource = external_resource.filter_by(alert_level=args.get("alert_level"))
        if args.get("alert_disable") is not None:
            if args.get("alert_disable") == "true":
                external_resource = external_resource.filter_by(alert_disable=True)
            elif args.get("alert_disable") == "false":
                external_resource = external_resource.filter_by(alert_disable=False)
        if args.get("sms_status") is not None:
            if args.get("sms_status") == "true":
                external_resource = external_resource.filter_by(sms_status=True)
            elif args.get("sms_status") == "false":
                external_resource = external_resource.filter_by(sms_status=False)
        if args.get("alert_peoples") is not None:
            external_resource = external_resource.filter_by(alert_peoples=args.get("alert_peoples"))
    return external_resource.order_by(desc(ExternalResources.buy_at)).limit(page_size).offset(
        int(page_size) * (int(page_num) - 1)), external_resource.count()


def query_logs(con, args, page_num, page_size):
    logs = con.query(AlertLogs)
    if args is not None:
        if args.get("alert_level") is not None:
            logs = logs.filter_by(alert_level=args.get("alert_level"))
        if args.get("id") is not None:
            logs = logs.filter(
                or_(AlertLogs.node_id.like('%{keyword}%'.format(keyword=args.get("id"))),
                    AlertLogs.disk_id.like('%{keyword}%'.format(keyword=args.get("id"))),
                    AlertLogs.network_id.like('%{keyword}%'.format(keyword=args.get("id"))),
                    AlertLogs.external_resource_id.like('%{keyword}%'.format(keyword=args.get("id"))),
                    ))
        if args.get("start_time") is not None and args.get("end_time") is not None:
            logs = logs.filter(
                AlertLogs.created_at.between(args.get("start_time"), args.get("end_time")))
    return logs.order_by(desc(AlertLogs.created_at)).limit(page_size).offset(
        int(page_size) * (int(page_num) - 1)), logs.count()


def query_peoples(con, args, page_num, page_size):
    people = con.query(Peoples)
    if args is not None:
        if args.get("name") is not None:
            people = people.filter(
                or_(Peoples.name.like('%{keyword}%'.format(keyword=args.get("name"))),
                    Peoples.id.like('%{keyword}%'.format(keyword=args.get("name")))))
        if args.get("mail") is not None:
            people = people.filter(Peoples.mail.like('%{keyword}%'.format(keyword=args.get("mail"))))
        if args.get("phone") is not None:
            people = people.filter(Peoples.phone.like('%{keyword}%'.format(keyword=args.get("phone"))))
    return people.order_by(desc(Peoples.created_at)).limit(page_size).offset(
        int(page_size) * (int(page_num) - 1)), people.count()


def query_account(con, args, page_num, page_size):
    account = con.query(Account)
    if args is not None:
        if args.get("cloud_type") is not None:
            account = account.filter_by(cloud_type=args.get("cloud_type"))
        if args.get("name") is not None:
            account = account.filter(Account.name.like('%{keyword}%'.format(keyword=args.get("name"))))
        if args.get("api_key") is not None:
            account = account.filter(Account.api_key.like('%{keyword}%'.format(keyword=args.get("api_key"))))
        if args.get("api_sec") is not None:
            account = account.filter(Account.api_sec.like('%{keyword}%'.format(keyword=args.get("api_sec"))))
    return account.limit(page_size).offset(int(page_size) * (int(page_num) - 1)), account.count()


def check_data(con, args):
    nodes = con.query(Nodes)
    disks = con.query(Disks)
    networks = con.query(NetWorks)
    externals = con.query(ExternalResources)
    if args is not None:
        if args.get("id") is not None:
            nodes = nodes.filter(Nodes.id.like('%{keyword}%'.format(keyword=args.get("id"))))
            disks = disks.filter(Disks.id.like('%{keyword}%'.format(keyword=args.get("id"))))
            networks = networks.filter(NetWorks.id.like('%{keyword}%'.format(keyword=args.get("id"))))
            externals = externals.filter(ExternalResources.id.like('%{keyword}%'.format(keyword=args.get("id"))))
        if args.get("instance_type") is not None:
            nodes = nodes.filter(Nodes.instance_type.like('%{keyword}%'.format(keyword=args.get("instance_type"))))
            disks = disks.filter(Disks.instance_type.like('%{keyword}%'.format(keyword=args.get("instance_type"))))
            networks = networks.filter(
                NetWorks.instance_type.like('%{keyword}%'.format(keyword=args.get("instance_type"))))
            externals = externals.filter(
                ExternalResources.instance_type.like('%{keyword}%'.format(keyword=args.get("instance_type"))))
        if args.get("cloud_type") is not None:
            nodes = nodes.filter_by(cloud_type=args.get("cloud_type"))
            disks = disks.filter_by(cloud_type=args.get("cloud_type"))
            networks = networks.filter_by(cloud_type=args.get("cloud_type"))
            externals = []
        if args.get("hostname") is not None:
            nodes = nodes.filter(Nodes.hostname.like('%{keyword}%'.format(keyword=args.get("hostname"))))
            disks = []
            networks = []
            externals = []
        if args.get("name") is not None:
            nodes = []
            disks = []
            networks = []
            if externals:
                externals = externals.filter(
                    ExternalResources.name.like('%{keyword}%'.format(keyword=args.get("name"))))
    all_data = []
    for node in nodes:
        node_info = {
            "type": "nodes",
            "id": node.id,
            "instance_type": node.instance_type,
            "hostname": node.hostname,
            "cloud_type": node.cloud_type,
        }
        all_data.append(node_info)
    for disk in disks:
        disk_info = {
            "type": "disks",
            "id": disk.id,
            "instance_type": disk.instance_type,
            "cloud_type": disk.cloud_type,
        }
        all_data.append(disk_info)
    for network in networks:
        network_info = {
            "type": "networks",
            "id": network.id,
            "instance_type": network.instance_type,
            "cloud_type": network.cloud_type,
        }
        all_data.append(network_info)
    for external in externals:
        external_info = {
            "type": "externals",
            "id": external.id,
            "instance_type": external.instance_type,
            "name": external.name,
        }
        all_data.append(external_info)
    resp = []
    flag = 0
    if args is not None:
        if args.get("type"):
            flag = 1
        if args.get("type") == "nodes":
            for info in all_data:
                if info.get("type") == "nodes":
                    resp.append(info)
                else:
                    del info
        elif args.get("type") == "disks":
            for info in all_data:
                if info.get("type") == "disks":
                    resp.append(info)
                else:
                    del info
        elif args.get("type") == "networks":
            for info in all_data:
                if info.get("type") == "networks":
                    resp.append(info)
                else:
                    del info
        elif args.get("type") == "externals":
            for info in all_data:
                if info.get("type") == "externals":
                    resp.append(info)
                else:
                    del info
    if not args:
        resp = all_data
    elif not resp and flag == 0:
        resp = all_data
    all_count = len(resp)
    if args.get("pageNum"):
        data = Page(int(args.get("pageNum")), int(args.get("pageSize", 10)), resp)
        resp = data.get_str_json()
    return resp, all_count


def get_content(con, people_id):
    nodes = con.query(Nodes).all()
    disks = con.query(Disks).all()
    networks = con.query(NetWorks).all()
    externals = con.query(ExternalResources).all()
    all_id_list = []
    for node in nodes:
        if node.alert_peoples is not None:
            if people_id in node.alert_peoples:
                all_id_list.append({"type": "nodes", "id": node.id})
    for disk in disks:
        if disk.alert_peoples is not None:
            if people_id in disk.alert_peoples:
                all_id_list.append({"type": "disks", "id": disk.id})
    for network in networks:
        if network.alert_peoples is not None:
            if people_id in network.alert_peoples:
                all_id_list.append({"type": "networks", "id": network.id})
    for external in externals:
        if external.alert_peoples is not None:
            if people_id in external.alert_peoples:
                all_id_list.append({"type": "externals", "id": external.id})
    return all_id_list
