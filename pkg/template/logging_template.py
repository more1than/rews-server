from app.models.alert_logs import AlertLogs
from pkg.create_con import create_con
from pkg.is_expire import is_expire


def logging_template(type, list, people_id=None, error=None):
    if type == "vm":
        for i in list:
            message = "'资源种类':%s-'资源名称':%s-'资源ID':%s-'资源规格':%s-'资源类型':%s还剩%s天时间" % (
                "云主机", i.hostname, i.id, i.instance_type, i.cloud_type,
                str((int(is_expire(str(i.expire_at)) / 24 / 60 / 60))))
            if error:
                message = "'资源种类':%s-'资源名称':%s-'资源ID':%s-'资源规格':%s-'资源类型':%s还剩%s天时间-'发送错误原因:%s" % (
                    "云主机", i.hostname, i.id, i.instance_type, i.cloud_type,
                    str((int(is_expire(str(i.expire_at)) / 24 / 60 / 60))), error)
            con = create_con()
            log = AlertLogs(message=message)
            con.add(log)
            log.node_id = i.id
            log.alert_level = i.alert_level
            if people_id:
                log.alert_peoples = people_id
            con.merge(log)
            con.commit()
            con.close()
    elif type == "disk":
        for i in list:
            message = "'资源种类':%s-'资源ID':%s-'资源规格':%s-'资源类型':%s还剩%s天时间" % (
                "云盘", i.id, i.instance_type, i.cloud_type, str((int(is_expire(str(i.expire_at)) / 24 / 60 / 60))))
            if error:
                message = "'资源种类':%s-'资源ID':%s-'资源规格':%s-'资源类型':%s还剩%s天时间-'发送错误原因:%s" % (
                    "云盘", i.id, i.instance_type, i.cloud_type,
                    str((int(is_expire(str(i.expire_at)) / 24 / 60 / 60))), error)
            con = create_con()
            log = AlertLogs(message=message)
            con.add(log)
            log.disk_id = i.id
            log.alert_level = i.alert_level
            if people_id:
                log.alert_peoples = people_id
            con.merge(log)
            con.commit()
            con.close()
    elif type == 'net':
        for i in list:
            message = "'资源种类':%s-'资源ID':%s-'资源规格':%s-'资源类型':%s还剩%s天时间" % (
                "带宽", i.id, i.instance_type, i.cloud_type, str((int(is_expire(str(i.expire_at)) / 24 / 60 / 60))))
            if error:
                message = "'资源种类':%s-'资源ID':%s-'资源规格':%s-'资源类型':%s还剩%s天时间-'发送错误原因:%s" % (
                    "带宽", i.id, i.instance_type, i.cloud_type,
                    str((int(is_expire(str(i.expire_at)) / 24 / 60 / 60))), error)
            con = create_con()
            log = AlertLogs(message=message)
            con.add(log)
            log.network_id = i.id
            log.alert_level = i.alert_level
            if people_id:
                log.alert_peoples = people_id
            con.merge(log)
            con.commit()
            con.close()
    elif type == 'ext':
        for i in list:
            message = "'资源种类':%s-'资源名称':%s-'资源ID':%s-'资源规格':%s-'资源类型':%s还剩%s天时间" % (
                "外置资源", i.name, i.id, i.instance_type, i.desc, str((int(is_expire(str(i.expire_at)) / 24 / 60 / 60))))
            if error:
                message = "'资源种类':%s-'资源名称':%s-'资源ID':%s-'资源规格':%s-'资源类型':%s还剩%s天时间-'发送错误原因:%s" % (
                    "外置资源", i.name, i.id, i.instance_type, i.desc,
                    str((int(is_expire(str(i.expire_at)) / 24 / 60 / 60))), error)
            con = create_con()
            log = AlertLogs(message=message)
            con.add(log)
            log.external_resource_id = i.id
            log.alert_level = i.alert_level
            if people_id:
                log.alert_peoples = people_id
            con.merge(log)
            con.commit()
            con.close()
