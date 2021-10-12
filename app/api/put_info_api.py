from flask import request
from flask_restful import Resource

from app.domain.put_info_domain import put_all_info, get_all_resource, people_choose
from pkg.request_parsers import MyRequestParser

parser = MyRequestParser(bundle_errors=True)


class PutInfo(Resource):
    def get(self, id=None):
        if not request.values.to_dict() and not id:
            result_vm = get_all_resource(request.values.to_dict())
            return result_vm
        else:
            result = get_all_resource(request.values.to_dict())
            return result

    def put(self):
        parser_copy = parser.copy()
        parser_copy.add_argument('type', type=str, location=['json'], help="资源类型不能为空")
        parser_copy.add_argument('ids', type=str, location=['json'], action="append", help="id不能为空")
        parser_copy.add_argument('alert_level', type=str, location=['json'])
        parser_copy.add_argument('alert_disable', type=bool, location=['json'])
        parser_copy.add_argument('sms_status', type=bool, location=['json'])
        args = parser_copy.parse_args()
        result = put_all_info(args)
        return result

    def post(self):
        parser_copy = parser.copy()
        parser_copy.add_argument('people_id', type=str, location=['json'], help="人员id不能为空")
        parser_copy.add_argument('nodes', type=str, location=['json'], action="append", help="资源id不能为空")
        parser_copy.add_argument('disks', type=str, location=['json'], action="append", help="资源id不能为空")
        parser_copy.add_argument('networks', type=str, location=['json'], action="append", help="资源id不能为空")
        parser_copy.add_argument('externals', type=str, location=['json'], action="append", help="资源id不能为空")
        args = parser_copy.parse_args()
        result = people_choose(args)
        return result
