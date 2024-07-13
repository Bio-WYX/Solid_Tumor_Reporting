import pandas as pd
def PcGet_maf(MAF):
    """读取MAF文件

    Args:
        MAF (str): MAF文件地址

    Returns:
        maf: 去掉没有相关药物的变异位点后的maf
    """
    maf = pd.read_csv(MAF,sep="\t")
    maf = maf[maf["VARIANT_IN_ONCOKB"] == True]
    #去掉不在oncokb中的变异位点

    maf.dropna(subset={"HIGHEST_LEVEL"},inplace=True)
    #去掉没有致病等级和对应药物的变异位点

    maf["mutation"] = maf["Hugo_Symbol"] + "-" + maf["HGVSp"]
    #新增mutation列

    return maf