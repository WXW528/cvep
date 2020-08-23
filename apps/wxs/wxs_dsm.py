#
from pathlib import Path
from apps.wxs.controller.c_bmy import CBmy

class WxsDsm(object):
    def __init__(self):
        self.refl = 'apps.wxs.WxsDsm'

    
    @staticmethod
    def generate_ds_from_wxs_tds_ibc():
        '''
        从无锡所图片文件和对应的年款编中，求出对应的简化年款编号和品牌索引号
        '''
        bmy_code_bmy_id_dict = CBmy.get_bmy_code_bmy_id_dict()
        with open('./work/wt_img_bmy_code.txt', 'r', encoding='utf-8') as fd:
            for line in fd:
                line = line.strip()
                arrs_a = line.split('*')
                img_file = arrs_a[0]
                bmy_code = '{0} '.format(arrs_a[1])
                if bmy_code in bmy_code_bmy_id_dict:
                    org_bmy_id = bmy_code_bmy_id_dict[bmy_code] - 1
                    print('##: {0}*{1};'.format(img_file, org_bmy_id))
                else:
                    print('@@@@@@@@@@@@@@@@@@@@@@@@ {0};'.format(bmy_code))

    @staticmethod
    def generate_txt_by_wxs_tds_ok_images():
        '''
        将无锡所测试集中标注出年款的图片文件名和年款编号写进文件文件中
        '''
        base_path = Path('E:/work/tcv/temp/wlok')
        with open('./work/wt_img_bmy_code.txt', 'w+', encoding='utf-8') as wfd:
            for img_obj in base_path.iterdir():
                full_fn = str(img_obj)
                arrs_a = full_fn.split('-')
                prefix = arrs_a[0]
                arrs_b = arrs_a[0].split('\\')
                bmy_code = arrs_b[-1]
                img_file = full_fn[len(prefix)+1:]
                wfd.write('{0}*{1}\n'.format(img_file, bmy_code))