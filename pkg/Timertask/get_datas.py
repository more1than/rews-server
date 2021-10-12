import datetime
import json
import logging
import threading
import time

from app.models.account import Account
from app.models.external_resource import ExternalResources
from app.models.nodes import Nodes
from app.models.disk import Disks
from app.models.network import NetWorks
from pkg.cloud_provider import Provider
from pkg.create_con import create_con
from dateutil.parser import parse
from pkg.is_change import is_change

vo_type = {"SATA": "普通IO", "SAS": "高IO", "SSD": "超高IO", "co-pl": "高IO (性能优化Ⅰ型)", "uh-l1": "超高 IO (时延优化)"}
vmids = []
voids = []
network_ids = []
count = 0


def get_nodes(provider):
    type = provider.type
    global vmids
    vmids = []
    ip_address_lan, ip_address_wan = '', ''
    node = provider.get_cloud_provider().get_node()
    con = create_con()
    result = node.query_vms()
    if result['statusCode'] != 800:
        return
    servers = result.get('returnObj').get('servers')
    if not servers:
        return
    for i in servers:
        vmid = i['id']
        vmids.append(vmid)
        vm = con.query(Nodes).filter_by(id=vmid).first()
        if not vm:
            vm = Nodes(id=i['id'], cloud_type=type, instance_type=i.get('flavor').get("original_name"),
                       hostname=i.get('name'), account_name=provider.name)
            con.add(vm)
            con.commit()
        result = node.query_vm_detail(vmid)
        if result['statusCode'] != 800:
            continue
        returnObjs = result.get('returnObj')
        os = {"id": "",
              "osType": "",
              "platform": "",
              "name": "",
              "osBit": "",
              "crateDate": "",
              "status": "",
              "osVersion": "",
              "minRam": "",
              "minDisk": "",
              "imageType": "private",
              "virtual": '否'}
        if returnObjs:
            vmStatus = returnObjs.get('vmStatus')
            if vmStatus != vm.status:
                vm.status = vmStatus
            image_id = i.get('image').get('id')
            image = provider.get_cloud_provider().get_image()
            res_images = image.query_images().get('returnObj')
            os['osType'] = returnObjs.get('osStyle')
            for res_image in res_images:
                if image_id == res_image.get('id'):
                    os = res_image
                    res = time.strptime(res_image.get('crateDate'), "%Y-%m-%dT%H:%M:%SZ")
                    os['crateDate'] = time.strftime("%Y-%m-%d %H:%M:%S", res)
                    if os['virtual'] == True:
                        os['virtual'] = '是'
                    else:
                        os['virtual'] = '否'
        cpu = returnObjs.get('cpuNum')
        mem = returnObjs.get('memSize')
        if cpu and mem:
            vm.status = 'RUNNING'
        for x in i.get('addresses').values():
            for j in x:
                if j.get('OS-EXT-IPS:type') == "fixed" and j.get('OS-EXT-IPS:type') != vm.ipaddress_lan:
                    vm.ipaddress_lan = j.get('addr')
                    ip_address_lan = j.get('addr')
                if j.get('OS-EXT-IPS:type') == "floating" and j.get('OS-EXT-IPS:type') != vm.ipaddress_wan:
                    vm.ipaddress_wan = j.get('addr')
                    ip_address_wan = j.get('addr')
        if i.get('expireTime'):
            expire_at = int(parse(i.get('expireTime')).timestamp())
        else:
            expire_at = 0
        if i.get('created'):
            buy_at = int(parse(i.get('created')).timestamp())
        else:
            buy_at = None
        expire_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(expire_at))
        buy_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(buy_at))
        network_id = None
        net_work = con.query(NetWorks).all()
        for a in net_work:
            if not vm.ipaddress_wan:
                break
            elif vm.ipaddress_wan in a.ips:
                vm.network_id = a.id
                network_id = a.id
        bool, hash_before = is_change(vm.body_hash,
                                      str(i['flavor']['original_name']), str(i['name']), str(cpu), str(mem), str(os),
                                      str(i['status']), str(ip_address_lan), str(ip_address_wan), str(buy_time),
                                      str(expire_time), str(network_id), vm.account_name)
        if bool is False:
            continue
        vm.body_hash = hash_before
        if expire_time != vm.expire_at:
            vm.expire_at = expire_time
        if buy_time != vm.buy_at:
            vm.buy_at = buy_time
        if vm.account_name != provider.name:
            vm.account_name = provider.name
        flavor = vm.instance_type
        if not cpu or not mem:
            vm.instance_type = flavor
        else:
            flavor = flavor.split("|")[0]
            vm.instance_type = "%s | %svCPUs | %sGB " % (flavor, cpu, mem)
            vm.cpu = cpu
            vm.mem_size = mem
        if vm.os != os:
            vm.os = json.dumps(os)
        workOrderResourceId = returnObjs.get('workOrderResourceId'),
        userId = returnObjs.get('userId'),
        accountId = returnObjs.get('accountId'),
        orderId = returnObjs.get('orderId'),
        vlanId = returnObjs.get('vlanId'),
        zoneId = returnObjs.get('zoneId'),
        if not workOrderResourceId[0]:
            workOrderResourceId = ""
        if not userId[0]:
            userId = ""
        if not accountId[0]:
            accountId = ""
        if not orderId[0]:
            orderId = ""
        if not vlanId[0]:
            vlanId = ""
        if not zoneId[0]:
            zoneId = ""
        platform = json.dumps({
            "workOrderResourceId": workOrderResourceId,
            "userId": userId,
            "accountId": accountId,
            "orderId": orderId,
            "vlanId": vlanId,
            "zoneId": zoneId,
        })
        vm.platform = platform
        con.merge(vm)
        con.commit()
    con.close()


