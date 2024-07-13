import pandas as pd 
import sys
sys.path.append("/data/autoReportV2/")
sys.path.append("/data/autoReportV2/reporter/guanhaowen/pan_cancer/pc/")
from PcClassification.PcFuctions.PcBaseinit import PcBaseinit
from PcClassification.PcFuctions.PcFilter_clinicaltrails import filter_clinicaltrail
from PcClassification.PcFuctions.PcGet_clinicaltrials2 import filter_clinicaltrail_2
from PcClassification.PcFuctions.PcTranslate import Translate 
from PcClassification.PcModules.PcBaseclassify import PcBaseclassify
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
        _var_df_3 = PcBaseinit(self._report,self._maf).get_classified(3)
        _df = pd.concat([_var_df_1,_var_df_2,_var_df_3])
        cli_df = filter_clinicaltrail(_df,self._clinicaltrils_database,self._cancer)
        translate_durg = partial(Translate().translate_durg,DURG_NAME_DATABASE=self._durg_name_database)
        cli_df['Interventions'] = cli_df['Interventions'].apply(translate_durg)
        cli_dict = filter_clinicaltrail_2(cli_df)
        return cli_dict

