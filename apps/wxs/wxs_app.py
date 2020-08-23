#
from apps.wxs.wxs_dsm import WxsDsm

class WxsApp(object):
    def __init__(self):
        self.refl = 'apps.wxs.WxsApp'

    def startup(self, args={}):
        print('无锡所应用...')
        run_mode = 1
        if 1 == run_mode:
            WxsDsm.generate_txt_by_wxs_tds_ok_images()