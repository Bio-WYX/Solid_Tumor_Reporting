from cmath import nan
from numpy import NaN
import pandas as pd
def get_sensetive(df):
    """获得敏感靶向用药

    Args:
        df (dataframe): 有药物靶点的变异位点dataframe

    Returns:
        series: 为有药物靶点的dataframe添加一列信息：是否对药物敏感
    """
    dict_1 = df.to_dict('records')
    if df.shape[0] == 0:
        sensetive = nan
    else:
        for i in dict_1:
            if i["LEVEL_1"] != nan:
                i['敏感'] = i["LEVEL_1"]
            elif i["LEVEL_2"] != nan:
                i['敏感'] = i["LEVEL_2"]
            elif i["LEVEL_3A"] != nan:
                i['敏感'] = i["LEVEL_3A"]
            elif i["LEVEL_3B"] != nan:
                i['敏感'] = i["LEVEL_3B"]
            elif i["LEVEL_4"] != nan:
                i['敏感'] = i["LEVEL_4"]
            elif i["LEVEL_R1"] != nan:
                i['敏感'] = ''
            elif i["LEVEL_R2"] != nan:
                i['敏感'] = ""
        sensetive = dict_1[0]['敏感']
    return sensetive

        