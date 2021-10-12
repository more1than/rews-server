from flask import request
from flask_restful import Resource
from app.domain.account_domain import get_accounts, get_account_detail, put_account, post_account, del_account
from pkg.request_parsers import MyRequestParser

parser = MyRequestParser(bundle_errors=True)


class Account(Resource):
    def get(self, id=None):
        if not request.values.to_dict() and not id:
            result = get_accounts()
            return result
        elif id:
            result = get_account_detail(id)
            return result
        else:
            result = get_accounts(request.values.to_dict(), request.values.to_dict().get('pageNum', 1),
                                  request.values.to_dict().get('pageSize', 10))
            return result

    def put(self, id):
        parser_copy = parser.copy()
        parser_copy.add_argument('cloud_type', type=str, location=['json'])
        parser_copy.add_argument('name', type=str, location=['json'], required=True, help="账号名称不能为空")
        parser_copy.add_argument('api_key', type=str, location=['json'])
        parser_copy.add_argument('api_sec', type=str, location=['json'])
        args = parser_copy.parse_args()
        result = put_account(args, id)
        return result

    def post(self):
        parser_copy = parser.copy()
        parser_copy.add_argument('cloud_type', type=str, location=['json'])
        parser_copy.add_argument('name', type=str, location=['json'], required=True, help="账号名称不能为空")
        parser_copy.add_argument('api_key', type=str, location=['json'])
        parser_copy.add_argument('api_sec', type=str, location=['json'])
        args = parser_copy.parse_args()
        result = post_account(args)
        return result

    def delete(self, id):
        result = del_account(id)
        return result
