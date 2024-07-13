import sys
sys.path.append("D:\肿瘤产品调研\测试模板\pan_cancer\pc")
import pandas as pd
from PcClassificationHome.PcModules.PcBaseclassify import PcBaseclassify
from PcClassificationHome.PcFuctions.PcBaseinit import PcBaseinit
from PcClassificationHome.PcFuctions.PcGet_envidence_proof import get_envidence_proof
from PcClassificationHome.PcFuctions.PcCoregene_fucs import *
import configparser
from docxtpl import DocxTemplate
class PcCoregene(PcBaseclassify):
    def __init__(self):
        super(PcCoregene, self).__init__()
    @property
    def var_dict(self):
        _var_df_1 = PcBaseinit(self._report,self._maf).get_classified(1)
        _var_df_2 = PcBaseinit(self._report,self._maf).get_classified(2)
        _var_df_3 = PcBaseinit(self._report,self._maf).get_classified(3)
        _var_df = pd.concat([_var_df_1,_var_df_2,_var_df_3])
        _var_df["证据等级"] = _var_df["HIGHEST_LEVEL"].apply(get_envidence_proof)
        if self._cancer == 'NSCLC':
            _nsclc_core_list = ['ALK',
                            'BRAF',
                            'EGFR',
                            'ERBB2',
                            'KRAS',
                            'MET',
                            'NTRK1',
                            'NTRK2',
                            'NTRK3',
                            # 'RET',
                            'ROS1']
            _var_df = _var_df[_var_df["SYMBOL"].isin(_nsclc_core_list)]
            _var_df["突变类型"] = _var_df['SYMBOL'].apply(get_type)
            _var_df.sort_values(by="SYMBOL" , ascending=False)
            _dict =_var_df.to_dict('records')   
        else:
            _dict = None    
        return _dict
    @property
    def text(self):
        _text = get_text(self._cancer)
        return _text

