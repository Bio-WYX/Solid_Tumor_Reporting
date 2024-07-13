import sys
sys.path.append("/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/pc")
from PcClassificationHome.PcFuctions.PcBaseinit import PcBaseinit
from PcClassificationHome.PcFuctions.PcTranslate import Translate
from PcClassificationHome.PcFuctions.PcGet_return_dict import get_return_dict 
from PcClassificationHome.PcModules.PcBaseclassify import PcBaseclassify
from PcClassificationHome.PcFuctions.PcFilter_level3 import PcFilter_level3
from PcClassificationHome.PcFuctions.PcGet_disease import PcGet_disease
from functools import partial
import pandas as pd

class PcGermline_var(PcBaseclassify):
    def __init__(self):
        super(PcGermline_var, self).__init__()
    
    @property
    def number(self):
        _db = pd.read_excel(self._gene_list,sheet_name="遗传易感")
        _df = PcBaseinit(self._report,self._maf).get_classified(all)
        _df['SYMBOL'] = _df['SYMBOL_x']
        _df['AF'] = _df['AF_x']
        _df = PcFilter_level3(_df)
        _var = _df[_df["SYMBOL"].isin(_db["所有基因"])]
        _var = _var[_var["AF"] > 20]
        self._number = _var.shape[0]
        return self._number

    @property
    def pathogenic(self):
        _df = pd.read_excel(self._result, sheet_name="variant")
        _df = _df.dropna(axis=0, subset=["致病性"])
        df_gp = dict(_df['致病性'].value_counts())
        all_num = _df.shape[0]
        pathogenic_list = []
        if '致病' in df_gp.keys():
            zhibing = '{}个致病变异'.format(df_gp['致病'])
            pathogenic_list.append(zhibing)
        if '可能致病' in df_gp.keys():
            keneng = '{}个可能致病变异'.format(df_gp['可能致病'])
            pathogenic_list.append(keneng)
        if 'VUS1' in df_gp.keys():
            vus1 = '{}个临床意义未明1级（VUS1）变异'.format(df_gp['VUS1'])
            pathogenic_list.append(vus1)
        if 'VUS2' in df_gp.keys():
            vus2 = '{}个临床意义未明2级（VUS2）变异'.format(df_gp['VUS2'])
            pathogenic_list.append(vus2)
        if 'VUS3' in df_gp.keys():
            vus3 = '{}个临床意义未明3级（VUS3）变异'.format(df_gp['VUS3'])
            pathogenic_list.append(vus3)
        pathogenic_str = '，'.join(pathogenic_list)
        pathogenic_final = pathogenic_str[::-1].replace('，', '和', 1)[::-1]
        self._pathogenic = {'all_num':all_num, 'pathogenic':pathogenic_final}
        return self._pathogenic

    @property
    def var_dict(self):
        _db = pd.read_excel(self._gene_list,sheet_name="遗传易感")
        _df = PcBaseinit(self._report,self._maf).get_classified(all)
        _df['SYMBOL'] = _df['SYMBOL_x']
        _df['AF'] = _df['AF_x']
        _df = PcFilter_level3(_df)
        
        _var = _df[_df["SYMBOL"].isin(_db["所有基因"])]
        _var = _var[_var["AF"] > 20]
        if _var.shape[0] == 0:
            self._var_dict = {}
        else:
            translate_clinvar = partial(Translate().translate_clinvar,DURG_NAME_DATABASE=self._durg_name_database)
            _var["ClinVar_CLNSIG"] = _var["ClinVar_CLNSIG"].apply(translate_clinvar)
            get_disease = partial(PcGet_disease,gene_list_ycyg = self._gene_list)
            translate_consequence_1 = partial(Translate().translate_consequence,DURG_NAME_DATABASE=self.durg_name_database)
            _var['Consequence_cn'] = _var["Consequence"].apply(translate_consequence_1)
            _var["疾病"] = _var["SYMBOL"].apply(get_disease)
            _var['chr'] = _var['Allele'].str.split(":",expand=True)[0].str.split("chr",expand=True)[1]
            self._var_dict = get_return_dict(_var)
        return self._var_dict
if __name__== "__main__":
    var = PcGermline_var()
    var.maf = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试数据/诺禾数据/MAF测试/SP20308W01.output_tnscope.filter.maf.oncokb_out"
    var.report = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试数据/诺禾数据/Sample_tumorSP20308W01.Analyses.xls"
    var.gene_list = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/dependent/gene_lists/641_genelist.xlsx"
    var.durg_name_database = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/dependent/durgs/药物名称.xlsx"
    print(var.var_dict)


