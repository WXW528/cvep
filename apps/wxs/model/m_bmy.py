from os import stat
import pymongo
from apps.wxs.model.m_mongodb import MMongoDb

class MBmy(object):
    def __init__(self):
        self.name = 'apps.wxs.model.MBmy'

    @staticmethod
    def get_bmy_id_bmy_codes():
        '''
        获取bmy_code对应bmy_id的对应关系
        '''
        query_cond = {}
        fields = {'bmy_id': 1, 'bmy_code': 1}
        return MMongoDb.convert_recs(MMongoDb.db['t_bmy']\
                    .find(query_cond, fields))