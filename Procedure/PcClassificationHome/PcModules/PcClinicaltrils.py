import sys
sys.path.append("D:\肿瘤产品调研\测试模板\pan_cancer\pc")
import pandas as pd 
from PcClassificationHome.PcFuctions.PcBaseinit import PcBaseinit
from PcClassificationHome.PcFuctions.PcFilter_clinicaltrails import filter_clinicaltrail
from PcClassificationHome.PcFuctions.PcGet_clinicaltrials2 import filter_clinicaltrail_2
from PcClassificationHome.PcFuctions.PcTranslate import Translate 
from PcClassificationHome.PcModules.PcBaseclassify import PcBaseclassify
from functools import partial


class PcClinicaltrils(PcBaseclassify):
    """获取变异相关临床试验信息
    """
    def __init__(self):
        super(PcClinicaltrils, self).__init__()
        

    @property
    def clinical_dict(self):
        _var_df_1 = PcBaseinit(self._report,self._maf).get_classified(1)
        _var_df_2 = PcBaseinit(self._report,self._maf).get_classified(2)
        # _var_df_3 = PcBaseinit(self._report,self._maf).get_classified(3)
        _df = pd.concat([_var_df_1,_var_df_2,])
                        #  _var_df_3])
        cli_df = filter_clinicaltrail(_df,self._clinicaltrils_database,self._cancer)

        translate_durg = partial(Translate().translate_durg,DURG_NAME_DATABASE=self._durg_name_database)
        cli_df['Interventions'] = cli_df['Interventions'].apply(translate_durg)
        cli_dict = filter_clinicaltrail_2(cli_df)
        return cli_dict

if __name__ == '__main__':
    var = PcClinicaltrils()
    var.maf = "D:\\肿瘤临床数据\\641panel\\20220321/SP20309W06.output_tnscope.filter.maf.clean.oncokb_out"
    var.report = "D:\\肿瘤临床数据\\641panel\\20220321/Sample_tumorSP20309W06.Analyses.xls"
    var.clinicaltrils_database = "D:\肿瘤产品调研\测试模板/pan_cancer/dependent/database/clinicaltrails_database_v4.xlsx"
    var.durg_name_database = "D:\肿瘤产品调研\测试模板/pan_cancer/dependent/durgs/药物名称.xlsx"
    var.cancer = 'NSCLC'
    # var.cancer = 'Colorectal Cancer'
    print(var.clinical_dict)