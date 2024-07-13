import sys
sys.path.append("/data/autoReportV2/")
sys.path.append("/data/autoReportV2/reporter/guanhaowen/pan_cancer/pc/")
from PcClassification.PcFuctions.PcFilter_immu import filter_immu
from PcClassification.PcFuctions.PcGet_clean_immu import get_clean_immu
from PcClassification.PcFuctions.PcBaseinit import PcBaseinit
from PcClassification.PcModules.PcBaseclassify import PcBaseclassify
import pandas as pd
from ar.db.WtDatabaseInstance import db

class PcImmu_var(PcBaseclassify):
    def __init__(self):
        super(PcImmu_var, self).__init__()
    
    @property
    def immu_negtive_dict(self):
        """获取免疫治疗负相关变异信息
        """
        _immu_df = PcBaseinit(self._report,self._maf).get_classified(all)
        _immu_df = filter_immu(_immu_df)
        array_db = db.get_table(self._immu_database, "免疫治疗临床意义").get()
        _immu_db = pd.DataFrame(array_db)
        #_immu_db = pd.read_excel(self._immu_database,sheet_name="免疫治疗临床意义")
        self._immu_classified = pd.merge(_immu_df,_immu_db,on=["基因"],how='inner')
        self._immu_classified.drop_duplicates(subset='mutation',keep='first',inplace=False,ignore_index=True)#去重
        self._immu_classified["Index"] = self._immu_classified["mutation"]
        self._immu_classified.set_index(["Index"],inplace=True)
        _immu_negtive = self._immu_classified[self._immu_classified["相关性"]=="负相关"]
        _immu_negtive = get_clean_immu(_immu_negtive)
        immu_negtive_dict = _immu_negtive.T.to_dict()
        return immu_negtive_dict
    
    @property
    def immu_postive_dict(self):
        """获取免疫治疗正相关变异信息
        """
        _immu_df = PcBaseinit(self._report,self._maf).get_classified(all)
        _immu_df = filter_immu(_immu_df)
        array_db = db.get_table(self._immu_database, "免疫治疗临床意义").get()
        _immu_db = pd.DataFrame(array_db)
        #_immu_db = pd.read_excel(self._immu_database,sheet_name="免疫治疗临床意义")
        self._immu_classified = pd.merge(_immu_df,_immu_db,on=["基因"],how='inner')
        self._immu_classified.drop_duplicates(subset='mutation',keep='first',inplace=False,ignore_index=True)#去重
        self._immu_classified["Index"] = self._immu_classified["mutation"]
        self._immu_classified.set_index(["Index"],inplace=True)
        _immu_postive = self._immu_classified[self._immu_classified["相关性"]=="正相关"]
        _immu_postive = get_clean_immu(_immu_postive)
        immu_postive_dict = _immu_postive.T.to_dict()
        return immu_postive_dict

    @property
    def immu_supper_dict(self):
        """获取免疫治疗超进展变异信息
        """
        _immu_df = PcBaseinit(self._report,self._maf).get_classified(all)
        _immu_df = filter_immu(_immu_df)
        array_db = db.get_table(self._immu_database, "免疫治疗临床意义").get()
        _immu_db = pd.DataFrame(array_db)
        #_immu_db = pd.read_excel(self._immu_database,sheet_name="免疫治疗临床意义")
        self._immu_classified = pd.merge(_immu_df,_immu_db,on=["基因"],how='inner')
        self._immu_classified.drop_duplicates(subset='mutation',keep='first',inplace=False,ignore_index=True)#去重
        self._immu_classified["Index"] = self._immu_classified["mutation"]
        self._immu_classified.set_index(["Index"],inplace=True)
        _immu_supper = self._immu_classified[self._immu_classified["相关性"]=="超进展"]
        _immu_supper = get_clean_immu(_immu_supper)
        immu_supper_dict = _immu_supper.T.to_dict()
        return immu_supper_dict
    
    @property
    def immu_clinicaltrials(self):
        """获取免疫治疗相关临床试验信息
        """
        array_db = db.get_table(self._immu_database, self._cancer).get()
        _df = pd.DataFrame(array_db)
        #_df = pd.read_excel(self._immu_database,sheet_name=self._cancer)
        _dict = _df.T.to_dict()
        return _dict
