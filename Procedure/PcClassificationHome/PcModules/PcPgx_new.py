from os import sep
import sys
from matplotlib.pyplot import axis
sys.path.append("/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/pc")
import pandas as pd 
import gzip
import re
import vcf
import pysam
import pybedtools
from PcClassificationHome.PcModules.PcBaseclassify import PcBaseclassify
import configparser
from docxtpl import DocxTemplate,InlineImage
import configparser
import datetime
from docx.shared import Mm
pd.set_option('mode.chained_assignment', None)
class PcPgx(PcBaseclassify):
    def __init__(self):
        super(PcPgx, self).__init__()
# def clean_allele(element):
#     a = re.match("(.*):(.*):(.*):(.*)",element)
#     chrom = a.group(1)
#     pos = a.group(2)
#     clean_allele = chrom + ":" + pos
#     return clean_allele

    def read_database(self,database):
        rs = pd.read_excel(database,sheet_name="rs")
        rs['chr'] = rs['Allele'].str.split(":",expand=True)[0]
        rs['pos'] = rs['Allele'].str.split(":",expand=True)[1]
        rs['start'] = rs['Allele'].str.split(":",expand=True)[1]
        rs['end'] = rs['Allele'].str.split(":",expand=True)[1]
        rs['ref'] = rs['Allele'].str.split(":",expand=True)[2]
        rs['alt'] = rs['Allele'].str.split(":",expand=True)[3]
        return rs

    def gvcf_df(self,gvcf):
        gvcf_df = pd.DataFrame(columns={'start':""
                                        ,'end':""
                                        ,'ref':""
                                        ,'alt':""
                                        ,'chr':""
                                        ,'heterozygosity':""
                                        ,'GT':""
                                        ,'genotype':""})
        vcf_reader = vcf.Reader(filename = gvcf)
        for record in vcf_reader:   
            if 'END' in record.INFO.keys():
                row = pd.DataFrame(data={'start':[record.POS]
                                        ,'end':[record.INFO['END']]
                                        ,'ref':[record.REF]
                                        ,'alt':[record.ALT]
                                        ,'chr':[record.CHROM]
                                        ,'heterozygosity':[record.heterozygosity]
                                        ,'GT':[record.samples[0]['GT']]
                                        ,'genotype':"纯合野生型"
                                        })
                gvcf_df = pd.concat([gvcf_df,row],axis=0,ignore_index=True)
            elif 'END' not in record.INFO.keys():
                new_GT = record.samples[0]['GT'].replace("|", "/")
                if record.heterozygosity == 0.5: #杂合
                    if new_GT.split("/")[0] == "0": #杂合型eg:(0/1)
                        ad_list = record.samples[0]['AD']
                        del ad_list[0]
                        alt = record.ALT[ad_list.index(max(ad_list))]
                        gt = str(record.REF)+str(alt)
                    else: #杂合型 eg（1/2）（2/3）
                        alt1 = int(new_GT.split("/")[0])-1
                        alt2 = int(new_GT.split("/")[1])-1
                        gt = str(record.ALT[int(alt1)])+str(record.ALT[int(alt2)])
                elif record.heterozygosity == 0: #纯合
                    if new_GT == "0/0": #纯合野生型
                        gt = record.REF+record.REF
                    else: #纯合突变型eg:(1/1) （2/2）（3/3）
                        ad_list = record.samples[0]['AD']
                        alt = record.ALT[ad_list.index(max(ad_list))-1]
                        record.samples[0]['DP']
                        gt = str(alt)+str(alt)
                row = pd.DataFrame(data={'start':[record.POS]
                                        ,'end':[record.POS + len(record.REF) -1]
                                        ,'ref':[record.REF]
                                        ,'alt':[record.ALT]
                                        ,'chr':[record.CHROM]
                                        ,'heterozygosity':[record.heterozygosity]
                                        ,'GT':[record.samples[0]['GT']]
                                        ,'genotype':gt
                                        })
                gvcf_df = pd.concat([gvcf_df,row],axis=0,ignore_index=True)
        return gvcf_df
    
    @property
    def chemo_dict(self):
        db = self.read_database(self._chemotherapy_database)
        df_all = pd.read_excel(self._chemotherapy_database,sheet_name="Pgx")
        db_bed_file = db[['chr','start','end']]
        db_bed_file.to_csv("db_bed.temp.bed",sep="\t",index=None,header=None)
        gvcf_df = self.gvcf_df(self._gvcf)
        gvcf_df_bed_file = gvcf_df[['chr','start','end']]
        gvcf_df_bed_file.to_csv("gvcf_bed.temp.bed",sep="\t",index=None,header=None)
        a = pybedtools.BedTool("db_bed.temp.bed")
        b = pybedtools.BedTool("gvcf_bed.temp.bed")
        a_and_b = a.intersect(b,wb=True)
        df = a_and_b.to_dataframe(names=['chr_db',
                                         'start_db',
                                         'end_db',
                                         'chr_gvcf',
                                         'start_gvcf',
                                         'end_gvcf',])
        db.rename(columns={'chr':'chr_db',
                           'start':'start_db',
                           'end':'end_db'},inplace=True)
        df['start_db'] = df['start_db'].astype(str)
        df['end_db'] = df['end_db'].astype(str)
        df1 = pd.merge(df,db,on=['chr_db','start_db','end_db'])
        gvcf_df.rename(columns={'chr':'chr_gvcf',
                           'start':'start_gvcf',
                           'end':'end_gvcf'},inplace=True)
        df2 = pd.merge(df1,gvcf_df,on=['chr_gvcf','start_gvcf','end_gvcf'])
        df2['基因型'] = df2.apply(self.get_GT,axis=1)
        df2 = df2[['位点','基因型']]
        group = df_all.groupby('药物')
        df_last = pd.DataFrame()
        for i in group:
            df_t = pd.merge(i[1],df2,on=['基因型','位点'])
            df_last = pd.concat([df_t,df_last],axis=0)
        df_toxic = df_last[df_last['毒副作用']=="Toxicity"]
        df_effic = df_last[df_last['功效']=="Efficacy"]
        
        group2 = df_last.groupby("药物")
        
        df_info = pd.DataFrame(columns={"药物":"",
                                        "毒性":"",
                                        "有效性":""})
        for i in group2:
            df_tmp = pd.Series()
            df_tmp["药物"] = i[0]
            #——————————————————————毒副作用汇总-----------------
            if len(i[1]['毒副作用-影响'].dropna().unique()) == 1:
                if i[1]['毒副作用-影响'].dropna().unique()[0] == "未知":
                    df_tmp["毒性"] = "/"
                else:
                    if i[1]['毒副作用-影响'].dropna().unique()[0] == "降低":
                        df_tmp["毒性"]='风险可能较低'
                    elif i[1]['毒副作用-影响'].dropna().unique()[0] == "增加":
                        df_tmp["毒性"]= '风险可能较高'
            elif len(i[1]['毒副作用-影响'].dropna().unique()) == 0:
                df_tmp["毒性"]= "/"
            else:
                counts = i[1]['毒副作用-影响'].dropna().value_counts()
                type_list = ['未知', '降低', '增加']
                nonelist = list(set(type_list).difference(set(counts.index.to_list())))
                if len(nonelist) > 0:
                    for non in nonelist:
                        counts[non]=0
                else:
                    continue                   
                if counts['增加'] == counts['降低']:
                    df_tmp["毒性"]="/"
                elif counts['增加'] > counts['降低']:
                    df_tmp["毒性"]="风险可能较高"
                elif counts['增加'] < counts['降低']:
                    df_tmp["毒性"]="风险可能较低"
            
            #----------------------有效性汇总---------------------
            if len(i[1]['功效-影响'].dropna().unique()) ==1:
                if i[1]['功效-影响'].dropna().unique()[0] == "未知":
                    df_tmp["有效性"]="/"
                else:
                    if i[1]['功效-影响'].dropna().unique()[0] == "降低":
                        df_tmp["有效性"]= "疗效可能较差"
                    elif i[1]['功效-影响'].dropna().unique()[0] == "增加":
                        df_tmp["有效性"]= "疗效可能较好"
            elif len(i[1]['功效-影响'].dropna().unique()) ==0:
                df_tmp["有效性"]="/"
            else:
                counts = i[1]['功效-影响'].dropna().value_counts()
                type_list = ['未知', '降低', '增加']
                nonelist = list(set(type_list).difference(set(counts.index.to_list())))
                if len(nonelist) > 0:
                    for non in nonelist:
                        counts[non]=0
                else:
                    pass   
                if counts['增加'] == counts['降低']:
                    df_tmp["有效性"]="/"
                elif counts['增加'] > counts['降低']:
                    df_tmp["有效性"]="疗效可能较好"
                elif counts['增加'] < counts['降低']:
                    df_tmp["有效性"]="疗效可能较差"
            
            df_info = df_info.append(df_tmp,ignore_index=True)
        df_info = df_info[~((df_info['有效性']=="/") & (df_info['毒性']=="/"))]
        df_info['检测结果'] = '谨慎使用'
        df_info.loc[(((df_info.毒性 == '风险可能较低') & (df_info.有效性 == '疗效可能较好')) | ((df_info.毒性 == '/') & (df_info.有效性 == '疗效可能较好'))), '检测结果'] = '推荐使用'
        df_info.loc[(((df_info.毒性 == '风险可能较高') & (df_info.有效性 == '疗效可能较差')) | ((df_info.毒性 == '/') & (df_info.有效性 == '疗效可能较差'))), '检测结果'] = '不推荐使用'
        df_group = df_all[['药物', '分类']]
        df_combine = pd.merge(df_info,df_group,on=['药物'])
        df_combine.drop_duplicates(subset=['药物', '毒性', '有效性', '分类'], keep='first', inplace=True)
        df_combine.sort_values(by='分类', inplace=True, ascending=False)
        df_combine['Index'] = range(df_combine.shape[0])
        df_combine.set_index(['Index'], inplace=True)

        ##################### 药物分类判断 ####################
        group_list= df_combine['分类'].unique()
        df_info_dict = {}
        for g in group_list:
            df_tmp = df_combine[df_combine['分类'] == g]
            # toxicity_good, toxicity_bad, curative_good, curative_bad, to_cu_good = 0, 0, 0, 0, 0
            # toxicity_good = df_tmp[df_tmp['毒性'] == '风险可能较低'].shape[0]
            # toxicity_bad = df_tmp[df_tmp['毒性'] == '风险可能较高'].shape[0]
            # curative_good = df_tmp[df_tmp['有效性'] == '疗效可能较好'].shape[0]
            # curative_bad = df_tmp[df_tmp['有效性'] == '疗效可能较差'].shape[0]
            # if toxicity_good > 0 or toxicity_bad > 0:
            #     toxicity_pre = toxicity_good / (toxicity_good + toxicity_bad)
            # else:
            #     toxicity_pre = 0
            # if curative_good > 0 or curative_bad > 0:
            #     curative_pre = curative_good / (curative_good + curative_bad)
            # else:
            #     curative_pre = 0
            # to_cu_good = df_tmp[(df_tmp['毒性'] == '风险可能较低') & (df_tmp['有效性'] == '疗效可能较好')].shape[0]
            # if toxicity_pre > 0.5 and curative_pre > 0.5 and to_cu_good > 0:
            #     result = '推荐使用'
            # else:
            #     result = '谨遵医嘱'
            # result_list = [''] * (df_tmp.shape[0] - 1)
            # result_list.insert(0, result)
            # df_tmp['检测结果'] = result_list
            df_info_dict_tmp = df_tmp.to_dict('records')
            df_info_dict[g] = df_info_dict_tmp

        df_toxic['Index'] = range(df_toxic.shape[0])
        df_toxic.set_index(['Index'],inplace=True)
        df_toxic_dict = df_toxic.T.to_dict()
        
        df_effic['Index'] = range(df_effic.shape[0])
        df_effic.set_index(['Index'],inplace=True)
        df_effic_dict = df_effic.T.to_dict()

        chemo_dict = {"toxic_dict":df_toxic_dict,
                   "effic_dict":df_effic_dict,
                   "info_dict":df_info_dict}
        
        return chemo_dict
    def get_GT(self,series):
        gt_dict = {
			"AA": "AA",
			"AC": "AC",
			"AG": "AG",
			"AT": "AT",
			"CA": "AC",
			"CC": "CC",
			"CG": "CG",
			"CT": "CT",
			"GA": "AG",
			"GC": "CG",
			"GG": "GG",
			"GT": "GT",
			"TA": "AT",
			"TC": "CT",
			"TG": "GT",
			"TT": "TT"
		}
        if series['genotype'] == "纯合野生型":
            GT = series['ref_x']+series['ref_x']
        elif series['genotype'] != "纯合野生型":
            GT = series['genotype']
        GT = gt_dict[GT]
        return GT

   
             
        
        
if __name__ == '__main__':
    var = PcPgx()
    var.gvcf = "/Users/guanhaowen/Desktop/pancancer_data/20220418/SP20411W03.Haplotyper.g.vcf.gz"
    var.chemotherapy_database = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/dependent/database/化疗药最终版-2022.04.07.xlsx"
    tpl = DocxTemplate("/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/新建文件夹/模板.docx")
    chemodic = {"toxic_dict":var.chemo_dict["toxic_dict"].values(),
                "effic_dict":var.chemo_dict["effic_dict"].values(),
                "info_dict":var.chemo_dict['info_dict'].values()}
    context = {"pgx_dict":chemodic}
    tpl.render(context)
    set_of_variables = tpl.get_undeclared_template_variables()
    tpl.save("/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/新建文件夹/pgx_test.docx")
