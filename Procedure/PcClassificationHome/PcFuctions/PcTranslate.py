import pandas as pd
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
        df = pd.read_excel(DURG_NAME_DATABASE)
        wordDict = df.set_index(["英文名称"])["中文名称"].to_dict()
        cn_durg = self.multipleReplace(en_durg,wordDict)
        # print(cn_durg)
        return cn_durg
    def translate_clinvar(self,en_clinvar,DURG_NAME_DATABASE):
        en_clinvar = str(en_clinvar)
        df = pd.read_excel(DURG_NAME_DATABASE,sheet_name="CLNSIG_dict")
        wordDict = df.set_index(["ClinVar_CLNSIG"])["CN_CLNSIG"].to_dict()
        cn_clinvar = self.multipleReplace(en_clinvar,wordDict)
        return cn_clinvar
    def translate_consequence(self,en_consequence,DURG_NAME_DATABASE):
        en_consequence = str(en_consequence)
        df = pd.read_excel(DURG_NAME_DATABASE,sheet_name="Consequence_dict")
        wordDict = df.set_index(['SO_term'])['翻译'].to_dict()
        cn_consequence = self.multipleReplace(en_consequence,wordDict)
        return cn_consequence