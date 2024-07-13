from numpy import NAN, NaN, nan
import pandas as pd
import sys
sys.path.append("/data/autoReportV2/")
sys.path.append("/data/autoReportV2/reporter/guanhaowen/pan_cancer/pc/")
from PcClassification.PcFuctions.PcGet_return_dict import get_return_dict 
from PcClassification.PcFuctions.PcFilter_level3 import PcFilter_level3
from PcClassification.PcFuctions.PcBaseinit import PcBaseinit
from PcClassification.PcModules.PcBaseclassify import PcBaseclassify
class PcGet_level3_var(PcBaseclassify):
    def __init__(self):
        super(PcGet_level3_var, self).__init__()

    @property
    def number(self):
        """获取三级变异个数
        """
        try:
            self._classified = PcBaseinit(self._report,self._maf).get_classified(3)
            self._number = len(self._classified["mutation"].drop_duplicates(keep='first',inplace=False).index.values) 
            if isinstance(self._number,int) == False:
                raise ValueError("变异个数应为int")
            else:
                return self._number
        except ValueError as e:
            print("引发异常：",repr(e))
    
    @property       
    def var_dict(self):
        """获取三级变异信息字典
        """
        self._classified = PcBaseinit(self._report,self._maf).get_classified(3)
        _var_df = self._classified.drop_duplicates(subset='mutation',keep='first',inplace=False,ignore_index=True) 
        #三级变异去重
        # _var_df_only = _var_df[["mutation","SYMBOL","AF"]]
        self._var_dict = get_return_dict(_var_df)
        return self._var_dict

