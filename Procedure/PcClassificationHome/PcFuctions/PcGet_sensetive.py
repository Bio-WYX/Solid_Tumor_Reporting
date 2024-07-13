import pandas as pd
from numpy import nan
def get_sensetive(df):
    sensetive=""
    """获得敏感靶向用药

    Args:
        df (dataframe): 有药物靶点的变异位点dataframe

    Returns:
        series: 为有药物靶点的dataframe添加一列信息：是否对药物敏感
    """
    if df.shape[0] == 0:
        sensetive = "无"
    else:
        if pd.notna(df.LEVEL_1)==True:
            sensetive = df.LEVEL_1
        if pd.notna(df.LEVEL_2)==True:
            sensetive = sensetive + df.LEVEL_2
        if pd.notna(df.LEVEL_3A)==True:
            sensetive = sensetive + df.LEVEL_3A
        if pd.notna(df.LEVEL_3B)==True:
            sensetive = sensetive + df.LEVEL_3B
        if pd.notna(df.LEVEL_4)==True:
            sensetive = sensetive + df.LEVEL_4
        if pd.notna(df.LEVEL_R1)==True:
            sensetive = sensetive
        if pd.notna(df.LEVEL_R2)==True:
            sensetive = sensetive
    return sensetive
        