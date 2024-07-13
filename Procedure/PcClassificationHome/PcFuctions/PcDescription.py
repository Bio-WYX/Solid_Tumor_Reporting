import re
import pandas as pd
def Gene_description(gene,database):
    tt = open('/data/download/lis/report/王月星/2023-05-30/40434/test.txt', 'w')
    tt.write('{}\n'.format(gene))
    _df = pd.read_excel(database)
    _df = _df[_df['SYMBOL'] == gene]
    _df.reset_index(inplace=True)
    _df.index = _df.index.astype(str)
    if _df.shape[0] > 0:
        if pd.isna(_df.loc['0', '校对后']):
            _description = _df.loc['0', '描述1'] + "; " + _df.loc['0', '描述2']
            _description = ''.join(_description)
        else:
            _description = _df.loc['0', '校对后']
    else:
        _description = ''
    return _description
def Var_description(var, result, NCCN_database, clinicaltrails_database, cancer):
    _re = result#pd.read_excel(result)#, sheet_name='Sheet1')
    _nc = pd.read_excel(NCCN_database, sheet_name='汇总-变异描述')
    _cl = pd.read_excel(clinicaltrails_database, sheet_name=cancer)
    _re = _re[_re['Allele'] == var]
    _re_new = _re.reset_index(drop=True)
    gene = _re_new.at[0,'SYMBOL_x']
    #_nc = _nc[_nc['SYMBOL'] == gene]

    ### 匹配提取信息 ###
    re_c = re.match('.*chr(.*):\d+:(.*):(.*)', str(_re_new.at[0,'Allele']))
    if re_c:
        re_chr = re_c.group(1)
        re_ref = re_c.group(2)
        re_alt = re_c.group(3)
    else:
        re_chr, re_ref, re_alt = '', '', ''
    re_e = re.match('.*Exon (\d+)\/(\d+)', str(_re_new.at[0, 'EXON_x']))
    if re_e:
        re_enum = re_e.group(1)
    else:
        re_enum = ''
    re_x = re.match('.*\.(\d+).*', str(_re_new.at[0, 'HGVSc_x']))
    if re_x:
        re_xnum = re_x.group(1)
    else:
        re_xnum = ''
    re_p = re.match('.*\.([A-Za-z]+)(\d+)([A-Za-z]+)', str(_re_new.at[0, 'HGVSp_x']))
    type_p = ''
    if re_p:
        re_ppos = re_p.group(2)
        re_pref = re_p.group(1)
        re_palt = re_p.group(3)
        type_p = '{}{}{}'.format(short_aa(re_pref)['s'], re_ppos, short_aa(re_palt)['s'])
    else:
        re_ppos, re_pref, re_palt = '', '', ''
    ### 变异描述 ###
    type_a = ''
    if re_ref == '-':
        result1 = f"位于{re_enum}号外显子上的第{re_xnum}位核苷酸发生插入，插入的核苷酸序列为{re_alt}，导致相应蛋白质序列中第{re_ppos}位氨基酸{short_aa(re_pref)['l']}突变为{short_aa(re_palt)['l']}，此突变在样本中的突变丰度为{_re_new.at[0, 'AlterRatio(%)']}%。\n"
        type_a = '插入'
    elif re_alt == '-':
        result1 = f"位于{re_enum}号外显子上的第{re_xnum}位核苷酸{re_ref}发生缺失，导致相应蛋白质序列中第{re_ppos}位氨基酸{short_aa(re_pref)['l']}突变为{short_aa(re_palt)['l']}，此突变在样本中的突变丰度为{_re_new.at[0, 'AlterRatio(%)']}%。\n"
        type_a = '缺失'
    else:
        result1 = f"位于{re_enum}号外显子上的第{re_xnum}位核苷酸{re_ref}突变为核苷酸{re_alt}，导致相应蛋白质序列中第{re_ppos}位氨基酸{short_aa(re_pref)['l']}突变为{short_aa(re_palt)['l']}，此突变在样本中的突变丰度为{_re_new.at[0, 'AlterRatio(%)']}%。\n"
        type_a = '突变'
    ### clinical描述 ###
    #result2 = '一项{已经完成/正在进行}的{Ⅰ/Ⅱ/Ⅲ}期临床试验针对{结肠癌中LN比率与KRAS表达的临床影响}进行了研究[{NCT04342676}]'
    odf = pd.DataFrame(columns={'Rank': "",
                                'NCT Number': "",
                                'Title': "",
                                'Status': "",
                                'Study Results': "",
                                'Conditions': "",
                                'Interventions': "",
                                'Phases': "",
                                'Locations': "",
                                'URL': "",
                                'Brief Summary': "",
                                'Detailed Description': "",
                                'Gene': "",
                                'Variation': "",
                                'Mutation': "",
                                'type': "",
                                'mutation': "",
                                'SYMBOL': ""})
    num_dict = {'1':'Ⅰ', '2':'Ⅱ', '3':'Ⅲ', '4':'Ⅳ', '5':'Ⅴ', '6':'Ⅵ'}
    study_dict = {'No Results Available':'正在进行', 'Has Results':'已经完成'}
    if _cl[_cl['Gene'] == gene].shape[0] == 0:
        odf = get_solid_tumor(gene, clinicaltrails_database, odf)
    else:
        tmp = _cl[_cl['Gene'] == gene]
        tmp['type'] = cancer
        tmp['mutation'] = gene
        tmp['SYMBOL'] = gene
        odf = pd.concat([odf, tmp])
    odf_new = odf.reset_index(drop=True)
    result2_list = []
    if odf_new.shape[0] == 0:
        result2 = ''
    else:
        if odf_new.shape[0] >= 3:
            odf_new.sort_values(by="Study Results", inplace=True, ascending=True)
            odf_new_tmp = odf_new.reset_index(drop=True)
            odf = odf_new_tmp.loc[:2]
        else:
            odf = odf_new
        for i in range(odf.shape[0]):
            ntc = odf.iloc[i]['NCT Number']
            title = odf.iloc[i]['Title']
            status = odf.iloc[i]['Status']
            study = odf.iloc[i]['Study Results']
            conditions = odf.iloc[i]['Conditions']
            phases = odf.iloc[i]['Phases']
            info = str(phases).split('|')
            num_all = []
            for n in info:
                num_tmp = re.match(r'.*Phase.*(\d+).*', str(n))
                if num_tmp:
                    num = num_dict[num_tmp.group(1)]
                else:
                    num = ''
                num_all.append(num)
            phases_re = '/'.join(num_all)
            result2_list.append(f'一项{study_dict[study]}的{phases_re}期临床试验针对{title}进行了研究[{ntc}]。')
        result2 = "".join(result2_list)

    ### NCCN描述 ###
    _nc = _nc[_nc['基因'] == gene]
    num = _nc.shape[0]
    result3 = ''
    if cancer != 'NSCLC' or num  == 0:
        result3 = ''
    else:
        for i in range(num):
            _nc_new = _nc.reset_index(drop=True)
            if (_nc_new.at[i,'基因'] == 'ERBB2' or _nc_new.at[i,'基因'] == 'HER2') and type_a == '突变':
                result3 = _nc_new.at[i,'NCCN指南汇总']
            elif _nc_new.at[i,'基因'] == 'EGFR' and re_enum == 19 and (type_a == '插入' or type_a == '缺失'):
                result3 = _nc_new.at[i, 'NCCN指南汇总']
            elif _nc_new.at[i,'基因'] == 'EGFR' and re_enum == 20 and type_a == '插入':
                result3 = _nc_new.at[i, 'NCCN指南汇总']
            elif _nc_new.at[i,'基因'] == 'MET' and re_enum == 14 and type_a == '缺失':
                result3 = _nc_new.at[i, 'NCCN指南汇总']
            elif _nc_new.at[i, '基因'] == 'EGFR' and _nc_new.at[i, '氨基酸'] == type_p:
                result3 = _nc_new.at[i, 'NCCN指南汇总']
            elif _nc_new.at[i, '基因'] == 'BRAF' and _nc_new.at[i, '氨基酸'] == type_p:
                result3 = _nc_new.at[i, 'NCCN指南汇总']
            elif _nc_new.at[i, '基因'] == 'KRAS' and _nc_new.at[i, '氨基酸'] == type_p:
                result3 = _nc_new.at[i, 'NCCN指南汇总']
            else:
                continue
    #result3 = 'NCCN指南内容'
    description = result1 + result2 + result3
    # '位于{2}号外显子上的第{35}位核苷酸{C}突变为核苷酸{T}，导致相应蛋白质序列中第{12}位氨基酸甘氨酸({G})\
    #             突变为天冬氨酸({D})，此突变在样本中的突变丰度为{47.72}%。\n{一项已经完成的Ⅲ期临床试验针对结肠癌中LN比率与KRAS表达的临床影响\
    #             进行了研究[NCT04342676]。一项已终止的Ⅰ期\Ⅱ期临床试验针对JI-101在晚期低度内分泌肿瘤、卵巢癌或KRAS突变结肠癌患者中的影响\
    #             进行了研究[NCT01149434]。NCCN指南指出，对于携带KRAS（exon2，3，4）基因突变、或NRAS（exon2，3，4）基因突变、或BRAF \
    #             V600E的转移性结直肠癌患者可能对西妥昔单抗或帕尼单抗耐药。}'
    #
    # var["HGVSp_short"] = short_id(var["HGVSp_x"])
    # if var['SYMBOL'] == "EGFR" and var['EXON'] == 'Exon 19/28' and var["mutation"].find("del") != -1:
    #     description = _df[(_df['gene'] == var['SYMBOL']) & (_df['var'] == 'Exon 19 deletion')]['des'].values.tolist()
    # elif var['SYMBOL'] in ["CDKN2A",'ERBB2','ESR1','KRAS','FGFR1',"FGFR2","FGFR3",'MTOR','NF1','NRAS','PTEN','STK11']:
    #     description = _df[(_df['gene'] == var['SYMBOL']) & (_df['var'] == 'Oncogenic Mutations')]['des'].values.tolist()
    # else:
    #     description = _df[(_df['gene'] == var['SYMBOL']) & (_df['var'] == var['HGVSp_short'])]['des'].values.tolist()
    # description = ''.join(map(str,description))
    return description
