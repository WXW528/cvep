#
from apps.wxs.model.m_mongodb import MMongoDb
from apps.wxs.wxs_app import WxsApp

def main(args={}):
    MMongoDb._initialize()
    app = WxsApp()
    params = {}
    app.startup(params)

if '__main__' == __name__:
    args = {}
    main(args)