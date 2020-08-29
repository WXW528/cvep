#
from apps.wxs.wxs_app import WxsApp
from apps.dcl.dcl_app import DclApp
from apps.siamese.siamese_app import SiameseApp

MODE_WXS_APP = 101 # 无锡所数据处理
MODE_DCL_APP = 102 # DCL应用
MODE_SIAMESE_APP = 103 # Siamese网络计算图片相似度

def run_wxs_app(args={}):
    app = WxsApp()
    app.startup(args)

def run_dcl_app(args={}):
    app = DclApp()
    app.startup(args)

def run_siamese_app(args={}):
    app = SiameseApp()
    app.startup(args)

def main(args={}):
    mode = MODE_WXS_APP
    if MODE_WXS_APP == mode:
        run_wxs_app(args)
    elif MODE_DCL_APP == mode:
        run_dcl_app(args)
    elif MODE_SIAMESE_APP == mode:
        run_siamese_app(args)

if '__main__' == __name__:
    args = {}
    main(args)