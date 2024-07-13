import pandas as pd
def filter_clinicaltrail(df,all_db,cancer):
    """过滤clinicaltrails信息

    Args:
        df (dataframe): 临床试验数据库dataframe

    Returns:
        [type]: 过滤掉重复后的临床试验数据库dataframe
    """
    df['SYMBOL'] = df["SYMBOL_x"]
    df['EXON'] = df['EXON_x']
    cancer_dict = {'NSCLC':"肺癌",
                    'Breast Cancer':'乳腺癌',
                    'Colorectal Cancer':'结直肠癌',
                    'HCC':"肝癌",
                    "Esophagogastric Cancer":"胃癌"}
    odf = pd.DataFrame(columns={'Rank':"",
                                'NCT Number':"", 
                                'Title':"", 
                                'Status':"", 
                                'Study Results':"", 
                                'Conditions':"",
                                'Interventions':"", 
                                'Phases':"", 
                                'Locations':"", 
                                'URL':"", 
                                'Brief Summary':"",
                                'Detailed Description':"", 
                                'Gene':"", 
                                'Variation':"", 
                                'Mutation':"", 
                                'type':"",
                                'mutation':"", 
                                'SYMBOL':""})
    if cancer == 'NSCLC':
        db = pd.read_excel(all_db,sheet_name=cancer)
        for i, row in df.iterrows():
            gene = row['SYMBOL']
            var = row['HGVSp_Short']
            exon = row['EXON']
        # for row in df.itertuples():
        #     gene = getattr(row,'SYMBOL')
        #     var = getattr(row,'HGVSp_Short')
        #     exon = getattr(row,'EXON')
            if gene in ['ALK','ARAF','BRAF','MAP2K1','CDKN2A','FGFR1','FGFR2', 'FGFR3','KRAS','MTOR','NF1','PTEN','STK11','ROS1']:
            # if gene != 'EGFR':
                if db[db['Gene'] == gene].shape[0]==0:
                    odf = get_solid_tumor(gene, all_db, var, odf)
                    #pass
                else:
                    tmp = db[db['Gene'] == gene]
                    tmp['type']= cancer_dict[cancer]
                    tmp['mutation'] = var
                    tmp['SYMBOL'] = gene
                    odf = pd.concat([odf,tmp])
            elif gene  == 'EGFR':
                if db[db['Gene'] == gene].shape[0]==0:
                    odf = get_solid_tumor(gene, all_db, var, odf)
                    #pass
                else:
                    if (var == 'p.L858R') or (exon == 'Exon 19/28' and var.find("del") != -1):
                        tmp = db[db['NCT Number'].isin(['NCT01532089','NCT04862780'])]
                        tmp['mutation'] = var
                        tmp['SYMBOL'] = gene
                        tmp['type'] =  cancer_dict[cancer]
                        odf = pd.concat([odf,tmp])
                    elif var == 'p.T790M':
                        tmp =db[db['NCT Number'].isin(['NCT03861156',
                        'NCT03257124',
                        'NCT04862780',
                        'NCT04764214',
                        'NCT02454933'])]
                        tmp['mutation'] = var
                        tmp['SYMBOL'] = gene
                        tmp['type'] =  cancer_dict[cancer]
                        odf = pd.concat([odf,tmp])
                tmp = db[db['NCT Number'].isin(['NCT02228369',
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
                                                        ])]
                tmp['mutation'] = var
                tmp['SYMBOL'] = gene
                tmp['type'] = cancer_dict[cancer]
                odf = pd.concat([odf,tmp])
    elif cancer != 'NSCLC':
        db = pd.read_excel(all_db,sheet_name=cancer)
        for i, row in df.iterrows():
            gene = row['SYMBOL']
            var = row['HGVSp_Short']
        # for row in df.itertuples():
        #     gene = getattr(row,'SYMBOL')
        #     var = getattr(row,'HGVSp_Short')
            if db[db['Gene'] == gene].shape[0]==0:
                odf = get_solid_tumor(gene, all_db, var, odf)
                #pass
            else:
                tmp = db[db['Gene'] == gene]
                tmp['type']= cancer_dict[cancer]
                tmp['mutation'] = var
                tmp['SYMBOL'] = gene
                odf = pd.concat([odf,tmp])

    return odf

###### 所在癌种中没有检测到结果，从实体瘤中提取信息 ######
def get_solid_tumor(gene, all_db, var, odf_s):
    db_s = pd.read_excel(all_db, sheet_name='solid tumor')
    tmp_s = db_s[db_s['Gene'] == gene]
    tmp_s['type'] = '实体瘤'
    tmp_s['mutation'] = var
    tmp_s['SYMBOL'] = gene
    odf_s = pd.concat([odf_s, tmp_s])

    return odf_s
