import pandas as pd
import sys
sys.path.append("/data/autoReportV2/")
sys.path.append("/data/autoReportV2/reporter/guanhaowen/pan_cancer/pc/")
from ar.db.WtDatabaseInstance import db
def Gene_description(gene,database):
    #_df = pd.read_excel(database,sheet_name="基因描述")
    array_db = db.get_table(database, "基因描述").get()
    _df = pd.DataFrame(array_db)
    _description = _df[_df['基因'] == gene]["基因描述"].values.tolist()
    _description = ''.join(_description)
    return _description
def Var_description(var,database):
    #_df = pd.read_excel(database,sheet_name='Sheet1')
    array_db = db.get_table(database, "Sheet1").get()
    _df = pd.DataFrame(array_db)
    var["HGVSp_short"] = short_id(var["HGVSp_x"])
    if var['SYMBOL'] == "EGFR" and var['EXON'] == 'Exon 19/28' and var["mutation"].find("del") != -1:
        description = _df[(_df['gene'] == var['SYMBOL']) & (_df['var'] == 'Exon 19 deletion')]['des'].values.tolist()
    elif var['SYMBOL'] in ["CDKN2A",'ERBB2','ESR1','KRAS','FGFR1',"FGFR2","FGFR3",'MTOR','NF1','NRAS','PTEN','STK11']:
        description = _df[(_df['gene'] == var['SYMBOL']) & (_df['var'] == 'Oncogenic Mutations')]['des'].values.tolist()
    else:
        description = _df[(_df['gene'] == var['SYMBOL']) & (_df['var'] == var['HGVSp_short'])]['des'].values.tolist()
    description = ''.join(description)
    return description
    
def short_id(longid):
    _map = {
        'Phe':'F',
        'Leu':'L',
        'Ile':'I',
        'Met':'M',
        'Val':'V',
        'Ser':'S',
        'Pro':'P',
        'Thr':'T',
        'Ala':'A',
        'Tyr':'Y',
        'His':'H',
        'Gln':'Q',
        'Asn':'N',
        'Lys':'K',
        'Asp':'D',
        'Glu':'E',
        'Cys':'C',
        'Trp':'W',
        'Arg':'R',
        'Ser':'S',
        'Arg':'R',
        'Gly':'G',
        'Ter':'*'
            }
    for key in _map:
        longid = longid.replace(key, _map[key])
    shortid = longid.replace("p.","")
    return shortid


      

        