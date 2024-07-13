import pandas as pd
def get_nccn(df,db,cancer):
    df = df.fillna("--")
    df["Index"] = df["mutation"]
    df.set_index(["Index"],inplace=True)
    dict_1 = df.T.to_dict()
    _dict = {}
    if cancer == "NSCLC":
        for i in dict_1:
            if dict_1[i]["SYMBOL_x"] =="EGFR":
                if dict_1[i]["HGVSp_Short"] == "p.L858R":
                    _dict[i] = get_info(db,"EGFR","L858R")
                elif dict_1[i]["HGVSp_Short"] == "p.L861Q":
                    _dict[i] = get_info(db,"EGFR","L861Q")
                elif dict_1[i]["HGVSp_Short"] == "p.G719X":
                    _dict[i] = get_info(db,"EGFR","G719X")
                elif dict_1[i]["HGVSp_Short"] == "p.S768I":
                    _dict[i] = get_info(db,"EGFR","S768I")
                elif dict_1[i]["HGVSp_Short"] == "p.T790M":
                    _dict[i] = get_info(db,"EGFR","T790M")
                elif dict_1[i]["EXON"] == "Exon 19/28" and dict_1[i]["HGVSp_Short"].find("del") != -1:
                    _dict[i] = get_info(db,"EGFR","19号外显子缺失")
                elif dict_1[i]["EXON"] == "Exon 19/28" and dict_1[i]["HGVSp_Short"].find("ins") != -1:
                    _dict[i] = get_info(db,"EGFR","19号外显子插入")
                elif dict_1[i]["EXON"] == "Exon 19/28" and dict_1[i]["HGVSp_Short"].find("dup") != -1:
                    _dict[i] = get_info(db,"EGFR","19号外显子插入")
                elif dict_1[i]["EXON"] == "Exon 20/28" and dict_1[i]["HGVSp_Short"].find("dup") != -1:
                    _dict[i] = get_info(db,"EGFR","20号外显子插入")
                elif dict_1[i]["EXON"] == "Exon 20/28" and dict_1[i]["HGVSp_Short"].find("ins") != -1:
                    _dict[i] = get_info(db,"EGFR","20号外显子插入")
            elif dict_1[i]["SYMBOL_x"] == "KRAS" and dict_1[i]["HGVSp_Short"] == "p.G12C":
                _dict[i] = get_info(db,"KRAS","G12C")
            elif dict_1[i]["SYMBOL_x"] == "BRAF" and dict_1[i]["HGVSp_Short"] == "p.V600E":
                _dict[i] = get_info(db,"BRAF","V600E")
            elif dict_1[i]["SYMBOL_x"] == "ERBB2":
                _dict[i] = get_info(db,"ERBB2","突变")
            elif dict_1[i]["SYMBOL_x"] == "HER2": 
                _dict[i] = get_info(db,"HER2","突变")
            else:
                _dict[i] = { 
                'durg' : "-",
                'nccn_des' : "-",
                'fda_des' : "-",
                'nmpa_des' : "-"
                }
            _dict[i]['mutation'] = dict_1[i]['HGVSp_Short']
    return _dict 




def get_info(df,gene,var):
    durg = df[(df['基因'] == gene) & (df['突变位点'] == var)]["药物"].values.tolist()
    nccn_des = df[(df['基因'] == gene) & (df['突变位点'] == var)]["NCCN指南汇总"].values.tolist()
    fda_des = df[(df['基因'] == gene) & (df['突变位点'] == var)]["FDA汇总"].values.tolist()
    nmpa_des = df[(df['基因'] == gene) & (df['突变位点'] == var)]["NMPA汇总"].values.tolist()
    durg = ''.join(durg)
    nccn_des = ''.join(nccn_des)
    fda_des = ''.join(fda_des)
    nmpa_des = ''.join(nmpa_des)
    _dict = {
        "durg":durg,
        "nccn_des":nccn_des,
        "fda_des":fda_des,
        "nmpa_des":nmpa_des
            }
    return _dict
