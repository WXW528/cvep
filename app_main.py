#
from apps.wxs.wxs_app import WxsApp

def main(args={}):
    app = WxsApp()
    params = {}
    app.startup(params)

if '__main__' == __name__:
    args = {}
    main(args)