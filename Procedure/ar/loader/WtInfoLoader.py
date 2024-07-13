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



class WtInfoLoader(WtSampleInfoLoader):
    def get_title(self, key, head, array, def_val='-'):
        return str(array[head.index(key)]).replace(".0", "") if key in head else def_val

    def load(self, inputInfo, loader_config):
        """
        加载excel文件到data中
        :param loader_config:
        :param file:
        """
        sample_list = []
        if(type(inputInfo) == type({})):
            inputInfo["sampleInfo"].setdefault("srcCode", "-")
            sample = {
                '样本编号': inputInfo["sampleInfo"].setdefault("srcCode", "-"),
                '采样日期': inputInfo["sampleInfo"].setdefault("getSampleTime", "-"),
                '接收日期': inputInfo["sampleInfo"].setdefault("receiveSampleTime", "-"),
                '姓名': inputInfo["sampleInfo"].setdefault("name", "-"),
                '性别': inputInfo["sampleInfo"].setdefault("gender", "-"),
                '年龄': inputInfo["sampleInfo"].setdefault("age", "-"),
                '送检医生': inputInfo["sampleInfo"].setdefault("doctor", "-"),
                '床号': inputInfo["sampleInfo"].setdefault("bedNumber", "-"),
                '申请科室': inputInfo["sampleInfo"].setdefault("department", "-"),
                '医院': inputInfo["sampleInfo"].setdefault("hospital", "-"),
                '门诊号': inputInfo["sampleInfo"].setdefault("outpatient", "-"),
                '住院号': inputInfo["sampleInfo"].setdefault("hospitalNumber", "-"),
                '民族': inputInfo["customSampleInfo"].setdefault("民族", "-"),
                '家系编号': inputInfo["customSampleInfo"].setdefault("家系编号", "-"),
                '临床表现': inputInfo["customSampleInfo"].setdefault("临床表现", "-"),
                '临床诊断': inputInfo["customSampleInfo"].setdefault("临床诊断", "-"),
                '临床信息': inputInfo["customSampleInfo"].setdefault("临床信息", "-"),
                '家族史': inputInfo["customSampleInfo"].setdefault("家族史", "-"),
                '既往病史': inputInfo["customSampleInfo"].setdefault("既往病史", "-"),
                '样本类型': inputInfo["customSampleInfo"].setdefault("样本类型", "-"),
                '样本性状': inputInfo["customSampleInfo"].setdefault("样本性状", "-"),
                '既往用药史': inputInfo["customSampleInfo"].setdefault("既往用药史", "-"),
                '是否怀孕': inputInfo["customSampleInfo"].setdefault("是否怀孕", "-"),
                '药物过敏史': inputInfo["customSampleInfo"].setdefault("药物过敏史", "-"),
                '身份证': inputInfo["customSampleInfo"].setdefault("身份证", "-"),
                '复发性细菌性阴道炎(BV)': inputInfo["customSampleInfo"].setdefault("复发性细菌性阴道炎(BV)", "-"),
                '联系方式': inputInfo["customSampleInfo"].setdefault("联系方式", "-"),
                '变异亲缘': inputInfo["customSampleInfo"].setdefault("变异亲缘", "-"),
                '遗传方式': inputInfo["customSampleInfo"].setdefault("遗传方式", "-"),
                '报告日期': inputInfo["customSampleInfo"].setdefault("报告日期", "-")
            }
        else:
            xlsx = xlrd.open_workbook(inputInfo)
            table = xlsx.sheets()[0]
            nrows = table.nrows
            head = table.row_values(0)
            for i in range(1, nrows):
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
                    '既往病史': self.get_title('既往病史', head, array),
                    '样本类型': self.get_title('样本类型', head, array),
                    '送检医生': self.get_title('送检医生', head, array),
                    '床号': self.get_title('床号', head, array),
                    '申请科室': self.get_title('申请科室', head, array),
                    '医院': self.get_title('医院', head, array),
                    '门诊号': self.get_title('门诊号', head, array),
                    '住院号': self.get_title('住院号', head, array),
                    '既往用药史': self.get_title('既往用药史', head, array),
                    '变异亲缘': self.get_title('变异亲缘', head, array),
                    '遗传方式': self.get_title('遗传方式', head, array),
                    '药物过敏史': self.get_title('药物过敏史', head, array)
                }

                #每个样本都必须指定code为唯一编号，用于索引
        sample['code'] = sample['样本编号']
        sample_list.append(sample)

        self.data = sample_list