def delete_nodes():
    con = create_con()
    nodes = con.query(Nodes).all()
    for no in nodes:
        if no.id not in vmids:
            con.delete(no)
            con.commit()
    con.close()


def get_disks(provider):
    type = provider.type
    con = create_con()
    disk = provider.get_cloud_provider().get_disk()
    volumeIds = []
    global voids
    voids = []
    result = disk.query_volumes()
    if result['statusCode'] != 800:
        return
    returnObj = result.get('returnObj')
    if not returnObj:
        return
    volumes = returnObj.get('volumes')
    if not volumes:
        return
    for i in volumes:
        volumeId = i['id']
        voids.append(volumeId)
        volumeIds.append(volumeId)
        vo = con.query(Disks).filter_by(id=volumeId).first()
        node = provider.get_cloud_provider().get_node()
        user_id = i.get("user_id"),
        availability_zone = i.get("availability_zone")
        attached_at = i.get("attached_at")
        shareable = i.get("shareable")
        device = i.get("device")
        if not user_id:
            user_id = ""
        if not availability_zone:
            availability_zone = ""
        if not attached_at:
            attached_at = ""
        if not shareable:
            shareable = ""
        if not device:
            device = ""
        platform = json.dumps({
            "user_id": user_id,
            "availability_zone": availability_zone,
            "attached_at": attached_at,
            "shareable": shareable,
            "device": device,
        })
        if not vo:
            vo = Disks(id=volumeId,
                       cloud_type=type,
                       size=int(i.get('size')),
                       disk_type=i.get("volume_type"),
                       platform=platform,
                       account_name=provider.name,
                       )
        if vo.size != i.get('size'):
            vo.size = i.get('size')
        if i.get('masterOrderId') is not None:
            vo_list = disk.query_resource(i.get('masterOrderId')).get('returnObj')
            if len(vo_list) == 0:
                vo.status = i.get('status')
            else:
                for j in vo_list:
                    if vo.status != j.get('status'):
                        if j.get('status') == 6 or j.get('status') == 7 or j.get('status') == 5:
                            vo.status = 'expired'
                        else:
                            vo.status = i.get('status')
        else:
            vo.status = i.get('status')
        if not i.get('expireTime'):
            expire_at = 0
        else:
            expire_at = int(int(i.get('expireTime')) / 1000)
        buy_at = int(int(i.get('created_at')) / 1000)
        expire_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(expire_at))
        buy_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(buy_at))
        bool, hash_before = is_change(vo.body_hash, str(i['volume_type']), str(i['size']), str(buy_time),
                                      str(expire_time), str(i.get('status')), vo.account_name)
        if not bool:
            continue
        vo.body_hash = hash_before
        if vo.buy_at != buy_time:
            vo.buy_at = buy_time
        if vo.expire_at != expire_time:
            vo.expire_at = expire_time
        if vo.account_name != provider.name:
            vo.account_name = provider.name
        if len(i.get('attachments')) == 0:
            node_name = None
            node_id = None
        else:
            result = node.query_vm(i.get('attachments')[0].get('server_id'))
            node_name = result.get("returnObj").get("name")
            node_id = i.get('attachments')[0].get('server_id')
        vo.node_id = node_id
        vo.node_name = node_name
        volume_type = vo_type[i.get("volume_type")]
        flavor = "%s | %sGB" % (volume_type, i.get('size'))
        if flavor != vo.instance_type:
            vo.instance_type = flavor
        con.merge(vo)
        con.commit()
    con.close()


def delete_disks():
    con = create_con()
    disks = con.query(Disks).all()
    for disk in disks:
        if disk.id not in voids:
            con.delete(disk)
            con.commit()
    con.close()


