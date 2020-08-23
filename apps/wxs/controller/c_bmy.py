#
from apps.wxs.model.m_bmy import MBmy

class CBmy(object):
    def __init__(self):
        self.refl = 'apps.wxs.controller.CBmy'

    @staticmethod
    def get_bmy_code_bmy_id_dict():
        bmy_code_bmy_id_dict = {}
        recs = MBmy.get_bmy_id_bmy_codes()
        for rec in recs:
            bmy_code_bmy_id_dict[rec['bmy_code']] = int(rec['bmy_id'])
        return bmy_code_bmy_id_dict