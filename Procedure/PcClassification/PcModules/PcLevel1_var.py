from numpy import NAN, NaN, nan
import sys
sys.path.append("/data/autoReportV2/")
sys.path.append("/data/autoReportV2/reporter/guanhaowen/pan_cancer/pc/")
from functools import partial
from PcClassification.PcFuctions.PcTranslate import Translate
from PcClassification.PcFuctions.PcGet_envidence_proof import get_envidence_proof
from PcClassification.PcFuctions.PcGet_sensetive import get_sensetive
from PcClassification.PcFuctions.PcGet_return_dict import get_return_dict 
from PcClassification.PcFuctions.PcBaseinit import PcBaseinit
from PcClassification.PcFuctions.PcDescription import *
from PcClassification.PcModules.PcBaseclassify import PcBaseclassify


class PcGet_level1_var(PcBaseclassify):
    """提取一级变异信息
    """
    def __init__(self):
        super(PcGet_level1_var,self).__init__()

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
        _var_df = PcBaseinit(self._report,self._maf).get_classified(1)
        #一级变异去重 
        _var_df["证据等级"] = _var_df["HIGHEST_LEVEL"].apply(get_envidence_proof) 
        #转换ACMG证据等级
        _var_df["敏感"] = get_sensetive(_var_df) 
        #获得敏感靶向用药
        translate_durg = partial(Translate().translate_durg,DURG_NAME_DATABASE=self._durg_name_database)
        _var_df["敏感"] = _var_df["敏感"].apply(translate_durg) 
        #翻译药物名称
        _var_df["耐药"] = _var_df["LEVEL_R1"].fillna("无").astype(str).apply(translate_durg)
        #翻译药物名称
        _var_df_only = _var_df[["mutation","EXON","SYMBOL","AF","证据等级","敏感","耐药","MUTATION_EFFECT_CITATIONS",'HGVSp_x']] 
        #保留必要信息
        _var_list = _var_df["mutation"].values 
        #一级变异列表
        self._var_dict = get_return_dict(_var_df_only) 
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

