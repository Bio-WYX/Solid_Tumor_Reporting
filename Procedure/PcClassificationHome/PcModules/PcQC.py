import sys
sys.path.append("/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/pc")
import pandas as pd 
import sys
import pandas as pd
import json
from docxtpl import DocxTemplate
from PcClassificationHome.PcModules.PcBaseclassify import PcBaseclassify
class PcGetQC(PcBaseclassify):
    def __init__(self):
        super(PcGetQC,self).__init__()
    @property
    def fasta_qc_result(self):
        q30_dict = {}
        with open(self._fastp_json_file, 'r') as js:
            json_data = json.load(js)
            q30 = round((json_data['summary']['after_filtering']['q30_rate'] * 100), 2)
            base = round((json_data['summary']['before_filtering']['total_bases'] / 1000000000), 2)
            q30_dict = {'q30':q30, 'raw_data':base}

            return q30_dict
    @property
    def bam_qc_result(self):
        bam_dict = {}
        depth = ""
        coverage = ""
        with open(self._bamdst_report, 'r') as bam:
            for b in bam:
                info = b.strip().split('\t')
                if info[0].startswith('#'):
                    continue
                if '[Target] Average depth' in info[0] and 'rmdup' not in info[0]:
                    depth = round(float(info[1]), 2)
                elif '[Target] Coverage (>=10x)' in info[0]:
                    coverage = round(float(info[1].replace("%", '')), 2)
                else:
                    continue
        bam_dict = {'depth':depth, 'coverage':coverage}
        bam.close()

        return bam_dict


if __name__ == '__main__':
    qc = PcGetQC()
    qc.fastp_json_file = "/Users/guanhaowen/Desktop/pancancer_data/20220414/SP20408W01.json"
    qc.bamdst_report = "/Users/guanhaowen/Desktop/pancancer_data/20220414/coverage.report"
    tpl = DocxTemplate("/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/新建文件夹/模板_2.docx")
    context = {"q30":qc.fasta_qc_result['q30'],
                "raw_data":qc.fasta_qc_result['raw_data'],
                "depth":qc.bam_qc_result['depth'],
                "coverage":qc.bam_qc_result['coverage']}
    print(qc.bam_qc_result)
    print(qc.fasta_qc_result)
    tpl.render(context)
    set_of_variables = tpl.get_undeclared_template_variables()
    tpl.save("/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/新建文件夹/test2.docx")
    
    