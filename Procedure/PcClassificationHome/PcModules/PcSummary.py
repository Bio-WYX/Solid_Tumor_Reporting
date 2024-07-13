import sys
sys.path.append("D:\肿瘤产品调研\测试模板\pan_cancer\pc")
from PcClassificationHome.PcModules.PcBaseclassify import PcBaseclassify
from PcClassificationHome.PcFuctions.PcBaseinit import PcBaseinit
from PcClassificationHome.PcFuctions.PcGet_return_dict import get_return_dict 
from PcClassificationHome.PcFuctions.PcTranslate import Translate
from functools import partial
import pandas as pd

class PcSummary(PcBaseclassify):
    def __init__(self):
         super(PcSummary, self).__init__()
    @property
    def var_dict(self):
        _var_df_1 = PcBaseinit(self._report,self._maf).get_classified(1)
        _var_df_2 = PcBaseinit(self._report,self._maf).get_classified(2)
        _var_df_3 = PcBaseinit(self._report,self._maf).get_classified(3)
        _var_df = pd.concat([_var_df_1,_var_df_2,_var_df_3])
        translate_clinvar = partial(Translate().translate_clinvar,DURG_NAME_DATABASE=self.durg_name_database)
        _var_df["ClinVar_CLNSIG"] = _var_df["ClinVar_CLNSIG"].apply(translate_clinvar)
        _dict = get_return_dict(_var_df)
        return _dict
