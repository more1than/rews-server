from flask_restful import Resource
from app.domain.alert_log_domain import get_alert_logs, get_alert_logs_detail
from flask import request
from pkg.request_parsers import MyRequestParser

parser = MyRequestParser(bundle_errors=True)


class AlertLogs(Resource):
    def get(self, id=None):
        if not request.values.to_dict() and not id:
            result_vm = get_alert_logs()
            return result_vm
        elif id:
            result = get_alert_logs_detail(id)
            return result
        else:
            result = get_alert_logs(request.values.to_dict(), request.values.to_dict().get('pageNum', 1),
                                    request.values.to_dict().get('pageSize', 10))
            return result
