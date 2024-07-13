import pandas as pd
import sys
sys.path.append("/data/autoReportV2/")
sys.path.append("/data/autoReportV2/reporter/guanhaowen/pan_cancer/pc/")
from ar.db.WtDatabaseInstance import db
def PcGet_disease(element,gene_list_ycyg):
    """获取遗传易感基因相关疾病函数

    Args:
        gene_list_ycyg ([type]): 遗传易感基因相关变异
        element ([type]): 变异位点

    Returns:
        [type]: 疾病
    """
    array_db = db.get_table(gene_list_ycyg, '遗传易感').get()
    df = pd.DataFrame(array_db)
    #df = pd.read_excel(gene_list_ycyg,sheet_name='遗传易感')
    df = df.drop(columns=['所有基因'])
    disease = ""
    for i in df.columns:
        if (element in df[i].values) == True:
            disease = disease+ " " + i 
        else:
            disease = disease
    return disease