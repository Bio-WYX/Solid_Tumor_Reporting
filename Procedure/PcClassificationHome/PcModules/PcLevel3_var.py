import sys
sys.path.append("/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/pc")
from numpy import NAN, NaN, nan
import pandas as pd
from PcClassificationHome.PcFuctions.PcGet_return_dict import get_return_dict 
from PcClassificationHome.PcFuctions.PcFilter_level3 import PcFilter_level3
from PcClassificationHome.PcFuctions.PcBaseinit import PcBaseinit
from PcClassificationHome.PcModules.PcBaseclassify import PcBaseclassify
from PcClassificationHome.PcFuctions.PcTranslate import Translate
from functools import partial
class PcGet_level3_var(PcBaseclassify):
    def __init__(self):
        super(PcGet_level3_var, self).__init__()

    @property
    def number(self):
        """获取三级变异个数
        """
        try:
            self._classified = PcBaseinit(self._report,self._maf).get_classified(3)
            self._classified = self._classified[self._classified['AlterRatio(%)']>10]
            self._number = len(self._classified["Allele"].drop_duplicates(keep='first',inplace=False).index.values) 
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
        self._classified = self._classified[self._classified['AlterRatio(%)']>10]
        _var_df = self._classified.drop_duplicates(subset='Allele',keep='first',inplace=False,ignore_index=True) 
        #三级变异去重
        # _var_df_only = _var_df[["mutation","SYMBOL","AF"]]
        if _var_df.shape[0] == 0:
            _var_df['Consequence_cn'] = ""
        else:
            translate_consequence_1 = partial(Translate().translate_consequence,DURG_NAME_DATABASE=self.durg_name_database)
            _var_df['Consequence_cn'] = _var_df["Consequence"].apply(translate_consequence_1)
            _var_df = _var_df[~(_var_df["HGVSc_x"] == "-")]

        ###添加预后结果###
        prognosis_re = pd.read_excel(self._prognosis, header=0)
        prognosis_df = prognosis_re.loc[:, ['Gene', self._cancer]]
        prognosis_df.columns = ['SYMBOL_x', 'prognosis']
        df2 = pd.merge(_var_df, prognosis_df, how='left', on='SYMBOL_x')
        _var_df = df2

        self._var_dict = get_return_dict(_var_df)
        return self._var_dict

if __name__== "__main__":
    var = PcGet_level3_var()
    var.maf = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试数据/诺禾数据/MAF测试/SP20308W01.output_tnscope.filter.maf.oncokb_out"
    var.report = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试数据/诺禾数据/Sample_tumorSP20308W01.Analyses.xls"
    var.gene_list = "/Users/guanhaowen/Desktop/肿瘤产品调研/肿瘤产品调研测试模板/pan_cancer/dependent/gene_lists/641_genelist.xlsx"
    var.durg_name_database = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/dependent/durgs/药物名称.xlsx"
    var.gene_description = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/dependent/database/oncokb.gene.des翻译文档_待校正.sle.xlsx"
    var.var_description = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/dependent/database/变异注释数据库2021_11_10.xlsx"
    var.number
    var.var_dict