def get_net_works(provider):
    type = provider.type
    con = create_con()
    net_work = provider.get_cloud_provider().get_net()
    global network_ids
    network_ids = []
    result = net_work.query_networks()
    if result['statusCode'] != 800:
        return
    page = result.get('returnObj').get("pageCount")
    for page_num in range(page):
        network_info = net_work.query_networks_page(page_num)
        network_infos = network_info.get('returnObj').get('result')
        if not network_infos:
            return
        for network in network_infos:
            network_id = network.get('resBandwidthId')
            network_ids.append(network_id)
            nt = con.query(NetWorks).filter_by(id=network_id).first()
            name = network.get("name")
            accountId = network.get("accountId")
            userId = network.get("userId")
            workOrderResourceId = network.get("workOrderResourceId")
            avaliableZoneId = network.get("avaliableZoneId")
            masterOrderId = network.get("masterOrderId")
            if not name[0] or not accountId[0] or not userId[0] or not workOrderResourceId[0] or not avaliableZoneId[
                0] or not masterOrderId[0]:
                name = ""
                accountId = ""
                userId = ""
                workOrderResourceId = ""
                avaliableZoneId = ""
                masterOrderId = ""
            platform = json.dumps({
                "name": name,
                "accountId": accountId,
                "userId": userId,
                "workOrderResourceId": workOrderResourceId,
                "avaliableZoneId": avaliableZoneId,
                "masterOrderId": masterOrderId,
            })
            if not nt:
                nt = NetWorks(
                    id=network.get('resBandwidthId'),
                    size=network.get('speed'),
                    network_type=network.get("bandwidthType"),
                    cloud_type=type,
                    platform=platform,
                    account_name=provider.name
                )
                con.add(nt)
                con.commit()
            expire_at = int(int(network.get('expireTime')) / 1000)
            buy_at = int(int(network.get('createTime')) / 1000)
            expire_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(expire_at))
            buy_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(buy_at))
            network_ips = []
            result = net_work.query_ips()
            if result.get('statusCode') != 800:
                continue
            ips = result.get('returnObj').get('publicips')
            count = 0
            for ip in ips:
                if ip.get('bandwidth_id') == network.get('resBandwidthId'):
                    network_ips.append(ip.get('public_ip_address'))
                if ip.get('bandwidth_share_type') == 'WHOLE' and ip.get('status') == 'DOWN' and ip.get(
                        'bandwidth_id') == network.get('resBandwidthId'):
                    count += 1
            network_ips = ','.join(network_ips)
            network_valid_ips = count
            bool, hash_before = is_change(nt.body_hash, network['bandwidthType'], network['speed'], network_valid_ips,
                                          buy_time, network_ips, platform, expire_time, nt.account_name)
            if not bool:
                continue
            nt.body_hash = hash_before
            if nt.platform != platform:
                nt.platform = platform
            if nt.ips != network_ips:
                nt.ips = network_ips
            if nt.status != network.get('status'):
                nt.status = network.get('status')
            if nt.instance_type != network.get("bandwidthType"):
                nt.instance_type = network.get("bandwidthType")
            if nt.buy_at != buy_time:
                nt.buy_at = buy_time
            if nt.expire_at != expire_time:
                nt.expire_at = expire_time
            if network_valid_ips != nt.valid_ips:
                nt.valid_ips = network_valid_ips
            if nt.account_name != provider.name:
                nt.account_name = provider.name
            if network.get("bandwidthType") == "WHOLE":
                volume_type = "共享"
            else:
                volume_type = "独享"
            flavor = "%s | %sMbit/s" % (volume_type, network.get('speed'))
            if flavor != nt.instance_type:
                nt.instance_type = flavor
            con.merge(nt)
            con.commit()
    con.close()


def delete_networks():
    con = create_con()
    networks = con.query(NetWorks).all()
    for net in networks:
        if net.id not in network_ids:
            con.delete(net)
            con.commit()
    con.close()


def put_nodes():
    con = create_con()
    nodes = con.query(Nodes).all()
    for i in nodes:
        if i.expire_at < datetime.datetime.now():
            i.status = 'Expired'
        con.merge(i)
    con.commit()
    con.close()


def put_disks():
    con = create_con()
    disks = con.query(Disks).all()
    for i in disks:
        if i.expire_at < datetime.datetime.now():
            i.status = 'expired'
        con.merge(i)
    con.commit()
    con.close()


def put_networks():
    con = create_con()
    nets = con.query(NetWorks).all()
    for i in nets:
        if i.expire_at < datetime.datetime.now():
            i.status = '6'
        con.merge(i)
    con.commit()
    con.close()


def put_external_resources():
    con = create_con()
    externals = con.query(ExternalResources).all()
    for i in externals:
        if i.expire_at < datetime.datetime.now():
            i.status = '过期'
        con.merge(i)
    con.commit()
    con.close()


def timing():
    con = create_con()
    accounts = con.query(Account).all()
    for account in accounts:
        t = threading.Thread(target=update_database, args=[account])
        t.start()


def update_database(account):
    try:
        provider = Provider(account.cloud_type, account.name, account.api_key, account.api_sec)
        print('net_works start')
        get_net_works(provider)
        print('net_works end')
        delete_networks()
        put_networks()
        print('nodes start')
        get_nodes(provider)
        print('nodes end')
        delete_nodes()
        put_nodes()
        print('disks start')
        get_disks(provider)
        print('disks end')
        delete_disks()
        put_disks()
        put_external_resources()
    except Exception as e:
        logging.error(e)
