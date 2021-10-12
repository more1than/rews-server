from flask import request
from flask_restful import Resource
from app.domain.external_resource_domain import put_external_resource, del_external_resource, get_external_resource, \
    get_external_resource_detail, post_external_resource
from pkg.request_parsers import MyRequestParser

parser = MyRequestParser(bundle_errors=True)


class ExternalResource(Resource):
    def get(self, id=None):
        if not request.values.to_dict() and not id:
            result_vm = get_external_resource()
            return result_vm
        elif id:
            result = get_external_resource_detail(id)
            return result
        else:
            result = get_external_resource(request.values.to_dict(), request.values.to_dict().get('pageNum', 1),
                                           request.values.to_dict().get('pageSize', 10))
            return result

    def post(self):
        parser_copy = parser.copy()
        parser_copy.add_argument('name', type=str, location=['json'], required=True, help="资源名称不能为空")
        parser_copy.add_argument('instance_type', type=str, location=['json'], required=True, help="资源类型不能为空")
        parser_copy.add_argument('desc', type=str, location=['json'])
        parser_copy.add_argument('buy_at', type=str, location=['json'], required=True, help="购买时间不能为空")
        parser_copy.add_argument('expire_at', type=str, location=['json'], required=True, help="到期时间不能为空")
        args = parser_copy.parse_args()
        result = post_external_resource(args)
        return result

    def put(self, id):
        parser_copy = parser.copy()
        parser_copy.add_argument('name', type=str, location=['json'])
        parser_copy.add_argument('instance_type', type=str, location=['json'])
        parser_copy.add_argument('desc', type=str, location=['json'])
        parser_copy.add_argument('buy_at', type=str, location=['json'])
        parser_copy.add_argument('expire_at', type=str, location=['json'])
        parser_copy.add_argument('alert_level', type=str, location=['json'])
        parser_copy.add_argument('alert_disable', type=bool, location=['json'])
        parser_copy.add_argument('alert_peoples', type=str, location=['json'], action="append")
        parser_copy.add_argument('sms_status', type=bool, location=['json'])
        args = parser_copy.parse_args()
        result = put_external_resource(args, id)
        return result

    def delete(self, id):
        result = del_external_resource(id)
        return result
