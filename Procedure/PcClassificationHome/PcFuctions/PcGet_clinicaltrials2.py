import pandas as pd 
def filter_clinicaltrail_2(df):
    """过滤clinicaltrails信息

    Args:
        df ([type]): [description]

    Returns:
        [type]: [description]
    """
    
    map_1 = {"Phase 1":"I期","Phase 2":"II期","Phase 3":"III期","Phase 4":"IV期"}
    def multipleReplace(text, wordDict=map_1):
        """多重替换函数"""
        for key in wordDict:
            text = text.replace(key, wordDict[key])
        return text
    df = df.drop_duplicates(subset='NCT Number',keep='first',inplace=False,ignore_index=True)
    df = df[['type',"mutation","Phases","Conditions","Interventions","NCT Number",'SYMBOL','Locations']]
    df["Index"] = df["NCT Number"]
    df["Interventions"] = df["Interventions"].map(lambda x : x.replace("|","\n"))
    df["Interventions"] = df["Interventions"].map(lambda x : x.replace("Drug:",""))
    df["Conditions"] = df["Conditions"].map(lambda x : x.replace("|","\n"))
    df["NCT_Number"] = df["NCT Number"]
    df['Phases'] = df['Phases'].apply(multipleReplace)
    df.fillna("-")  
    df.set_index(["Index"],inplace=True)
    clinical_dict = df.T.to_dict()
    return clinical_dict