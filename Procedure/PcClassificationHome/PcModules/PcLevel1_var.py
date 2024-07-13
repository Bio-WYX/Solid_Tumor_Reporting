import sys
#sys.path.append("/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/pc")
from numpy import NAN, NaN, nan
import pandas as pd
from functools import partial
from PcClassificationHome.PcFuctions.PcAb import ab
from PcClassificationHome.PcFuctions.PcTranslate import Translate
from PcClassificationHome.PcFuctions.PcGet_envidence_proof import get_envidence_proof
from PcClassificationHome.PcFuctions.PcGet_sensetive import get_sensetive
from PcClassificationHome.PcFuctions.PcGet_return_dict import get_return_dict 
from PcClassificationHome.PcFuctions.PcBaseinit import PcBaseinit
from PcClassificationHome.PcFuctions.PcDescription import *
from PcClassificationHome.PcModules.PcBaseclassify import PcBaseclassify
from docxtpl import DocxTemplate,InlineImage
import configparser
import datetime
from docx.shared import Mm

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
            self._number = len(self._classified["Allele"].drop_duplicates(keep='first',inplace=False).index.values) 
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
        #转换ACMG证据等
        _var_df["敏感"]= _var_df.apply(get_sensetive,axis=1)
        #获得敏感靶向用药
        translate_durg = partial(Translate().translate_durg,DURG_NAME_DATABASE=self._durg_name_database)
        _var_df["敏感"] = _var_df["敏感"].apply(translate_durg) 
        #翻译药物名称
        _var_df["耐药"] = _var_df["LEVEL_R1"].fillna("无").astype(str).apply(translate_durg)
        #翻译药物名称
        # _var_df_only = _var_df[["mutation","EXON","SYMBOL","AF","证据等级","敏感","耐药","MUTATION_EFFECT_CITATIONS",'HGVSp_x']] 
        #保留必要信息
        # _var_list = _var_df["mutation"].values 
        #一级变异列表
        _var_df['SYMBOL'] = _var_df['SYMBOL_x']
        _var_df['AF'] = _var_df['AF_x']
        # ### 匹配提取信息 ###
        # _var_chr = _var_df['Allele'].str.extract('(?P<chr>chr.*):\d+:.*', expand=True)
        # _var_ref = _var_df['Allele'].str.extract('chr.*:\d+:(?P<ref>.*):.*', expand=True)
        # _var_alt = _var_df['Allele'].str.extract('chr.*:\d+:.*:(?P<alt>.*)', expand=True)
        # _var_num = _var_df['HGVSc_x'].str.extract('.*:.*\.(?P<num>\d+).*', expand=True)
        # _var_pnum = _var_df['HGVSp_x'].str.extract('.*\..*(?P<pnum>\d+).*', expand=True)
        # _var_pref = _var_df['HGVSp_x'].str.extract('.*\.(?P<pref>.*)\d+.*', expand=True)
        # _var_palt = _var_df['HGVSp_x'].str.extract('.*\..*\d+(?P<palt>.*)', expand=True)
        #
        # _var_df.insert(loc=len(_var_df.columns), column='chr', value=_var_chr['chr'])

        if _var_df.shape[0]==0:
            _var_df["基因描述"]=""
            _var_df["变异描述"]=""
        else:
            Gene_description_1 = partial(Gene_description,database=self._gene_description)
            #Var_description_1 = partial(Var_description,database=self._var_description)
            _var_df["基因描述"]=_var_df['SYMBOL_x'].apply(Gene_description_1)

            Var_description_1 = partial(Var_description, result=_var_df, NCCN_database=self._nccn_database,
                                        clinicaltrails_database=self._clinicaltrils_database,
                                        cancer = self._cancer)
            _var_df["变异描述"] = _var_df['Allele'].apply(Var_description_1)

            # Var_description_1 = '位于{2}号外显子上的第{35}位核苷酸{C}突变为核苷酸{T}，导致相应蛋白质序列中第{12}位氨基酸甘氨酸({G})\
            # 突变为天冬氨酸({D})，此突变在样本中的突变丰度为{47.72}%。\n{一项已经完成的Ⅲ期临床试验针对结肠癌中LN比率与KRAS表达的临床影响\
            # 进行了研究[NCT04342676]。一项已终止的Ⅰ期\Ⅱ期临床试验针对JI-101在晚期低度内分泌肿瘤、卵巢癌或KRAS突变结肠癌患者中的影响\
            # 进行了研究[NCT01149434]。NCCN指南指出，对于携带KRAS（exon2，3，4）基因突变、或NRAS（exon2，3，4）基因突变、或BRAF \
            # V600E的转移性结直肠癌患者可能对西妥昔单抗或帕尼单抗耐药。}'
            # _var_df["变异描述"]=_var_df.apply(Var_description_1,axis=1)
            #_var_df["变异描述"] = ""

        ###添加预后结果###
        prognosis_re = pd.read_excel(self._prognosis, header=0)
        #prognosis_re.rename(columns={'Unnamed: 0':'SYMBOL'}, inplace = True)
        prognosis_df = prognosis_re.loc[:, ['Gene', self._cancer]]
        prognosis_df.columns = ['SYMBOL', 'prognosis']
        df2 = pd.merge(_var_df, prognosis_df, how='left', on='SYMBOL')
        _var_df = df2
        #_var_df.to_csv('level1_tmp.txt', sep='\t', index=False)
        # group = ['耐药','敏感','基因描述','变异描述','SYMBOL','证据等级']
        # _var_df['AF'] = _var_df['AF'].astype(str)
        # _var_df_1 = _var_df.groupby(group)['Allele'].apply(ab)
        # _var_df_2 = _var_df.groupby(group)['mutation'].apply(ab)
        # _var_df_3 = _var_df.groupby(group)['AF'].apply(ab)
        # _var_df_4 = _var_df.groupby(group)['HGVSc_x'].apply(ab)
        # _var_last = pd.concat([_var_df_1,_var_df_2,_var_df_3,_var_df_4],axis=1)
        _var_df= _var_df.reset_index()
        _var_df["Index"] =_var_df["Allele"]
        self._var_dict = get_return_dict(_var_df)

        #重新提取证据等级等内容
        for key1 in self._var_dict.keys():
            tmp_zjmgny = []
            tmp_mg = []
            tmp_ny = []
            _var_tmp = _var_df[_var_df['Allele'] == key1]
            _var_tmp = _var_tmp.reset_index()
            for i in range(_var_tmp.shape[0]):
                zj = _var_tmp.loc[i, '证据等级']
                mg = _var_tmp.loc[i, '敏感']
                ny = _var_tmp.loc[i, '耐药']
                tmp_dict = {'证据等级':zj, '敏感': mg, '耐药': ny}
                # mg_dict = {'敏感': mg}
                # ny_dict = {'耐药': ny}
                tmp_zjmgny.append(tmp_dict)
                # tmp_zjmgny.append(mg_dict)
                # tmp_zjmgny.append(ny_dict)
            self._var_dict[key1]['证据敏感耐药'] = tmp_zjmgny
            # self._var_dict[key1]['敏感'] = tmp_mg
            # self._var_dict[key1]['耐药'] = tmp_ny

        #df转化为字典
        # for i in _var_list:
        #         self._var_dict[i]["基因描述"]  = Gene_description(self._var_dict[i]["SYMBOL"],self._gene_description)
        #         self._var_dict[i]["变异描述"]  = Var_description(self._var_dict[i],self._var_description)
        try:
            if isinstance(self._var_dict,dict) == False:
                raise ValueError("level1_var字典格式错误")
            else:
                return self._var_dict
        except ValueError as e:
            print("引发异常：",repr(e))
if __name__== "__main__":
    var = PcGet_level1_var()
    var.maf = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试数据/诺禾数据/MAF测试/SP20308W01.output_tnscope.filter.maf.oncokb_out"
    var.report = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试数据/诺禾数据/Sample_tumorSP20308W01.Analyses.xls"
    var.gene_list = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/dependent/gene_lists/641_genelist.xlsx"
    var.durg_name_database = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/dependent/durgs/药物名称.xlsx"
    var.gene_description = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/dependent/database/oncokb.gene.des翻译文档_待校正.sle.xlsx"
    var.var_description = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/dependent/database/变异注释数据库2021_11_10.xlsx"
    var.var_dict
    tpl = DocxTemplate("/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/新建文件夹/模板_1.docx")
    context = {"level1_var_dict":var.var_dict.values(),
               "level1_var_number":var.number}
    tpl.render(context)
    set_of_variables = tpl.get_undeclared_template_variables()
    tpl.save("/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/新建文件夹/test1.docx")
