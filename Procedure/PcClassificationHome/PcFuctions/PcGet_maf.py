import pandas as pd
def PcGet_maf(MAF):
    """读取MAF文件

    Args:
        MAF (str): MAF文件地址

    Returns:
        maf: 去掉没有相关药物的变异位点后的maf
    """
    #maf = pd.read_csv(MAF,sep="\t",encoding_errors='ignore')
    maf = pd.read_csv(MAF, sep="\t", error_bad_lines = False)
    # maf = maf[maf["VARIANT_IN_ONCOKB"] == True]
    #去掉不在oncokb中的变异位点

    maf.dropna(subset=["HIGHEST_LEVEL"],inplace=True)
    #去掉没有致病等级和对应药物的变异位点
    maf.dropna(subset=['Chromosome'],inplace=True)
    maf['Start_Position'] = maf['Start_Position'].astype(int)
    # print(maf[['Chromosome','Start_Position','Reference_Allele','Tumor_Seq_Allele2']])
    # maf["mutation"] = maf["Hugo_Symbol"] + "-" + maf["Chromosome"] +":"+ maf['Start_Position']+":"+maf['Reference_Allele']+":"+maf['Tumor_Seq_Allele1']
    # maf["mutation"] = maf["Hugo_Symbol"] + "-" + maf["HGVSp"]
    #新增mutation列
    maf['Allele'] = maf['Chromosome'].astype(str)+":"+maf['Start_Position'].astype(int).astype(str)+":"+maf['Reference_Allele'].astype(str)+":"+maf['Tumor_Seq_Allele2'].astype(str)
    #新增Allele列
    return maf
if __name__== "__main__":
    maf = "D:/肿瘤产品调研/测试数据/诺禾数据/SP20308W01.output_tnscope.filter.clean.maf.oncokb_out"
    print(PcGet_maf(maf)['mutation'])