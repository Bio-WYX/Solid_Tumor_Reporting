import sys
sys.path.append("/mnt/e/ansaisi/641panel/pan_cancer/pc")
from PcClassificationHome.PcFuctions.PcBaseinit import PcBaseinit
from PcClassificationHome.PcFuctions.PcTranslate import Translate
from PcClassificationHome.PcFuctions.PcGet_return_dict import get_return_dict 
from PcClassificationHome.PcModules.PcBaseclassify import PcBaseclassify
from PcClassificationHome.PcFuctions.PcFilter_level3 import PcFilter_level3
from functools import partial
import configparser
import pandas as pd

class PcDDR_var(PcBaseclassify):
    def __init__(self):
        super(PcDDR_var, self).__init__()
    @property
    def number(self):
        """获取DDR相关基因变异个数
        """
        try:
            _df = PcBaseinit(self._report,self._maf).get_classified(all)
            _df = PcFilter_level3(_df)
            _ddr_db = pd.read_excel(self._gene_list,sheet_name="DDR相关基因")
            _df['SYMBOL'] = _df['SYMBOL_x']
            _ddr_var = _df[_df["SYMBOL"].isin(_ddr_db["DDR_gene"])]
            self._number = _ddr_var.shape[0]
            if isinstance(self._number,int) == False:
                raise ValueError("DDR相关突变个数应为int")
            else:
                return self._number
        except ValueError as e:
            print("引发异常：",repr(e))
    @property
    def var_dict(self):
        """获取DDR基因相关变异信息字典
        """
        _df = PcBaseinit(self._report,self._maf).get_classified(all)
        _df = PcFilter_level3(_df)
        _df['SYMBOL'] = _df['SYMBOL_x']
        _df = _df[_df['AlterRatio(%)'] >= 5]
        _ddr_db = pd.read_excel(self._gene_list,sheet_name="DDR相关基因")
        _ddr_var = _df[_df["SYMBOL"].isin(_ddr_db["DDR_gene"])]
        translate_clinvar = partial(Translate().translate_clinvar,DURG_NAME_DATABASE=self.durg_name_database)
        translate_consequence_1 = partial(Translate().translate_consequence,DURG_NAME_DATABASE=self.durg_name_database)
        _ddr_var['Consequence_cn'] = _ddr_var["Consequence"].apply(translate_consequence_1)
        _ddr_var["ClinVar_CLNSIG"] = _ddr_var["ClinVar_CLNSIG"].apply(translate_clinvar)
        _ddr_var["ClinVar_CLNSIG"] = _ddr_var["ClinVar_CLNSIG"].astype('category')
        clnsig_order = ['致病',
                        '致病/可能致病',
                        '可能致病',
                        '风险因素',
                        '与风险因素关联',
                        '药物反应',
                        '对致病性的解释存在冲突',
                        '临床意义未明',
                        '预防性的',
                        '未提供',
                        '-'
                        ]
        _ddr_var["ClinVar_CLNSIG"].cat.set_categories(clnsig_order,inplace=True)
        _ddr_var.sort_values('ClinVar_CLNSIG',ascending=True,inplace=True)
        _ddr_var['Index'] = _ddr_var['Allele']
        _ddr_var.set_index(['Index'],inplace=True)
        self._var_dict = _ddr_var.T.to_dict()
        return self._var_dict

    ##### 增加MSH基因的信息 #####
    @property
    def msh_dict(self):
        if self._cancer == 'Colorectal Cancer':
            _df = PcBaseinit(self._report, self._maf).get_classified(all)
            _df = PcFilter_level3(_df)
            _df['SYMBOL'] = _df['SYMBOL_x']
            _df = _df[_df['AlterRatio(%)'] >= 5]
            _msh_db = pd.read_excel(self._gene_list, sheet_name="DDR相关基因")
            _msh_var = _df[_df["SYMBOL"].isin(_msh_db["MSH_gene"])]
            _msh_var["mutation_HGVSc_x"] = _msh_var["mutation"].str.cat(_msh_var["HGVSc_x"], sep = "\n")

            diff_list1 = set(_msh_db["MSH_gene"].tolist()).difference(set(_msh_var["SYMBOL"].tolist()))
            diff_list = [x for x in diff_list1 if pd.isnull(x) == False and x != 'nan']
            names = _msh_var.columns.tolist()
            gene_list = []
            result_list = []
            for d in diff_list:
                gene_list.append(d)
                result_list.append('未检测到相关基因突变')
            data_f = {}
            for n in names:
                if n == 'SYMBOL':
                    data_f[n] = gene_list
                elif n == 'mutation':
                    data_f[n] = result_list
                elif n == 'HGVSc_x':
                    data_f[n] = [''] * len(gene_list)
                elif n == 'Allele':
                    data_f[n] = gene_list
                else:
                    data_f[n] = ['-'] * len(gene_list)
            data_f['mutation_HGVSc_x'] = result_list
            #print (data_f)
            diff_add = pd.DataFrame(data_f)
            #_msh_var['mutation_HGVSc_x'] = '-'
            new_var = _msh_var.append(diff_add, ignore_index=True)
            _msh_var = new_var
            translate_clinvar = partial(Translate().translate_clinvar, DURG_NAME_DATABASE=self.durg_name_database)
            translate_consequence_1 = partial(Translate().translate_consequence, DURG_NAME_DATABASE=self.durg_name_database)
            _msh_var['Consequence_cn'] = _msh_var["Consequence"].apply(translate_consequence_1)
            _msh_var["ClinVar_CLNSIG"] = _msh_var["ClinVar_CLNSIG"].apply(translate_clinvar)
            _msh_var["ClinVar_CLNSIG"] = _msh_var["ClinVar_CLNSIG"].astype('category')
            _msh_var.rename(columns={'SYMBOL': 'SYMBOL_m'}, inplace=True)
            #_msh_var.rename(columns={'mutation': 'mutation_m'}, inplace=True)
            #_msh_var.rename(columns={'HGVSc_x': 'HGVSc_x_m'}, inplace=True)
            #_msh_var["mutation_HGVSc_x"] = _msh_var["mutation"].str.cat(_msh_var["HGVSc_x"], sep = "\n")
            _msh_var.rename(columns={'HGVSp_x': 'HGVSp_x_m'}, inplace=True)
            #_msh_var["AF_x_m"] = ['{}%'.format(i) for i in _msh_var["AF_x"] if i != '-' else]
            _msh_var["AF_x_m"] = [i if i == '-' else '{}%'.format(i) for i in _msh_var["AF_x"]]
            #_msh_var.rename(columns={'AF_x': 'AF_x_m'}, inplace=True)
            _msh_var.rename(columns={'Consequence_cn': 'Consequence_cn_m'}, inplace=True)
            _msh_var.rename(columns={'ClinVar_CLNSIG': 'ClinVar_CLNSIG_m'}, inplace=True)
            clnsig_order = ['致病',
                            '致病/可能致病',
                            '可能致病',
                            '风险因素',
                            '与风险因素关联',
                            '药物反应',
                            '对致病性的解释存在冲突',
                            '临床意义未明',
                            '预防性的',
                            '未提供',
                            '-'
                            ]
            _msh_var["ClinVar_CLNSIG_m"].cat.set_categories(clnsig_order, inplace=True)
            _msh_var.sort_values('ClinVar_CLNSIG_m', ascending=True, inplace=True)
            _msh_var['Index'] = _msh_var['Allele']
            _msh_var.set_index(['Index'], inplace=True)
            self._msh_dict = _msh_var.T.to_dict()
        else:
            self._msh_dict = {}
        return self._msh_dict

if __name__ == '__main__':
    var = PcDDR_var()
    var.maf = "/mnt/e/ansaisi/641panel/20220510/SP20408W01.fusion.json.clean.oncokb_out"
    var.report = "/mnt/e/ansaisi/641panel/20220510/Sample_SP20408W01.Analyses.all.xls"
    var.gene_list = "/mnt/e/ansaisi/641panel/pan_cancer/dependent/gene_lists/641_genelist.xlsx"
    var.durg_name_database = "/mnt/e/ansaisi/641panel/pan_cancer/dependent/durgs/药物名称.xlsx"
    print(var.var_dict)
    
