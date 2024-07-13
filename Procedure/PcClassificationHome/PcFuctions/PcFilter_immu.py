import pandas as pd
def filter_immu(df):
    """过滤免疫治疗相关位点

    Args:
        df (dataframe): 变异相关位点dataframe

    Returns:
        dataframe: 过滤后的免疫相关变异位点dataframe
    """
    df['Consequence'] = df["Consequence_x"]
    df['SYMBOL'] = df["SYMBOL_x"]
    df = df[df["Gnomad_AF_POPMAX"]<0.01]
    #人群频率小于0.01

    df = df[df["CoverageDepth"]>4]
    #测序深度大于4

    df["readsnum"] = (df["AlterRatio(%)"] * df["CoverageDepth"])/100
    df = df[df["readsnum"]>10]
    #支持reads大于10

    df = df[df["Consequence"]!="upstream_gene_variant"]
    df = df[df["Consequence"]!="downstream_gene_variant"]
    df = df[df["Consequence"]!="3_prime_UTR_variant"]
    df = df[df["Consequence"]!="5_prime_UTR_variant"]
    df["dbscSNV_ada_score"] = df["dbscSNV_ada_score"].replace("-",0)
    df["dbscSNV_rf_score"] = df["dbscSNV_rf_score"].replace("-",0)
    df = df[(df["Consequence"]!="intron_variant")]
    df = df[(df["Consequence"]!="synonymous_variant")]
    df = df[(df["Consequence"]!="splice_region_variant")]
    #筛选突变类型

    df = df[df["AlterRatio(%)"]>1]
    #突变频率大于1

    df["基因"] = df["SYMBOL"]
    # df = df[["mutation","基因"]]
    #保留mutation和基因列


    
    return df