def Fusion_description(fusion,database):
    _df = pd.read_excel(database,sheet_name='Sheet1')
    _df = _df[_df['var'] == "Fusions"]
    description = _df[_df['gene'] == fusion['Hugo_Symbol']]['des'].values.tolist()
    description = ''.join(map(str,description))
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
        'Gly':'G',
        'Ter':'*'
            }
    for key in _map:
        longid = longid.replace(key, _map[key])
    shortid = longid.replace("p.","")
    return shortid

def short_aa(longid):
    id_aa = {
        'Phe': {'l':'苯丙氨酸(F)', 's':'F'},
        'Leu': {'l':'亮氨酸(L)', 's':'L'},
        'Ile': {'l':'异亮氨酸(I)', 's':'I'},
        'Met': {'l':'蛋氨酸(M)', 's':'M'},
        'Val': {'l':'缬氨酸(V)', 's':'V'},
        'Pro': {'l':'脯氨酸(P)', 's':'P'},
        'Thr': {'l':'苏氨酸(T)', 's':'T'},
        'Ala': {'l':'丙氨酸(A)', 's':'A'},
        'Tyr': {'l':'酪氨酸(Y)', 's':'Y'},
        'His': {'l':'组氨酸(H)', 's':'H'},
        'Gln': {'l':'谷氨酰胺(Q)', 's':'Q'},
        'Asn': {'l':'天冬酰胺(N)', 's':'N'},
        'Lys': {'l':'赖氨酸(K)', 's':'K'},
        'Asp': {'l':'天冬氨酸(D)', 's':'D'},
        'Glu': {'l':'谷氨酸(E)', 's':'E'},
        'Cys': {'l':'半胱氨酸(C)', 's':'C'},
        'Trp': {'l':'色氨酸(W)', 's':'W'},
        'Arg': {'l':'精氨酸(R)', 's':'R'},
        'Ser': {'l':'丝氨酸(S)', 's':'S'},
        'Gly': {'l':'甘氨酸(G)', 's':'G'},
        'Ter': {'l':'*', 's':'*'}
            }
    if longid in id_aa:
        return id_aa[longid]
    else:
        id_aa[longid] = {'l':'-', 's':'-'}
        return id_aa[longid]

###### 所在癌种中没有检测到结果，从实体瘤中提取信息 ######
def get_solid_tumor(gene, all_db, odf_s):
    db_s = pd.read_excel(all_db, sheet_name='solid tumor')
    tmp_s = db_s[db_s['Gene'] == gene]
    tmp_s['type'] = '实体瘤'
    tmp_s['mutation'] = gene
    tmp_s['SYMBOL'] = gene
    odf_s = pd.concat([odf_s, tmp_s])

    return odf_s
      

        
