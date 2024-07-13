import pandas as pd
def PcFilter_level3(df):
    """过滤三级变异

    Args:
        df (dataframe): 三级变异位点dataframe

    Returns:
        dataframe: 过滤后的三级变异位点dataframe
    """
    df = df[df["Gnomad_AF_POPMAX"]<0.01]
    df = df[df["CoverageDepth"]>4]
    df["readsnum"] = (df["AlterRatio(%)"] * df["CoverageDepth"])/100
    df = df[df["readsnum"]>10]
    df = df[df["Consequence"]!="upstream_gene_variant"]
    df = df[df["Consequence"]!="downstream_gene_variant"]
    df = df[df["Consequence"]!="3_prime_UTR_variant"]
    df = df[df["Consequence"]!="5_prime_UTR_variant"]
    df["dbscSNV_ada_score"] = df["dbscSNV_ada_score"].replace("-",0)
    df["dbscSNV_rf_score"] = df["dbscSNV_rf_score"].replace("-",0)
    df = df[(df["Consequence"]!="intron_variant")]
    df = df[(df["Consequence"]!="synonymous_variant")]
    df = df[(df["Consequence"]!="splice_region_variant")]
    df = df[df["AlterRatio(%)"]>1]
    df = df[df['ClinVar_CLNSIG']!='Benign/Likely benign']
    df = df[df['ClinVar_CLNSIG']!='Likely benign']
    df = df[df['ClinVar_CLNSIG']!='Benign']
    return df