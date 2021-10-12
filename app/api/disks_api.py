from flask import request
from flask_restful import Resource
from app.domain.disks_domain import get_disks, get_disk_detail, put_disks, post_disks
from pkg.request_parsers import MyRequestParser

parser = MyRequestParser(bundle_errors=True)


class Disk(Resource):
    def get(self, id=None):
        if not request.values.to_dict() and not id:
            result_vm = get_disks()
            return result_vm
        elif id:
            result = get_disk_detail(id)
            return result
        else:
            result = get_disks(request.values.to_dict(), request.values.to_dict().get('pageNum', 1),
                               request.values.to_dict().get('pageSize', 10))
            return result

    def put(self, id):
        parser_copy = parser.copy()
        parser_copy.add_argument('alert_level', type=str, location=['json'])
        parser_copy.add_argument('alert_disable', type=bool, location=['json'])
        parser_copy.add_argument('alert_peoples', type=str, location=['json'], action="append")
        parser_copy.add_argument('sms_status', type=bool, location=['json'])
        args = parser_copy.parse_args()
        result = put_disks(args, id)
        return result

    def post(self):
        parser_copy = parser.copy()
        parser_copy.add_argument('id', type=str, location=['json'], required=True, help="磁盘id不能为空")
        parser_copy.add_argument('key', type=str, location=['json'])
        args = parser_copy.parse_args()
        result = post_disks(args)
        return result
