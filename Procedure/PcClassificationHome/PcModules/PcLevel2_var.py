import sys
sys.path.append("/data/auto_reporter_V2/reporter/guanhaowen/pan_cancer/pc")
from functools import partial
import pandas as pd 
from PcClassificationHome.PcFuctions.PcTranslate import Translate
from PcClassificationHome.PcFuctions.PcGet_envidence_proof import get_envidence_proof
from PcClassificationHome.PcFuctions.PcGet_sensetive import get_sensetive
from PcClassificationHome.PcFuctions.PcGet_return_dict import get_return_dict 
from PcClassificationHome.PcFuctions.PcDescription import Gene_description,Var_description
from PcClassificationHome.PcFuctions.PcBaseinit import PcBaseinit
from PcClassificationHome.PcFuctions.PcAb import ab
from PcClassificationHome.PcModules.PcBaseclassify import PcBaseclassify
from docxtpl import DocxTemplate,InlineImage
import configparser
import datetime
from docx.shared import Mm
pd.set_option('mode.chained_assignment', None)
class PcGet_level2_var(PcBaseclassify):
    def __init__(self):
        super(PcGet_level2_var, self).__init__()

    @property
    def number(self):
        try:
            self._classified = PcBaseinit(self._report,self._maf).get_classified(2)
            self._number = len(self._classified["Allele"].drop_duplicates(keep='first',inplace=False).index.values) 
            if isinstance(self._number,int) == False:
                raise ValueError("变异个数应为int")
            else:
                return self._number
        except ValueError as e:
            print("引发异常：",repr(e))
    
    @property
    def var_dict(self):
        """获取二级变异字典
        """
        _var_df = PcBaseinit(self._report,self._maf).get_classified(2)
        #_var_df.to_excel('report_maf.xlsx', index = False)
        #二级变异去重 
        _var_df["证据等级"] = _var_df["HIGHEST_LEVEL"].apply(get_envidence_proof) 
        #转换ACMG证据等级
        _var_df["敏感"] = _var_df.apply(get_sensetive,axis=1)
        #获得敏感靶向用药
        translate_durg = partial(Translate().translate_durg,DURG_NAME_DATABASE=self.durg_name_database)
        _var_df["敏感"] = _var_df["敏感"].apply(translate_durg)
        #翻译药物名称
        _var_df["耐药"] = _var_df["LEVEL_R2"].fillna("无").astype(str).apply(translate_durg)
        #_var_df.to_excel('report_maf.zjmgny.xlsx', index=False)
        #翻译药物名称
        #_var_df_only = _var_df[["mutation","EXON","SYMBOL","AF","证据等级","敏感","耐药","MUTATION_EFFECT_CITATIONS"]] 
        #保留必要信息
        _var_df['SYMBOL'] = _var_df['SYMBOL_x']
        _var_df['AF'] = _var_df['AF_x']
        # _var_list = _var_df["Allele"].values 
        if _var_df.shape[0]==0:
            _var_df["基因描述"]=""
            _var_df["变异描述"]="-"
        else:
            Gene_description_1 = partial(Gene_description,database=self._gene_description)
            #Var_description_1 = partial(Var_description,database=self._var_description)
            #_var_df["基因描述"]=_var_df['SYMBOL_x'].apply(Gene_description_1)
            #_var_df["变异描述"]=_var_df.apply(Var_description_1,axis=1)
            _var_df["基因描述"] = _var_df['SYMBOL'].apply(Gene_description_1)

            Var_description_1 = partial(Var_description, result=_var_df,
                                        NCCN_database=self._nccn_database,
                                        clinicaltrails_database=self._clinicaltrils_database,
                                        cancer = self._cancer)
            _var_df["变异描述"] = _var_df['Allele'].apply(Var_description_1)

        _var_df["变异描述"] = _var_df["变异描述"].str.replace("nan","")
        # _var_df["突变说明"] = _var_df.apply()

        ###添加预后结果###
        prognosis_re = pd.read_excel(self._prognosis, header=0)
        prognosis_df = prognosis_re.loc[:, ['Gene', self._cancer]]
        prognosis_df.columns = ['SYMBOL', 'prognosis']
        df2 = pd.merge(_var_df, prognosis_df, how='left', on='SYMBOL')
        _var_df = df2
        #_var_df.to_csv('level2_tmp.txt', sep = '\t', index = False)
        _var_df= _var_df.reset_index()
        _var_df["Index"] =_var_df["Allele"]
        self._var_dict = get_return_dict(_var_df)

        # 重新提取证据等级等内容
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
                tmp_dict = {'证据等级': zj, '敏感': mg, '耐药': ny}
                # mg_dict = {'敏感': mg}
                # ny_dict = {'耐药': ny}
                tmp_zjmgny.append(tmp_dict)
                #tmp_zjmgny.append({'证据等级': '测试证据', '敏感': '测试敏感', '耐药': '测试耐药'})
                #tmp_zjmgny.append(self._var_dict.values())
                # tmp_zjmgny.append(mg_dict)
                # tmp_zjmgny.append(ny_dict)
            self._var_dict[key1]['证据敏感耐药'] = tmp_zjmgny
            # self._var_dict[key1]['敏感'] = tmp_mg
            # self._var_dict[key1]['耐药'] = tmp_ny

        try:
            if isinstance(self._var_dict,dict) == False:
                raise ValueError("level2_var字典格式错误")
            else:
                return self._var_dict
        except ValueError as e: 
            print("引发异常：",repr(e))
if __name__ == '__main__':
    var = PcGet_level2_var()
    var.maf = "/data/download/lis/report/王月星/2023-05-30/40434/9175f10defc0d5fe3fc9d1ec2de8e33d.maf.clean.oncokb_out"
    var.report = "/data/download/lis/report/王月星/2023-05-30/40434/336f93259a4b4589c29e1b006329459b.xls"
    var.gene_list = "/data/autoReportV2/reporter/guanhaowen/database_ST/实体瘤-genelist.xlsx"
    var.durg_name_database = "/data/autoReportV2/reporter/guanhaowen/database_ST/实体瘤-药物名称.xlsx"
    var.gene_description = "/data/autoReportV2/reporter/guanhaowen/database_ST/实体瘤-Gene_description.xlsx"
    var.nccn_database = "/data/autoReportV2/reporter/guanhaowen/database_ST/实体瘤-NCCN.xlsx"
    var.clinicaltrils_database = "/data/autoReportV2/reporter/guanhaowen/database_ST/实体瘤-clinicaltrails.xlsx"
    var.prognosis = "/data/autoReportV2/reporter/guanhaowen/database_ST/实体瘤-预后计算.xlsx"
    var.cancer = "HCC"
    var.var_dict
    #tpl = DocxTemplate("/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/新建文件夹/模板_1.docx")
    context = {"level2_var_dict":var.var_dict.values(),
               "level2_var_number":var.number}
    print (context)
    #tpl.render(context)
    #set_of_variables = tpl.get_undeclared_template_variables()
    #tpl.save("/data/download/lis/report/王月星/2023-05-30/40434//test1.docx")
