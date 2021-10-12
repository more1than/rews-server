import json

from app.models.disk import Disks
from app.models.external_resource import ExternalResources
from flask import make_response

from app.models.network import NetWorks
from app.models.nodes import Nodes
from pkg.create_con import create_con


def external_choose(args):
    con = create_con()
    external = con.query(ExternalResources).filter_by(id=args.get("id")).first()
    external_list = []
    if not external:
        resp = make_response({'msg': '外置资源关联资源失败', 'value': [], 'errors': [{
            "code": "400",
            "desc": "请输入正确的id",
            "field": "id"
        }]}, 400)
        return resp
    if args.get("nodes"):
        for node_id in args.get("nodes"):
            data = {"type": "nodes", "id": node_id}
            if external_list:
                external_list.append(data)
            else:
                external_list = [data]
    elif not args.get("nodes"):
        for id_dict in external_list:
            node_info = con.query(Nodes).filter_by(id=id_dict.get("id")).first()
            if node_info is not None and external_list:
                external_list.remove(id_dict)
    if args.get("disks"):
        for disk_id in args.get("disks"):
            data = {"type": "disks", "id": disk_id}
            if external_list:
                external_list.append(data)
            else:
                external_list = [data]
    elif not args.get("disks"):
        for id_dict in external_list:
            disk_info = con.query(Disks).filter_by(id=id_dict.get("id")).first()
            if disk_info is not None and external_list:
                external_list.remove(id_dict)
    if args.get("networks"):
        for network_id in args.get("networks"):
            data = {"type": "networks", "id": network_id}
            if external_list:
                external_list.append(data)
            else:
                external_list = [data]
    elif not args.get("networks"):
        for id_dict in external_list:
            network_info = con.query(NetWorks).filter_by(id=id_dict.get("id")).first()
            if network_info is not None and external_list:
                external_list.remove(id_dict)
    if args.get("externals"):
        for external_id in args.get("externals"):
            data = {"type": "externals", "id": external_id}
            if external_id == external.id:
                resp = make_response({'msg': '外置资源关联资源失败', 'value': [], 'errors': [{
                    "code": "400",
                    "desc": "外置资源不可以关联自身",
                    "field": "id"
                }]}, 400)
                return resp
            if external_list:
                external_list.append(data)
            else:
                external_list = [data]
    elif not args.get("externals"):
        for id_dict in external_list:
            external_info = con.query(ExternalResources).filter_by(id=id_dict.get("id")).first()
            if external_info is not None and external_list:
                external_list.remove(id_dict)
    external.related_objects = json.dumps(str(external_list))
    con.merge(external)
    con.commit()
    resp = make_response({"msg": "外置资源关联资源成功", "value": external.to_dict()}, 200)
    con.close()
    return resp
