#
from apps.wxs.model.m_mongodb import MMongoDb
from apps.wxs.wxs_dsm import WxsDsm

class WxsApp(object):
    def __init__(self):
        self.refl = 'apps.wxs.WxsApp'

    def startup(self, args={}):
        print('无锡所应用...')
        MMongoDb._initialize()
        run_mode = 1
        if 1 == run_mode:
            #WxsDsm.generate_txt_by_wxs_tds_ok_images()
            WxsDsm.generate_ds_from_wxs_tds_ibc()
        elif 2 == run_mode:
            WxsDsm.generate_wxs_tds_for_integration_test()