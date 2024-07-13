import json
import time
class PcInfo():
    def __init__(self):
        self._raw_dict = None

    @property
    def load_dict(self):
        return self._load_dict

    @load_dict.setter
    def load_dict(self, load_dict):
        self._load_dict = load_dict
        #print ('####################\n{}'.format(type(self._load_dict)))

    @property
    def info_dict(self):
        self._info_dict = {'name': self._load_dict["sampleInfo"]['name'],
                'hospital':self._load_dict["sampleInfo"]["hospital"],
                'order_code':self._load_dict["sampleInfo"]["orderCode"],
                'src_code':self._load_dict["sampleInfo"]["srcCode"],
                'department':self._load_dict["sampleInfo"]["department"],
                'age':self._load_dict["sampleInfo"]["age"],
                'doctor':self._load_dict["sampleInfo"]["doctor"],
                'gender': self._load_dict["sampleInfo"]['gender'],
                'sample_id': self._load_dict["sampleInfo"]['sampleId'],
                'phone': self._load_dict["customSampleInfo"]['联系电话'],
                'send_date': self._load_dict["sampleInfo"]['sendSampleTime'],
                # 'birthday': _load_dict["sampleInfo"]birthday, #后期看需求是否添加
                'admission_number': self._load_dict["sampleInfo"]['hospitalNumber'],
                'sampling_date': self._load_dict["sampleInfo"]['getSampleTime'],
                'recive_date': self._load_dict["sampleInfo"]['receiveSampleTime'],
                # 'patient_id': _load_dict["sampleInfo"][''], #后期看需求是否添加
                'report_date': time.strftime("%Y-%m-%d", time.localtime()) ,
                'paltform': self._load_dict["customSampleInfo"]['检测平台'],
                'medical_history': self._load_dict["customSampleInfo"]['用药史'],
                'family_history': self._load_dict["customSampleInfo"]['家族史'],
                'sample_type':self._load_dict["customSampleInfo"]['样本类型'],
                'diagnosis': self._load_dict["customSampleInfo"]["临床诊断"]}
                # "umi":_load_dict["sampleInfo"]umi}  #后期看需求是否添加
        if self._info_dict['gender'] == "男":
            self._info_dict['call'] = '先生'
        elif self._info_dict['gender'] == "女":
            self._info_dict['call'] = '女士'
        return  self._info_dict
    @property
    def fastp_json_file(self):
        self._fastp_json_file = self._load_dict["customFiles"]["fastp_json_file"]
        return self._fastp_json_file
    @property
    def bamdst_report(self):
        self._bamdst_report = self._load_dict["customFiles"]["bamdst_report"]
        return self._bamdst_report
    @property
    def report(self):
        self._report = self._load_dict["customFiles"]["inputPath"]
        return self._report
    @property
    def result(self):
        #self._result = self._load_dict["customFiles"]["result_file"]
        self._result = self._load_dict["customFiles"]["inputPath"]
        return self._result
    @property
    def gvcf(self):
        self._gvcf = self._load_dict["customFiles"]["gvcf_path"]
        return self._gvcf
    @property
    def msi_out(self):
        self._msi_out = self._load_dict["customFiles"]["msi_result_path"]
        return self._msi_out
    @property
    def raw_maf(self):
        self._raw_maf = self._load_dict["customFiles"]["raw_maf_path"]
        return self._raw_maf
    @property
    def cnv_out(self):
        self._cnv_out = self._load_dict["customFiles"]["cnv_result_path"]
        return self._cnv_out
    @property
    def fusion_out(self):
        if self._load_dict["customFiles"]["fusion_path"] == "融合基因检测结果文件":
            self._fusion_out = None
        else:
            self._fusion_out = self._load_dict["customFiles"]["fusion_path"]
        return self._fusion_out
    @property
    def docx_path(self):
        self._docx_path = self._load_dict["docxPath"]
        return self._docx_path
    @property
    def mode(self):
        self._mode = int(self._load_dict['mode'])
        return self._mode
    # @property
    # def diagnosis(self):
    #     self._diagnosis = self._load_dict["customSampleInfo"]["临床诊断"]
    #     return self._diagnosis
    @property
    def template(self):
        if self._mode == None:
            pass
        elif self._mode in [357,358,359,360,361]:
                self._template = 1
        elif self._mode in [362,363,364,365,366]:
                self._template = 2
        return self._template

# if __name__ == '__main__':
#     test_json = '/data/autoReportV2/reporter/guanhaowen/输入参数.json'
#     with open(test_json,'r',encoding='utf-8') as _load_f:
#         test_dict = json.load(_load_f)
#         info = PcInfo()
#         info.load_dict = test_dict
#         print(info.info_dict)
#         print(info.mode)
#         print(info.sv_out)
#         print(info.report)
#         print(info.template)
