import threading
import logging
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from app.api.account_api import Account
from app.api.alert_log_api import AlertLogs
from app.api.disks_api import Disk
from app.api.external_related_api import RelatedObjects
from app.api.external_resource_api import ExternalResource
from app.api.networks_api import NetWork
from app.api.nodes_api import Nodes
from app.api.peoples_api import Peoples
from app.api.put_info_api import PutInfo
from pkg.Timertask.send_message import send_message
from pkg.Timertask.get_datas import timing
from pkg.util.setting import setting

app = Flask(__name__)


def init_logging():
    stream_handler = logging.StreamHandler(sys.stderr)  # 默认是sys.stderr
    stream_handler.setFormatter(
        logging.Formatter("[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s"))
    # 将处理器附加到根logger
    root_logger = logging.getLogger()
    root_logger.addHandler(setting.get_log_config())
    root_logger.addHandler(stream_handler)


api = Api(app)
CORS(app, pkg_resources=r'/*')
api.add_resource(Nodes, '/api/v1/vms', '/api/v1/vms/<id>')
api.add_resource(Disk, '/api/v1/disks', '/api/v1/disks/<id>')
api.add_resource(NetWork, '/api/v1/networks', '/api/v1/networks/<id>')
api.add_resource(ExternalResource, '/api/v1/external_resources', '/api/v1/external_resources/<id>')
api.add_resource(Peoples, '/api/v1/peoples', '/api/v1/peoples/<id>')
api.add_resource(AlertLogs, '/api/v1/logs', '/api/v1/logs/<id>')
api.add_resource(PutInfo, '/api/v1/put_info')
api.add_resource(Account, '/api/v1/account', '/api/v1/account/<id>')
api.add_resource(RelatedObjects, '/api/v1/related_objects')
time_msg = setting.get_timer_time()
time1 = time_msg['Timer1']
time2 = time_msg['Timer2']
# @app.errorhandler(404)
# def no_found(e):
#     return "404"


if __name__ == '__main__':
    with app.app_context():
        init_logging()
    app.debug = False
    t1 = threading.Thread(target=timing)
    t2 = threading.Thread(target=send_message)
    t1.start()
    t2.start()
    sched1 = BackgroundScheduler(timezone="Asia/Shanghai")
    sched2 = BackgroundScheduler(timezone="Asia/Shanghai")
    sched1.add_job(timing, 'interval', hours=int(time1))
    sched1.start()
    sched2.add_job(send_message, 'interval', hours=int(time2))
    sched2.start()
    app.run(host="0.0.0.0", port=8080)
