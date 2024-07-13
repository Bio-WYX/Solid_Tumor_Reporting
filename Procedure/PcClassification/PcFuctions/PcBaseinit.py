import sys
sys.path.append("/data/autoReportV2/")
sys.path.append("/data/autoReportV2/reporter/guanhaowen/pan_cancer/pc/")
from PcClassification.PcFuctions.PcGet_protein_id import get_protein_id
from PcClassification.PcFuctions.PcGet_maf import PcGet_maf
from PcClassification.PcFuctions.PcFilter_level3 import PcFilter_level3
import pandas as pd
from numpy import NAN, NaN, nan
class PcBaseinit():
    """从注释结果初步过滤
    """
    def __init__(self,report,MAF):
        """从注释结果初步过滤

        Args:
            report (xlsx): vep注释结果
            MAF (maf): oncokb注释结果
        """
        self.report = pd.read_excel(report,sheet_name="variant")
        #读取注释结果。
        self.report["HGVSp"] = self.report["HGVSp"].apply(get_protein_id)
        self.report = self.report[self.report["HGVSp"]!='']
        # self.report.dropna(subset=['HGVSp'],inplace=True)
        #提取HGVSp名称。
        self.report["mutation"] = self.report["SYMBOL"] + "-" + self.report["HGVSp"]
        #提取基因名和HGVSp结合的mutation名称。
        self.report["AF"] = self.report["AlterRatio(%)"]
        #提取AF作为突变频率。
        self.report["support_reads"] = (self.report["AF"]*self.report["CoverageDepth"])/100
        #提取变异位点支持的reads数。
        self.maf = PcGet_maf(MAF)
        #提取oncokb注释结果信息
    def get_classified(self,level):
        """返回过滤后的dataframe

        Args:
            level (int): 需要分级的变异等级

        Returns:
            dataframe: 分级后的变异位点dataframe
        """
        if level == 1 :
            classified = pd.merge(self.report,self.maf,on=["mutation"],how='inner')
            classified = classified[classified["support_reads"] > 10]
            classified = classified[(classified["LEVEL_1"]!=NaN) | (classified["LEVEL_2"]!=NaN) | (classified["LEVEL_R1"]!=NaN) | (classified["LEVEL_3A"]!=NaN)]
            classified.drop_duplicates(subset='mutation',keep='first',inplace=False,ignore_index=True)
        elif level == 2 :
            classified = pd.merge(self.report,self.maf,on=["mutation"],how='inner')
            classified = classified[classified["support_reads"] > 10]
            classified = classified[((classified["LEVEL_3B"]!=NaN) | (classified["LEVEL_4"]!=NaN) | (classified["LEVEL_R2"]!=NaN)) & (classified["LEVEL_1"]==NaN)]
        elif level == 3 :
            classified = pd.merge(self.report,self.maf,on=["mutation"],how='outer')
            classified = classified[classified["support_reads"] > 10]
            classified = classified[(classified["HIGHEST_LEVEL"] != "LEVEL_1") & (classified["HIGHEST_LEVEL"] != "LEVEL_1") & (classified["HIGHEST_LEVEL"] != "LEVEL_2") & (classified["HIGHEST_LEVEL"] != "LEVEL_3A") &(classified["HIGHEST_LEVEL"] != "LEVEL_3B") &(classified["HIGHEST_LEVEL"] != "LEVEL_4") & (classified["HIGHEST_LEVEL"] != "LEVEL_R1") & (classified["HIGHEST_LEVEL"] != "LEVEL_R2")]
            classified.drop_duplicates(subset='mutation',keep='first',inplace=False,ignore_index=True) 
            classified = classified[(classified["ClinVar_CLNSIG"] != "Benign") & (classified["ClinVar_CLNSIG"] != "Likely benign") & (classified["ClinVar_CLNSIG"] != "-") & (classified["ClinVar_CLNSIG"] != "Benign/Likely benign")]
            classified = PcFilter_level3(classified)
        elif level == all :
            classified = pd.merge(self.report,self.maf,on=["mutation"],how='outer')
            classified = classified[classified["support_reads"] > 10]
            classified.drop_duplicates(subset='mutation',keep='first',inplace=False,ignore_index=True) 
        return classified

