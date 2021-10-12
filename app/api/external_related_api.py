from flask_restful import Resource
from app.domain.external_related_domain import external_choose
from pkg.request_parsers import MyRequestParser

parser = MyRequestParser(bundle_errors=True)


class RelatedObjects(Resource):
    def post(self):
        parser_copy = parser.copy()
        parser_copy.add_argument('id', type=str, location=['json'], help="外置资源id不能为空")
        parser_copy.add_argument('nodes', type=str, location=['json'], action="append", help="资源id不能为空")
        parser_copy.add_argument('disks', type=str, location=['json'], action="append", help="资源id不能为空")
        parser_copy.add_argument('networks', type=str, location=['json'], action="append", help="资源id不能为空")
        parser_copy.add_argument('externals', type=str, location=['json'], action="append", help="资源id不能为空")
        args = parser_copy.parse_args()
        result = external_choose(args)
        return result
