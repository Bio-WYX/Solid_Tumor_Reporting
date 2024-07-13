# -- coding: utf-8 --**
from numpy import NAN, NaN, nan
from functools import partial
import sys
sys.path.append("/data/autoReportV2/")
sys.path.append("/data/autoReportV2/reporter/guanhaowen/pan_cancer/pc/")
from PcClassification.PcFuctions.PcTranslate import Translate
from PcClassification.PcFuctions.PcGet_return_dict import get_return_dict 
from PcClassification.PcFuctions.PcBaseinit import PcBaseinit
from PcClassification.PcFuctions.PcDescription import *
from PcClassification.PcModules.PcBaseclassify import PcBaseclassify
import pandas as pd

class PcDurg(PcBaseclassify):
    """提取一级变异信息
    """
    def __init__(self):
        super(PcDurg,self).__init__()
    @property
    def number(self):
        """一级变异个数
        """
        try:
            self._classified = PcBaseinit(self._report,self._maf).get_classified(1)
            self._number = len(self._classified["mutation"].drop_duplicates(keep='first',inplace=False).index.values) 
            if isinstance(self._number,int) == False:
                raise ValueError("变异个数应为int")
            else:
                return self._number
        except ValueError as e:
            print("引发异常：",repr(e))

    @property
    def var_dict(self):
        _var_df_1 = PcBaseinit(self._report,self._maf).get_classified(1)
        _var_df_2 = PcBaseinit(self._report,self._maf).get_classified(2)
        _var_df = pd.concat([_var_df_1,_var_df_2])
        translate_durg = partial(Translate().translate_durg,DURG_NAME_DATABASE=self._durg_name_database)
       
  

        #获得敏感靶向用药
        # print(_var_df['LEVEL_1'])
        _var_df["A_durgs"] = _var_df['LEVEL_1'].fillna("").astype(str).apply(translate_durg) + _var_df['LEVEL_2'].fillna("").astype(str).apply(translate_durg)
        _var_df["B_durgs"] = _var_df['LEVEL_3A'].fillna("").astype(str).apply(translate_durg)
        _var_df["C_durgs"] = _var_df['LEVEL_3B'].fillna("").astype(str).apply(translate_durg)
        _var_df["耐药"] = _var_df["LEVEL_R1"].fillna("").astype(str).apply(translate_durg) +  _var_df["LEVEL_R2"].fillna("").astype(str).apply(translate_durg)
        _var_list = _var_df["mutation"].values 
        #一级变异列表
        self._var_dict = get_return_dict(_var_df) 
        #df转化为字典
        for i in _var_list:
                self._var_dict[i]["基因描述"]  = Gene_description(self._var_dict[i]["SYMBOL"],self._gene_description)
                self._var_dict[i]["变异描述"]  = Var_description(self._var_dict[i],self._var_description)
        try:
            if isinstance(self._var_dict,dict) == False:
                raise ValueError("level1_var字典格式错误")
            else:
                return self._var_dict
        except ValueError as e:
            print("引发异常：",repr(e))

