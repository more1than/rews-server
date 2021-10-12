import datetime
import logging
import time

from app.models.disk import Disks
from app.models.external_resource import ExternalResources
from app.models.network import NetWorks
from app.models.nodes import Nodes
from app.models.peoples import Peoples
from pkg.create_con import create_con
from pkg.is_expire import is_expire
from pkg.send_email import send_email
from pkg.sms_send import send
from pkg.template.logging_template import logging_template
from pkg.util.setting import setting

ten_days_time = 10 * 24 * 60 * 60
fifteen_days_time = 15 * 24 * 60 * 60
hour_times = 60 * 60
time_msg = setting.get_time_config()
start_time = time_msg.get("start_time")
end_time = time_msg.get("end_time")

create_people = []
people_list = []
gt_10_vm = []
gt_10_disk = []
gt_10_net = []
gt_10_ext = []
le_10_vm = []
le_10_disk = []
le_10_net = []
le_10_ext = []

is_send = False


class SendPPeople:
    def __init__(self, id, name, mail, phone):
        self.id = id
        self.name = name
        self.mail = mail
        self.phone = phone
        self.result_vm = []
        self.result_disk = []
        self.result_new_work = []
        self.result_external_resource = []
        self.has_send_gt_10_vm = []
        self.has_send_gt_10_disk = []
        self.has_send_gt_10_net = []
        self.has_send_gt_10_ext = []
        self.has_send_le_10_vm = []
        self.has_send_le_10_disk = []
        self.has_send_le_10_net = []
        self.has_send_le_10_ext = []
        self.has_sms = False

    def update_send_message(self):
        for node in gt_10_vm:
            if self.id in node.alert_peoples and node.id not in self.has_send_gt_10_vm:
                if node.sms_status == 0:
                    self.has_sms = True
                self.result_vm.append(node)
                self.has_send_gt_10_vm.append(node.id)
        for node in le_10_vm:
            if self.id in node.alert_peoples and node.id not in self.has_send_le_10_vm:
                if node.sms_status == 0:
                    self.has_sms = True
                self.result_vm.append(node)
                self.has_send_le_10_vm.append(node.id)
        for disk in gt_10_disk:
            if self.id in disk.alert_peoples and disk.id not in self.has_send_gt_10_disk:
                if disk.sms_status == 0:
                    self.has_sms = True
                self.result_disk.append(disk)
                self.has_send_gt_10_disk.append(disk.id)
        for disk in le_10_disk:
            if self.id in disk.alert_peoples and disk.id not in self.has_send_le_10_disk:
                if disk.sms_status == 0:
                    self.has_sms = True
                self.result_disk.append(disk)
                self.has_send_le_10_disk.append(disk.id)
        for net in gt_10_net:
            if self.id in net.alert_peoples and net.id not in self.has_send_gt_10_net:
                if net.sms_status == 0:
                    self.has_sms = True
                self.result_new_work.append(net)
                self.has_send_gt_10_net.append(net.id)
        for net in le_10_net:
            if self.id in net.alert_peoples and net.id not in self.has_send_le_10_net:
                if net.sms_status == 0:
                    self.has_sms = True
                self.result_new_work.append(net)
                self.has_send_le_10_net.append(net.id)
        for ext in gt_10_ext:
            if self.id in ext.alert_peoples and ext.id not in self.has_send_gt_10_ext:
                if ext.sms_status == 0:
                    self.has_sms = True
                self.result_external_resource.append(ext)
                self.has_send_gt_10_ext.append(ext.id)
        for ext in le_10_ext:
            if self.id in ext.alert_peoples and ext.id not in self.has_send_le_10_ext:
                if ext.sms_status == 0:
                    self.has_sms = True
                self.result_external_resource.append(ext)
                self.has_send_le_10_ext.append(ext.id)

    def pre_send_message(self):
        if not self.result_vm and not self.result_disk and not self.result_new_work and not self.result_external_resource:
            return
        send_email(self)
        if self.has_sms:
            send(self.phone)
        self.result_vm.clear()
        self.result_disk.clear()
        self.result_new_work.clear()
        self.result_external_resource.clear()
        self.has_sms = False


def update_resource():
    con = create_con()
    nodes = con.query(Nodes).all()
    for node in nodes:
        if not node.expire_at or node.status == "FREEZING" or node.alert_disable == 1:
            continue
        time1 = is_expire(node.to_dict().get('expire_at'))
        if time1:
            if fifteen_days_time > time1 >= ten_days_time:
                gt_10_vm.append(node)
            elif time1 < ten_days_time:
                le_10_vm.append(node)
    disks = con.query(Disks).all()
    for disk in disks:
        if not disk.expire_at or disk.alert_disable == 1:
            continue
        time1 = is_expire(disk.to_dict().get('expire_at'))
        if time1:
            if fifteen_days_time > time1 >= ten_days_time:
                gt_10_disk.append(disk)
            elif time1 < ten_days_time:
                le_10_disk.append(disk)
    nets = con.query(NetWorks).all()
    for net in nets:
        if not net.expire_at or net.alert_disable == 1:
            continue
        time1 = is_expire(net.to_dict().get('expire_at'))
        if time1:
            if fifteen_days_time > time1 >= ten_days_time:
                gt_10_net.append(net)
            elif time1 < ten_days_time:
                le_10_net.append(net)
    exts = con.query(ExternalResources).all()
    for ext in exts:
        if not ext.expire_at or ext.alert_disable == 1:
            continue
        time1 = is_expire(ext.to_dict().get('expire_at'))
        if time1:
            if fifteen_days_time > time1 >= ten_days_time:
                gt_10_ext.append(ext)
            elif time1 < ten_days_time:
                le_10_ext.append(ext)
    con.close()


def update_peoples():
    con = create_con()
    peoples = con.query(Peoples)
    for people in peoples:
        if people.id in create_people:
            continue
        sp = SendPPeople(people.id, people.name, people.mail, people.phone)
        people_list.append(sp)
        create_people.append(people.id)
    con.close()
    for sp in people_list:
        try:
            sp.update_send_message()
            sp.pre_send_message()
        except Exception as e:
            logging.error(e)
            continue


def save_logging():
    logging_template('vm', gt_10_vm)
    logging_template('vm', le_10_vm)
    logging_template('disk', gt_10_disk)
    logging_template('disk', le_10_disk)
    logging_template('net', gt_10_net)
    logging_template('net', le_10_net)
    logging_template('ext', gt_10_ext)
    logging_template('ext', le_10_ext)


def send_message():
    time.sleep(2 * 60)
    try:
        global is_send
        if start_time < datetime.datetime.now().strftime("%H:%M") < end_time:
            print('pre_send_message')
            update_resource()
            update_peoples()
            if is_send is False:
                save_logging()
                is_send = True
        else:
            people_list.clear()
            create_people.clear()
            is_send = False
    except Exception as e:
        logging.error(e)
