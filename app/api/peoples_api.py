from flask import request
from flask_restful import Resource, inputs
from app.domain.peoples_domain import del_peoples, put_peoples, post_people, get_peoples, get_people_details
from pkg.request_parsers import MyRequestParser

parser = MyRequestParser(bundle_errors=True)


class Peoples(Resource):
    def get(self, id=None):
        if not request.values.to_dict() and not id:
            result_vm = get_peoples()
            return result_vm
        elif id:
            result = get_people_details(id)
            return result
        else:
            result = get_peoples(request.values.to_dict(), request.values.to_dict().get('pageNum', 1),
                                 request.values.to_dict().get('pageSize', 10))
            return result

    def post(self):
        parser_copy = parser.copy()
        parser_copy.add_argument('name', type=str, location=['json'], required=True, help="请输入用户名")
        parser_copy.add_argument('mail',
                                 type=inputs.regex(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$'),
                                 location=['json'], required=True, help="请输入正确的邮箱地址")
        parser_copy.add_argument('phone', type=inputs.regex(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d|19\d)\d{8}$'),
                                 location=['json'], required=True, help="请输入正确的手机号码格式")
        parser_copy.add_argument('im_ding', type=str, location=['json'])
        parser_copy.add_argument('im_wechat', type=str, location=['json'])
        args = parser_copy.parse_args()
        result = post_people(args)
        return result

    def put(self, id):
        parser_copy = parser.copy()
        parser_copy.add_argument('name', type=str, location=['json'])
        parser_copy.add_argument('mail',
                                 type=inputs.regex(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$'),
                                 location=['json'], help="请输入正确的邮箱地址")
        parser_copy.add_argument('phone', type=inputs.regex(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d|19\d)\d{8}$'),
                                 location=['json'], help="请输入正确的手机号码格式")
        parser_copy.add_argument('im_ding', type=str, location=['json'])
        parser_copy.add_argument('im_wechat', type=str, location=['json'])
        parser_copy.add_argument('nodes', type=str, location=['json'], action="append")
        parser_copy.add_argument('disks', type=str, location=['json'], action="append")
        parser_copy.add_argument('networks', type=str, location=['json'], action="append")
        parser_copy.add_argument('externals', type=str, location=['json'], action="append")
        args = parser_copy.parse_args()
        result = put_peoples(args, id)
        return result

    def delete(self, id):
        result = del_peoples(id)
        return result
