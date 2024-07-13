from ar.loader.WtBloodVariantLoader import WtBloodVariantLoader
from ar.loader.WtSampleInfoLoader import WtSampleInfoFromExcel


"""
用于加载输入的样本信息，变异位点信息，和其它配置信息
WtInputInfoLoader 可以支持批量加载信息，load函数返回WtInputInfo列表
"""


class WtInputInfoLoader:
    @staticmethod
    def load(sample_path, variant_path, other_info, sample_loader=None, variant_loader=None, sub_loader_config={}):
        """"
        加载数据
        :param sample_path:
        :param variant_path:
        :param other_info:
        :param sample_loader:
        :param variant_loader:
        :param sub_loader_config:
        :param loader_config: dict
        :return:
        """
        if not sample_loader:
            sample_loader = WtSampleInfoFromExcel()

        sample_loader.load(sample_path, sub_loader_config)

        if not variant_loader:
            variant_loader = WtBloodVariantLoader()

        variant_loader.load(variant_path, sub_loader_config)

        input_info_list = []
        for item in sample_loader.items():
            print(item)
            k = item['code']
            variant_info = variant_loader.get(k)
            if variant_info:
                data = {
                    'sample': item,
                    'other': other_info
                }
                data.update(variant_info)
                input_info_list.append(WtInputInfo(data))

        return input_info_list


class WtInputInfo:
    def __init__(self, data):
        self.data = data

    def get(self, t, key):
        if key is None:
            return self.data[t]
        else:
            return self.data[t].get(key)

    def get_all(self):
        return self.data

    def get_sample(self, key=None):
        if key is None:
            return self.data['sample']
        else:
            return self.data['sample'].get(key)

    def get_variant(self, key=None):
        if key is None:
            return self.data['variant']
        else:
            return self.data['variant'].get(key)

    def get_other(self, key=None):
        if key is None:
            return self.data['other']
        else:
            return self.data['other'].get(key)