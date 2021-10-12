from app.models.disk import Disks
from app.models.external_resource import ExternalResources
from app.models.network import NetWorks
from app.models.nodes import Nodes
from flask import make_response
from pkg.create_con import create_con
from pkg.resource_query import check_data


def get_all_resource(args=None):
    con = create_con()
    all_data, all_count = check_data(con, args)
    resp = make_response({'msg': '查询资源列表成功', 'value': all_data, 'total': all_count}, 200)
    con.close()
    return resp


def put_all_info(args=None):
    con = create_con()
    if args.get("type") == "nodes":
        for node_id in args.get("ids"):
            node = con.query(Nodes).filter_by(id=node_id).first()
            if args.get("alert_level") is not None:
                node.alert_level = args.get("alert_level")
            if args.get("alert_disable") is not None:
                node.alert_disable = args.get("alert_disable")
                if node.alert_disable is True and node.sms_status is False:
                    node.sms_status = True
            if args.get("sms_status") is not None:
                node.sms_status = args.get("sms_status")
            con.merge(node)
            con.commit()
    elif args.get("type") == "disks":
        for disk_id in args.get("ids"):
            disk = con.query(Disks).filter_by(id=disk_id).first()
            if args.get("alert_level") is not None:
                disk.alert_level = args.get("alert_level")
            if args.get("alert_disable") is not None:
                disk.alert_disable = args.get("alert_disable")
                if disk.alert_disable is True and disk.sms_status is False:
                    disk.sms_status = True
            if args.get("sms_status") is not None:
                disk.sms_status = args.get("sms_status")
            con.merge(disk)
            con.commit()
    elif args.get("type") == "networks":
        for network_id in args.get("ids"):
            network = con.query(NetWorks).filter_by(id=network_id).first()
            if args.get("alert_level") is not None:
                network.alert_level = args.get("alert_level")
            if args.get("alert_disable") is not None:
                network.alert_disable = args.get("alert_disable")
                if network.alert_disable is True and network.sms_status is False:
                    network.sms_status = True
            if args.get("sms_status") is not None:
                network.sms_status = args.get("sms_status")
            con.merge(network)
            con.commit()
    elif args.get("type") == "externals":
        for external_id in args.get("ids"):
            external = con.query(ExternalResources).filter_by(id=external_id).first()
            if args.get("alert_level") is not None:
                external.alert_level = args.get("alert_level")
            if args.get("alert_disable") is not None:
                external.alert_disable = args.get("alert_disable")
                if external.alert_disable is True and external.sms_status is False:
                    external.sms_status = True
            if args.get("sms_status") is not None:
                external.sms_status = args.get("sms_status")
            con.merge(external)
            con.commit()
    resp = make_response({'msg': '成功', 'value': []}, 200)
    con.close()
    return resp


def people_choose(args):
    con = create_con()
    if args.get("nodes"):
        nodes = con.query(Nodes).all()
        for node in nodes:
            if node.id not in args.get("nodes"):
                if node.alert_peoples is None:
                    continue
                elif args.get("people_id") in node.alert_peoples:
                    id_list = node.alert_peoples.split(",")
                    id_list.remove(args.get("people_id"))
                    node.alert_peoples = ','.join(id_list)
            elif node.id in args.get("nodes"):
                if node.alert_peoples is None:
                    node.alert_peoples = args.get("people_id")
                else:
                    if args.get("people_id") not in node.alert_peoples:
                        node.alert_peoples = node.alert_peoples + "," + args.get("people_id")
            con.merge(node)
            con.commit()
    elif not args.get("nodes"):
        nodes = con.query(Nodes).all()
        for node in nodes:
            if node.alert_peoples is None:
                continue
            elif args.get("people_id") in node.alert_peoples:
                id_list = node.alert_peoples.split(",")
                id_list.remove(args.get("people_id"))
                node.alert_peoples = ','.join(id_list)
            con.merge(node)
            con.commit()
    if args.get("disks"):
        disks = con.query(Disks).all()
        for disk in disks:
            if disk.id not in args.get("disks"):
                if disk.alert_peoples is None:
                    continue
                elif args.get("people_id") in disk.alert_peoples:
                    id_list = disk.alert_peoples.split(",")
                    id_list.remove(args.get("people_id"))
                    disk.alert_peoples = ','.join(id_list)
            elif disk.id in args.get("disks"):
                if disk.alert_peoples is None:
                    disk.alert_peoples = args.get("people_id")
                else:
                    if args.get("people_id") not in disk.alert_peoples:
                        disk.alert_peoples = disk.alert_peoples + "," + args.get("people_id")
            con.merge(disk)
            con.commit()
    elif not args.get("disks"):
        disks = con.query(Disks).all()
        for disk in disks:
            if disk.alert_peoples is None:
                continue
            elif args.get("people_id") in disk.alert_peoples:
                id_list = disk.alert_peoples.split(",")
                id_list.remove(args.get("people_id"))
                disk.alert_peoples = ','.join(id_list)
            con.merge(disk)
            con.commit()
    if args.get("networks"):
        networks = con.query(NetWorks).all()
        for network in networks:
            if network.id not in args.get("networks"):
                if network.alert_peoples is None:
                    continue
                elif args.get("people_id") in network.alert_peoples:
                    id_list = network.alert_peoples.split(",")
                    id_list.remove(args.get("people_id"))
                    network.alert_peoples = ','.join(id_list)
            elif network.id in args.get("networks"):
                if network.alert_peoples is None:
                    network.alert_peoples = args.get("people_id")
                else:
                    if args.get("people_id") not in network.alert_peoples:
                        network.alert_peoples = network.alert_peoples + "," + args.get("people_id")
            con.merge(network)
            con.commit()
    elif not args.get("networks"):
        networks = con.query(NetWorks).all()
        for network in networks:
            if network.alert_peoples is None:
                continue
            elif args.get("people_id") in network.alert_peoples:
                id_list = network.alert_peoples.split(",")
                id_list.remove(args.get("people_id"))
                network.alert_peoples = ','.join(id_list)
            con.merge(network)
            con.commit()
    if args.get("externals"):
        externals = con.query(ExternalResources).all()
        for external in externals:
            if external.id not in args.get("externals"):
                if external.alert_peoples is None:
                    continue
                elif args.get("people_id") in external.alert_peoples:
                    id_list = external.alert_peoples.split(",")
                    id_list.remove(args.get("people_id"))
                    external.alert_peoples = ','.join(id_list)
            elif external.id in args.get("externals"):
                if external.alert_peoples is None:
                    external.alert_peoples = args.get("people_id")
                else:
                    if args.get("people_id") not in external.alert_peoples:
                        external.alert_peoples = external.alert_peoples + "," + args.get("people_id")
            con.merge(external)
            con.commit()
    elif not args.get("externals"):
        externals = con.query(ExternalResources).all()
        for external in externals:
            if external.alert_peoples is None:
                continue
            elif args.get("people_id") in external.alert_peoples:
                id_list = external.alert_peoples.split(",")
                id_list.remove(args.get("people_id"))
                external.alert_peoples = ','.join(id_list)
            con.merge(external)
            con.commit()
    resp = make_response({'msg': '用户选择资源成功', 'value': []}, 200)
    con.close()
    return resp
