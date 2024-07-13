import pandas as pd 
import json
def get_clean_fusion(fusion_json_file):
    df = pd.DataFrame()
    df["Fusion"] = ""
    df["position"] = ""
    _index = 0
    with open(fusion_json_file,'r',encoding='utf-8') as _load_f:
                _load_dict = json.load(_load_f)
    for fusion in  _load_dict['fusions'].values():
        left = fusion["left"]["gene_name"].split("_")[0]
        right = fusion["right"]["gene_name"].split("_")[0]
        if left == right:
            fusion_name = left + "-intragenic" 
        else:
            fusion_name = left + "-" + right 
        left_pos = fusion["left"]["gene_chr"] + ":" + str(fusion['left']["position"]).replace("-","")
        right_pos = fusion['right']['gene_chr'] + ":" + str(fusion['right']["position"]).replace("-","")
        _dict = {"Fusion":fusion_name,
                 "position":left_pos+"; "+right_pos}
        ser = pd.DataFrame(data=_dict,index=[_index])
        _index = _index +1
        df = pd.concat([df,ser])
    df["Tumor_Sample_Barcode"] = "TUMOR"
    df = df[["Tumor_Sample_Barcode","Fusion","position"]]
    df.to_csv(fusion_json_file +".clean",sep="\t",index=None)
    return 
if __name__ == '__main__':       
    test = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试数据/诺禾数据/MAF测试/SP20308W01.fusion.json"           
    df = get_clean_fusion(test)
             