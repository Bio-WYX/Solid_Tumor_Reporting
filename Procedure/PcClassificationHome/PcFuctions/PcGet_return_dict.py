import pandas as pd
def get_return_dict(df):
    """返回字典

    Args:
        df (dataframe): 变异位点dataframe

    Returns:
        dict: 将变异位点dataframe转换为字典
    """
    df = df.fillna("--")
    df["Index"] = df["Allele"].copy()
    df.set_index(["Index"],inplace=True)
    return_dict = df.T.to_dict()
    return return_dict