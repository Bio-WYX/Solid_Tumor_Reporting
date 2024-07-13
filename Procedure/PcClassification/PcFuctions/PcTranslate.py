import pandas as pd
import sys
sys.path.append("/data/autoReportV2/")
sys.path.append("/data/autoReportV2/reporter/guanhaowen/pan_cancer/pc/")
from ar.db.WtDatabaseInstance import db
class Translate():
    def __init__(self) -> None:
        pass
    def multipleReplace(self,text, wordDict):
        """多重替换函数"""
        for key in wordDict:
            text = text.replace(key, wordDict[key])
        return text 
    def translate_durg(self,en_durg,DURG_NAME_DATABASE):
        en_durg = str(en_durg)
        _predb = db.get_table(DURG_NAME_DATABASE,"Sheet1").get()
        df = pd.DataFrame(_predb)
        wordDict = df.set_index(["英文名称"])["中文名称"].to_dict()
        cn_durg = self.multipleReplace(en_durg,wordDict)
        # print(cn_durg)
        return cn_durg
    def translate_clinvar(self,en_clinvar,DURG_NAME_DATABASE):
        en_clinvar = str(en_clinvar)
        _predb = db.get_table(DURG_NAME_DATABASE,"CLNSIG_dict").get()
        df = pd.DataFrame(_predb)
        wordDict = df.set_index(["ClinVar_CLNSIG"])["CN_CLNSIG"].to_dict()
        cn_clinvar = self.multipleReplace(en_clinvar,wordDict)
        return cn_clinvar
