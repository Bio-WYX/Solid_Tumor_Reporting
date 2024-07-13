import abc

import xlrd


class WtSampleInfoLoader():
    def __init__(self):
        self.data = []

    def get(self, sample_code):
        for item in self.data:
            if item['code'] == sample_code:
                return item

        return None

    def items(self):
        return self.data

    @abc.abstractmethod
    def load(self, file, loader_config):
        pass


class WtSampleInfoFromExcel(WtSampleInfoLoader):
    def get_title(self, key, head, array, def_val='-'):
        return str(array[head.index(key)]).replace(".0", "") if key in head else def_val

    def load(self, file, loader_config):
        """
        加载excel文件到data中
        :param loader_config:
        :param file:
        """
        xlsx = xlrd.open_workbook(file)
        table = xlsx.sheets()[0]
        nrows = table.nrows
        head = table.row_values(0)
        sample_list = []
        for i in range(nrows):
            array = table.row_values(i)
            if (len(array) < 10): continue
            sample = {
                '样本编号': self.get_title('样本编号', head, array),
                '采样日期': self.get_title('采样日期', head, array),
                '接收日期': self.get_title('接收日期', head, array),
                '姓名': self.get_title('姓名', head, array),
                '性别': self.get_title('性别', head, array),
                '年龄': self.get_title('年龄', head, array),
                '民族': self.get_title('民族', head, array),
                '家系编号': self.get_title('家系编号', head, array),
                '临床表现': self.get_title('临床表现', head, array),
                '临床诊断': self.get_title('临床诊断', head, array),
                '家族史': self.get_title('家族史', head, array),
                '样本类型': self.get_title('样本类型', head, array),
                '既往诊断结果': self.get_title('既往诊断结果', head, array),
                '既往用药史': self.get_title('既往用药史', head, array),
                '药物过敏史': self.get_title('药物过敏史', head, array)
            }

            #每个样本都必须指定code为唯一编号，用于索引
            sample['code'] = sample['样本编号']
            sample_list.append(sample)

        self.data = sample_list