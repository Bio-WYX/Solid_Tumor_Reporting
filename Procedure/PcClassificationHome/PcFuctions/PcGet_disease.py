import pandas as pd 
def PcGet_disease(element,gene_list_ycyg):
    """获取遗传易感基因相关疾病函数

    Args:
        gene_list_ycyg ([type]): 遗传易感基因相关变异
        element ([type]): 变异位点

    Returns:
        [type]: 疾病
    """
    df = pd.read_excel(gene_list_ycyg,sheet_name='遗传易感')
    df = df.drop(columns=['所有基因'])
    disease = ""
    for i in df.columns:
        if element in df[i].values:
            disease = disease+ " " + i 
        else:
            disease = disease
    return disease