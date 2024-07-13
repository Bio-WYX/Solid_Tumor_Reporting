import pandas as pd 
def PcClinical(path,mode):
    """生成oncokb api 注释所需的clincial文件

    Args:
        path (str): 文件路径
        mode (int): mode号
    """
    dict_1 = {357:"Breast Cancer",
              362:"Breast Cancer",
              358:"Colorectal Cancer",
              363:"Colorectal Cancer",
              359:"NSCLC",
              364:"NSCLC",
              360:"HCC",
              365:"HCC",
              361:"EGC",
              366:"EGC"}
    onco_id = dict_1[mode]

    d = {"SAMPLE_ID":["TUMOR"],"ONCOTREE_CODE":[onco_id]}
    df = pd.DataFrame(data=d)
    df.to_csv(path,sep="\t",index=None)

