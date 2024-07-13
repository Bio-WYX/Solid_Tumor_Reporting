import sys
sys.path.append("/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/pc")
import pandas as pd
from PcClassificationHome.PcModules.PcBaseclassify import PcBaseclassify
from PcClassificationHome.PcFuctions.PcBaseinit import PcBaseinit
from PcClassificationHome.PcFuctions.PcNCCN import *

class PcOverall(PcBaseclassify):
    def __init__(self):
         super(PcOverall, self).__init__()
    @property
    def var_dict(self):
        _var_df_1 = PcBaseinit(self._report,self._maf).get_classified(1)
        _var_df_2 = PcBaseinit(self._report,self._maf).get_classified(2)
        _var_df = pd.concat([_var_df_1,_var_df_2])
        _db = pd.read_excel(self._nccn_database)
        _dict = get_nccn(_var_df,_db,self._cancer)
        return _dict

if __name__ == '__main__':
    var = PcOverall()
    var.maf = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试数据/诺禾数据/MAF测试/SP20308W01.output_tnscope.filter.maf.oncokb_out"
    var.report = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试数据/诺禾数据/Sample_tumorSP20308W01.Analyses.xls"
    var.nccn_database = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/dependent/database/靶向用药-NCCN-FDA-NMPA-专家共识-lw.xlsx"
    var.cancer = "NSCLC"
    print(var.var_dict)