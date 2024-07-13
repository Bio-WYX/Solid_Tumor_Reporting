import contextlib
from matplotlib.pyplot import axis
import pandas as pd 
import json
import sys
sys.path.append("/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/pc")
from functools import partial
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
class PcSv(PcBaseclassify):
    """提取结构变异注释信息
    """
    def __init__(self):
        super(PcSv,self).__init__()
    
    @property
    def var_dict(self):
        if self._sv == None:
            number_1 = 0
            number_2 = 0
            _f_1 = {}
            _f_2 = {}
        else:
            #_var_df = pd.read_csv(self._sv,sep="\t",header=0,encoding_errors='ignore')
            _var_df = pd.read_csv(self._sv, sep="\t", header=0, error_bad_lines = False)
            _var_df.insert(loc=len(_var_df.columns),column='tmp',value="")
            _var_df.columns = ['Tumor_Sample_Barcode','Fusion','position','GENE_IN_ONCOKB','VARIANT_IN_ONCOKB','MUTATION_EFFECT','tmp','ONCOGENIC','LEVEL_1','LEVEL_2','LEVEL_3A','LEVEL_3B','LEVEL_4','LEVEL_R1','LEVEL_R2','LEVEL_R3','HIGHEST_LEVEL','CITATIONS','LEVEL_Dx1','LEVEL_Dx2','LEVEL_Dx3','HIGHEST_DX_LEVEL','LEVEL_Px1','LEVEL_Px2','LEVEL_Px3','HIGHEST_PX_LEVEL']
            _var_df.dropna(subset=(['HIGHEST_LEVEL']),inplace=True)  
            _var_df["证据等级"] = _var_df["HIGHEST_LEVEL"].apply(get_envidence_proof)
            _var_df["敏感"]= _var_df.apply(get_sensetive,axis=1)
            translate_durg = partial(Translate().translate_durg,DURG_NAME_DATABASE=self._durg_name_database)
            _var_df["敏感"] = _var_df["敏感"].apply(translate_durg)
            _var_df["耐药"] = _var_df["LEVEL_R1"].fillna("无").astype(str).apply(translate_durg)
            if _var_df.shape[0]==0:
                _var_df["基因描述"]=""
                _var_df["变异描述"]=""
            else:
                Gene_description_1 = partial(Gene_description,database=self._gene_description)
                Var_description_1 = partial(Fusion_description,database=self._var_description)
                _var_df["left"] = _var_df['Fusion'].str.split("-")[0][0]
                _var_df["right"] = _var_df['Fusion'].str.split("-")[0][1]
                _var_df["基因描述"]= _var_df["left"].apply(Gene_description_1) +"\n\t"+ _var_df["right"].apply(Gene_description_1)
                # _var_df["变异描述"]=_var_df.apply(Var_description_1,axis=1)
            _var_df = _var_df.fillna("--")
            _var_df['Index'] =  _var_df['Fusion'].str.cat(_var_df['position'].astype(str))
            _var_df.set_index(["Index"],inplace=True)
            _var_df_levle1 = _var_df[_var_df['证据等级'].isin(['A','B'])]
            number_1 = _var_df_levle1.shape[0]
            _var_df_levle2 = _var_df[_var_df['证据等级'].isin(['C','D'])]
            number_2 = _var_df_levle2.shape[0]
            _f_1 = _var_df_levle1.T.to_dict()
            _f_2 = _var_df_levle2.T.to_dict()
        self._var_dict = {"level_1_fusion":_f_1,
                        "level_2_fusion":_f_2,
                        "level_1_fusion_number":number_1,
                        "level_2_fusion_number":number_2}
        return self._var_dict

if __name__ == '__main__':
    var = PcSv()
    var.sv = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试数据/诺禾数据/MAF测试/SP20308W01.fusion.json.clean.oncokb_out"
    var.gene_list = "/Users/guanhaowen/Desktop/测试模板/pan_cancer/dependent/gene_lists/641_genelist.xlsx"
    var.durg_name_database = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/dependent/durgs/药物名称.xlsx"
    var.gene_description = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/dependent/database/oncokb.gene.des翻译文档_待校正.sle.xlsx"
    var.var_description = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/dependent/database/变异注释数据库2021_11_10.xlsx" 
    tpl = DocxTemplate("/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/新建文件夹/模板_1.docx")
    fusion_dict = {"level1_fusion_dict":var.var_dict['level_1_fusion'].values(),
               "level2_fusion_dict":var.var_dict['level_2_fusion'].values(),
               "level1_var_number":var.var_dict["level_1_fusion_number"],
               "level2_var_number":var.var_dict["level_2_fusion_number"]}
    context = {"fusion_dict":fusion_dict}
    tpl.render(context)
    set_of_variables = tpl.get_undeclared_template_variables()
    tpl.save("/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/新建文件夹/test1.docx")
    
