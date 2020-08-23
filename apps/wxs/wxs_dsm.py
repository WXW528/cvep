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
        bmy_org_sim_dict = WxsDsm.get_bmy_org_sim_dict()
        print('读入原始年款编号和简化年款编号字典')
        bmy_code_bmy_id_dict = CBmy.get_bmy_code_bmy_id_dict()
        print('读出bmy_code和bmy_id对应关系字典')
        img_file_to_full_fn_dict = WxsDsm.get_wxs_tds_img_file_full_fn_dict()
        print('获取图片文件名和全路么名字典')
        with open('./work/addition_ds.txt', 'w+', encoding='utf-8') as wfd:
            with open('./work/wt_img_bmy_code.txt', 'r', encoding='utf-8') as fd:
                for line in fd:
                    line = line.strip()
                    arrs_a = line.split('*')
                    img_file = arrs_a[0]
                    bmy_code = '{0} '.format(arrs_a[1])
                    if bmy_code in bmy_code_bmy_id_dict:
                        org_bmy_id = bmy_code_bmy_id_dict[bmy_code] - 1
                        print('##: {0}*{1};'.format(img_file, org_bmy_id))
                        if org_bmy_id not in bmy_org_sim_dict:
                            print('Error: {0} !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1'.format(org_bmy_id))
                        full_fn = img_file_to_full_fn_dict[img_file]
                        wfd.write('{0}*{1}\n'.format(full_fn, org_bmy_id))
                    else:
                        print('@@@@@@@@@@@@@@@@@@@@@@@@ {0};'.format(bmy_code))

    @staticmethod
    def get_bmy_org_sim_dict():
        '''
        从/media/zjkj/work/yantao/w1/bmy_org_sim_dict.txt中读出内容初始化字典
        '''
        bmy_org_sim_dict = {}
        with open('/media/zjkj/work/yantao/w1/bmy_org_sim_dict.txt', 'r', encoding='utf-8') as fd:
            for line in fd:
                line = line.strip()
                arrs_a = line.split(':')
                bmy_org_sim_dict[int(arrs_a[0])] = int(arrs_a[1])
        return bmy_org_sim_dict

    @staticmethod
    def get_wxs_tds_img_file_full_fn_dict():
        '''
        获取在/media/zjkj/work/yantao/zjkj/test_ds目录下图片文件名和
        全路径名字典
        '''
        img_file_to_full_fn_dict = {}
        base_path = Path('/media/zjkj/work/yantao/zjkj/test_ds')
        for sub1 in base_path.iterdir():
            for sub2 in sub1.iterdir():
                for file_obj in sub2.iterdir():
                    full_fn = str(file_obj)
                    arrs_a = full_fn.split('/')
                    img_file = arrs_a[-1]
                    img_file_to_full_fn_dict[img_file] = full_fn
        return img_file_to_full_fn_dict

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

    @staticmethod
    def generate_wxs_tds_for_integration_test():
        '''
        将整理过的无锡所测集图片文件和正确品牌名称导出供刘兵做集成测试
        '''
        brand_idx_to_brand_name_dict = WxsDsm.get_brand_idx_to_brand_name_dict()
        for k, v in brand_idx_to_brand_name_dict.items():
            print('### {0} => {1};'.format(k, v))
        i_debug = 1
        if 1 == i_debug:
            return
        with open('/media/zjkj/work/yantao/fgvc/dcl_onnx/datasets/'\
                    'CUB_200_2011/anno/bid_brand_test_ds.txt', 'r', \
                    encoding='utf-8') as fd:
            for line in fd:
                line = line.strip()
                arrs_a = line.split('*')
                full_fn = arrs_a[0]
                arrs_b = full_fn.split('/')
                img_file = arrs_b[-1]
                sim_bmy_id = int(arrs_a[1])
                brand_idx = int(arrs_a[2])
                print('{0}    => {1};'.format(img_file, brand_idx))

    @staticmethod
    def get_brand_idx_to_brand_name_dict():
        '''
        从/media/zjkj/work/yantao/w1_0823/bid_brands_dict.txt中读出品牌索引号和
        品牌名字典
        '''
        brand_idx_to_brand_name_dict = {}
        with open('/media/zjkj/work/yantao/w1_0823/bid_brands_dict.txt', 'r', encoding='utf-8') as bfd:
            for line in bfd:
                line = line.strip()
                arrs_a = line.split(':')
                brand_idx = int(arrs_a[0])
                brand_name = arrs_a[1]
                brand_idx_to_brand_name_dict[brand_idx] = brand_name
        return brand_idx_to_brand_name_dict