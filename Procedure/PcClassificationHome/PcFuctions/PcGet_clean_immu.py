import sys
sys.path.append("D:\肿瘤产品调研\测试模板\pan_cancer\pc")
import pandas as pd 
from PcClassificationHome.PcFuctions.PcAb import ab
def get_clean_immu(df):
    """过滤免疫位点

    Args:
        df (dataframe): 免疫位点dataframe

    Returns:
        df (dataframe): 过滤后
    """
    df = df.fillna("--")
    df = df.drop_duplicates(subset='Allele',keep='first',inplace=False,ignore_index=True)
    df1 = df.groupby(['基因','临床解释','参考文献'])['mutation'].apply(ab)
    df2 = df.groupby(['基因','临床解释','参考文献'])['Allele'].apply(ab)
    df_last = pd.concat([df1,df2],axis=1)
    df_last= df_last.reset_index()
    df_last["Index"] = df_last["Allele"]
    df_last.set_index(["Index"],inplace=True)
    return df_last