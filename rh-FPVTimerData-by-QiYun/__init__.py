'''Plugin'''

import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy import inspect

from RHUI import UIField, UIFieldType
import requests
import Database

def initialize(rhapi):

    rhapi.ui.register_panel("qiyun_format", "骑云-数据上传", "format")
    rhapi.fields.register_option( UIField("data_uuid", "秘钥", UIFieldType.TEXT), "qiyun_format")
    rhapi.ui.register_quickbutton("qiyun_format", "upload_data", "同步数据", runUploadBtn, {"rhapi": rhapi})

def runUploadBtn(args):
    args['rhapi'].ui.message_notify(args['rhapi'].__('开始上传数据.'))

    keys = Database.GlobalSettings.query.filter_by(option_name='data_uuid').first().option_value

    SavedRaceLap = Database.SavedRaceLap.query.all()
    SavedRaceMeta = Database.SavedRaceMeta.query.all()
    RaceClass = Database.RaceClass.query.all()
    Heat = Database.Heat.query.all()
    HeatNode = Database.HeatNode.query.all()
    Pilot = Database.Pilot.query.all()
    RaceFormat = Database.RaceFormat.query.all()

    datas = {
        'key': keys,
        'Pilot': Pilot,
        'Heat': Heat,
        'HeatNode': HeatNode,
        'RaceClass': RaceClass,
        'SavedRaceMeta': SavedRaceMeta,
        'SavedRaceLap': SavedRaceLap,
        'RaceFormat': RaceFormat,
    }

    res = requests.post('https://fpvtimer.cn/laptimer/dataupload', json=json.loads(json.dumps(datas, cls=AlchemyEncoder)))
    args['rhapi'].ui.message_notify(args['rhapi'].__(res.json()['message']))

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        custom_vars = []
        if isinstance(obj.__class__, DeclarativeMeta):
            mapped_instance = inspect(obj)
            fields = {}
            for field in dir(obj):
                if field in [*mapped_instance.attrs.keys(), *custom_vars]:
                    data = obj.__getattribute__(field)
                    if field != 'query' \
                        and field != 'query_class':
                        try:
                            json.dumps(data)
                            fields[field] = data
                        except TypeError:
                            fields[field] = None
            return fields

        return json.JSONEncoder.default(self, obj)
