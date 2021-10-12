import hashlib
import json
import os
import time
from datetime import datetime
import uuid
from hashlib import sha256
import requests
from app.models.alert_logs import AlertLogs
from app.models.disk import Disks
from app.models.external_resource import ExternalResources
from app.models.network import *
from app.models.nodes import Nodes
from app.models.peoples import *
from pkg.create_con import create_con
from pkg.sms_send import send
import threading

# a = "{\"id\": \"8556c9f6-1ae4-4638-b4fd-90f41891de58\", \"osType\": \"Linux\", \"platform\": \"Ubuntu\", \"name\":
# \"ubuntu18.05.05_\测\试\镜\像\", \"osBit\": 64, \"crateDate\": \"2021-07-28 08:07:39\", \"status\": \"active\",
# \"osVersion\": \"Ubuntu 16.04 server 64bit\", \"minRam\": 0, \"minDisk\": 40, \"imageType\": \"private\",
# \"virtual\": \"\是\"}"
# b = json.loads(a)
# print(b)
from pkg.util.setting import setting


# [{'type': 'nodes', 'id': '014e1cd8-da6e-464e-ad82-1627f1e0b965'}]
# b = "[{'type': 'nodes', 'id': '014e1cd8-da6e-464e-ad82-1627f1e0b965'}, " \
#     "{'type': 'nodes', 'id': '03caad4a-fef6-4460-9dc1-dd35605bb424'}]"
# c = eval(b)
# print(c)
# print(type(c))

