import pandas as pd
import sys
sys.path.append("/data/autoReportV2/")
sys.path.append("/data/autoReportV2/reporter/guanhaowen/pan_cancer/pc/")
from PcClassification.PcFuctions.PcAb import ab
def get_clean_immu(df):
    """过滤免疫位点

    Args:
        df (dataframe): 免疫位点dataframe

    Returns:
        df (dataframe): 过滤后
    """
    df = df.fillna("--")
    df = df.drop_duplicates(subset='mutation',keep='first',inplace=False,ignore_index=True)
    df = df.groupby(['基因','临床解释','参考文献'])['mutation'].apply(ab)
    df = df.reset_index()
    df["Index"] = df["mutation"]
    df.set_index(["Index"],inplace=True)
    return df