from app.models.disk import Disks
from app.models.external_resource import ExternalResources
from app.models.network import NetWorks
from app.models.nodes import Nodes
from pkg.create_con import create_con


def put_people_ids(id):
    con = create_con()
    nodes = con.query(Nodes).all()
    for node in nodes:
        if node.alert_peoples and id in node.alert_peoples.split(','):
            node.alert_peoples.split(',').remove(id)
            setattr(node, 'alert_peoples', ','.join(node.alert_peoples.split(',')))
    disks = con.query(Disks).all()
    for disk in disks:
        if disk.alert_peoples and id in disk.alert_peoples.split(','):
            disk.alert_peoples.split(',').remove(id)
            setattr(disk, 'alert_peoples', ','.join(disk.alert_peoples.split(',')))
    nets = con.query(NetWorks).all()
    for net in nets:
        if net.alert_peoples and id in net.alert_peoples.split(','):
            net.alert_peoples.split(',').remove(id)
            setattr(net, 'alert_peoples', ','.join(net.alert_peoples.split(',')))
    externals = con.query(ExternalResources).all()
    for external in externals:
        if external.alert_peoples and id in external.alert_peoples.split(','):
            external.alert_peoples.split(',').remove(id)
            setattr(external, 'alert_peoples', ','.join(external.alert_peoples.split(',')))
    con.commit()
    con.close()
