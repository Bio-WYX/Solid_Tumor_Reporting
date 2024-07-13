import sys
sys.path.append("D:\肿瘤产品调研\测试模板\pan_cancer\pc")
from PcClassificationHome.PcFuctions.PcGet_protein_id import get_protein_id
from PcClassificationHome.PcFuctions.PcGet_maf import PcGet_maf
from PcClassificationHome.PcFuctions.PcFilter_level3 import PcFilter_level3
import pandas as pd
class PcDisease():
    """从注释结果初步过滤
    """
    def __init__(self,result,MAF):
        """解析过滤解读结果

        Args:
            result (xlsx): 医学部解读结果
            MAF (maf): oncokb注释结果
        """
        self.result = pd.read_excel(result,sheet_name="variant")
        self.result.dropna(axis=0, subset=["致病性"])
        #self.result = self.result[self.result['FILTER']=="PASS"]
        self.result["HGVSp"] = self.result["HGVSp"].apply(get_protein_id)
        self.result["mutation"] = self.result["SYMBOL"] + "-" + self.result["HGVSp"]
        self.result["AF"] = self.result["AlterRatio(%)"]
        self.result["support_reads"] = (self.result["AF"]*self.result["CoverageDepth"])/100
        self.maf = PcGet_maf(MAF)
        # self.report = pd.read_excel(report,sheet_name="variant")
        # #读取注释结果。
        # self.report["HGVSp"] = self.report["HGVSp"].apply(get_protein_id)
        # self.report = self.report[self.report["HGVSp"]!='']
        # # self.report.dropna(subset=['HGVSp'],inplace=True)
        # #提取HGVSp名称。
        # self.report["mutation"] = self.report["SYMBOL"] + "-" + self.report["HGVSp"]
        # #提取基因名和HGVSp结合的mutation名称。
        # self.report["AF"] = self.report["AlterRatio(%)"]
        # #提取AF作为突变频率。
        # self.report["support_reads"] = (self.report["AF"]*self.report["CoverageDepth"])/100
        # #提取变异位点支持的reads数。
        # self.maf = PcGet_maf(MAF)
        # #提取oncokb注释结果信息
    def get_disease(self):
        pass
    # def get_classified(self,level):
    #     """返回过滤后的dataframe
    #
    #     Args:
    #         level (int): 需要分级的变异等级
    #
    #     Returns:
    #         dataframe: 分级后的变异位点dataframe
    #     """
    #     if level == 1 :
    #         cdf = pd.merge(self.report,self.maf,on=["Allele"],how='inner')
    #         cdf = cdf[cdf["support_reads"] > 10]
    #         cdf_1 = cdf[cdf["LEVEL_1"].notna()==True]
    #         cdf_2 = cdf[cdf["LEVEL_2"].notna()==True]
    #         cdf_R1 = cdf[cdf["LEVEL_R1"].notna()==True]
    #         cdf_3A = cdf[cdf["LEVEL_3A"].notna()==True]
    #         cdf_last = pd.concat([cdf_1,cdf_2,cdf_R1,cdf_3A])
    #         cdf_last.drop_duplicates(subset='Allele',keep='first',inplace=True,ignore_index=True)
    #     elif level == 2 :
    #         cdf = pd.merge(self.report,self.maf,on=["Allele"],how='inner')
    #         cdf = cdf[cdf["support_reads"] > 10]
    #         cdf_1 = cdf[cdf["LEVEL_1"].notna()==True]
    #         cdf_2 = cdf[cdf["LEVEL_2"].notna()==True]
    #         cdf_R1 = cdf[cdf["LEVEL_R1"].notna()==True]
    #         cdf_3A = cdf[cdf["LEVEL_3A"].notna()==True]
    #         cdf_3B = cdf[cdf["LEVEL_3B"].notna()==True]
    #         cdf_4 = cdf[cdf["LEVEL_4"].notna()==True]
    #         cdf_R2 = cdf[cdf["LEVEL_R2"].notna()==True]
    #         cdf_level2 = pd.concat([cdf_3B,cdf_4,cdf_R2])
    #         cdf_level1 = pd.concat([cdf_1,cdf_2,cdf_R1,cdf_3A])
    #         cdf_last = pd.concat([cdf_level2,cdf_level1,cdf_level1]).drop_duplicates(keep=False)
    #
    #         cdf_last.drop_duplicates(subset='Allele',keep='first',inplace=True,ignore_index=True)
    #         cdf_last = cdf_last[~((cdf_last['Consequence_x']== "splice_region_variant; intron_variant") & (cdf_last['ClinVar']=="-") & (cdf_last['HGMD']=="-"))]
    #         # cdf_last.drop_duplicates(subset='mutation',keep='first',inplace=False,ignore_index=True)
    #         blacklist = ["NM_000051:c.6975+13dup",
    #                      "NM_000051:c.8608del",
    #                      "NM_000368:c.2626-4dup",
    #                      "NM_000368:c.2626-5_2626-4dup",
    #                      "NM_000368:c.2626-6_2626-4dup",
    #                      "NM_000368:c.2626-3C>T",
    #                      "NM_000368:c.2626-4del",
    #                      "NM_000368:c.2626-5_2626-4del",
    #                      "NM_000368:c.2626-6_2626-4del",
    #                      "NM_000267:c.3198-3C>A",
    #                      "NM_000267:c.7258+3A>G",
    #                      "NM_001114121:c.676dup",
    #                      "NM_001114121:c.667G>T",
    #                      "NM_001321809:c.316-2_316del",
    #                      'NM_000368:c.2626-3_2626-2insTA',
    #
    #
    #
    #                     ]
    #         cdf_last = cdf_last[~cdf_last["HGVSc_x"].isin(blacklist)]
    #     elif level == 3 :
    #         cdf = pd.merge(self.report,self.maf,on=["Allele"],how='outer')
    #         cdf = cdf[cdf["support_reads"] > 10]
    #         cdf = cdf[~cdf["HIGHEST_LEVEL"].isin(["LEVEL_1",
    #                                                                   "LEVEL_2",
    #                                                                   "LEVEL_3A",
    #                                                                   "LEVEL_3B",
    #                                                                   "LEVEL_4",
    #                                                                   "LEVEL_R1",
    #                                                                   "LEVEL_R2"])]
    #         # cdf.drop_duplicates(subset='mutation',keep='first',inplace=False,ignore_index=True)
    #         cdf.drop_duplicates(subset='Allele',keep='first',inplace=True,ignore_index=True)
    #         cdf = cdf[~cdf["ClinVar_CLNSIG"].isin(["Benign",
    #                                                                     "Likely benign",
    #                                                                     "Benign/Likely benign"])]
    #         cdf_last = PcFilter_level3(cdf)
    #     elif level == all :
    #         cdf = pd.merge(self.report,self.maf,on=["Allele"],how='outer')
    #         cdf_last = cdf[cdf["support_reads"] > 10]
    #         # cdf_last.drop_duplicates(subset='mutation',keep='first',inplace=False,ignore_index=True)
    #         cdf_last.drop_duplicates(subset='Allele',keep='first',inplace=True,ignore_index=True)
    #     return cdf_last
# if __name__== "__main__":
#     report = "D:/肿瘤产品调研/测试数据/诺禾数据/Sample_tumorGHL.Analyses.xls"
#     maf = "D:/肿瘤产品调研/测试数据/诺禾数据/GHL.output_tnscope.filter.clean.maf.oncokb_out"
#     var = PcBaseinit(report,maf).get_cdf(4)
#     print(var['HIGHEST_LEVEL'])
    
    