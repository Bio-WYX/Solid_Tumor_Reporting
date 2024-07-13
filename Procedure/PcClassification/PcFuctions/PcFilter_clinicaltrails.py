import pandas as pd
import sys
sys.path.append("/data/autoReportV2/")
sys.path.append("/data/autoReportV2/reporter/guanhaowen/pan_cancer/pc/")
from ar.db.WtDatabaseInstance import db
def filter_clinicaltrail(df,all_db,cancer):
    """过滤clinicaltrails信息

    Args:
        df (dataframe): 临床试验数据库dataframe

    Returns:
        [type]: 过滤掉重复后的临床试验数据库dataframe
    """
    cancer_dict = {'NSCLC':"肺癌",
                    'Breast Cancer':'乳腺癌',
                    'Colorectal Cancer':'结直肠癌',
                    'HCC':"肝癌",
                    "Esophagogastric Cancer":"胃癌"}
    odf = pd.DataFrame(columns={'Rank':"",
                                'NCT Number':"",
                                "Title":"",
                                "Status":"",
                                "Study Results":"",
                                "Conditions":"",
                                "Interventions":"",
                                "Phases":"",
                                "Locations":"",
                                "URL":"",
                                "Brief Summary":"",
                                "Detailed Description":"",
                                "Gene":"",
                                "Variation":"",
                                "mutation":"",
                                "type":""
                                })
    if cancer == 'NSCLC':
        _predb = db.get_table(all_db,cancer).get() 
        _db = pd.DataFrame(_predb)
        for row in df.itertuples():
            gene = getattr(row,'SYMBOL')
            var = getattr(row,'HGVSp_Short')
            exon = getattr(row,'EXON')
            if gene in ['ALK','ARAF','BRAF','MAP2K1','CDKN2A','FGFR1','FGFR2',
            'FGFR3','KRAS','MTOR','NF1','PTEN','STK11','ROS1']:
                odf.append(_db[_db['gene'] == gene])
                odf['mutation'] = var
                odf['SYMBOL'] = gene
                odf['type'] = cancer_dict[cancer]
            elif gene  == 'EGFR':
                if (var == 'p.L858R') or (exon == 'Exon 19/28' and var["mutation"].find("del") != -1):
                    odf = _db[_db['NCT Number'].isin(['NCT01532089','NCT04862780'])]
                    odf['mutation'] = var
                    odf['SYMBOL'] = gene
                    odf['type'] =  cancer_dict[cancer]
                elif var == 'p.T790M':
                    odf.append(_db[_db['NCT Number'].isin(['NCT03861156',
                    'NCT03257124',
                    'NCT04862780',
                    'NCT04764214',
                    'NCT02454933'])])
                    odf['mutation'] = var
                    odf['SYMBOL'] = gene
                    odf['type'] = cancer_dict[cancer]
                odf.append(_db[_db['NCT Number'].isin(['NCT02228369',
                                                        'NCT02296125',
                                                        'NCT03994393',
                                                        'NCT03396185',
                                                        'NCT02529995',
                                                        'NCT04425681',
                                                        'NCT04206072',
                                                        'NCT04001777',
                                                        'NCT03333343',
                                                        'NCT03382795',
                                                        'NCT02824458',
                                                        'NCT04636593',
                                                        'NCT04245085',
                                                        'NCT04824079',
                                                        'NCT03909334',
                                                        'NCT03239340',
                                                        'NCT04027647',
                                                        'NCT03257124',
                                                        'NCT03846310',
                                                        'NCT04233021',
                                                        'NCT02803203',
                                                        'NCT03653546',
                                                        'NCT03381066',
                                                        'NCT03046992',
                                                        'NCT03457337',
                                                        'NCT01941654',
                                                        'NCT02454933',
                                                        'NCT01203917',
                                                        'NCT04770688'
                                                        ])])
                odf['mutation'] = var
                odf['SYMBOL'] = gene
                odf['type'] = cancer_dict[cancer]
    elif cancer != 'NSCLC':
        array_db = db.get_table(all_db, cancer).get()
        _db = pd.DataFrame(array_db)
        #_db = pd.read_excel(all_db,sheet_name=cancer)
        for row in df.itertuples():
            gene = getattr(row,'SYMBOL')
            odf.append(_db[_db['gene'] == gene])  
            odf['mutation'] = var
            odf['SYMBOL'] = gene
            odf['type'] = cancer_dict[cancer]
    return odf
    