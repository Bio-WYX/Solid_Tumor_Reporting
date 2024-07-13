import json
import time
import os
from ar.db.WtDatabaseInstance import db
import configparser
import pandas as pd

class PcDatabase():
    def get_excel(self, data_dict, database_path, outname):
        self._data_dict = data_dict
        self._database_path = database_path
        self._outname = outname
        try:
            writer = pd.ExcelWriter(os.path.join(self._database_path, '{}.xlsx'.format(self._outname)))
            for keys in self._data_dict.keys():
                df = self._data_dict[keys]
                df.to_excel(writer, keys, index=False)
            writer.save()
            writer.close()
        except ValueError as e:
            print("引发异常：", repr(e))

    def database_dict(self):
        pd.set_option('mode.chained_assignment', None)
        config = configparser.ConfigParser()
        config_path = "/data/auto_reporter_V2/reporter/guanhaowen/pan_cancer/dependent/config/config.ini"
        config.read(config_path, encoding='utf-8')
        database_path = config['PATH']['path'] + config['DATABASE']['database_ST']
        print (database_path)
        if not os.path.exists(database_path):
            os.makedirs(database_path)

        DURG_NAME_DATABASE_1 = db.get_table("实体瘤-药物名称", "Sheet1").get()  # Sheet1,Sheet2,CLNSIG_dict,Consequence_dict
        DURG_NAME_DATABASE_2 = db.get_table("实体瘤-药物名称", "Sheet2").get()
        DURG_NAME_DATABASE_CL = db.get_table("实体瘤-药物名称", "CLNSIG_dict").get()
        DURG_NAME_DATABASE_Co = db.get_table("实体瘤-药物名称", "Consequence_dict").get()
        Sheet1 = pd.DataFrame(DURG_NAME_DATABASE_1)[['英文名称','中文名称']]
        Sheet2 = pd.DataFrame(DURG_NAME_DATABASE_2)[['中文名称','英文名称']]
        CLNSIG_dict = pd.DataFrame(DURG_NAME_DATABASE_CL)[['ClinVar_CLNSIG','CN_CLNSIG']]
        Consequence_dict = pd.DataFrame(DURG_NAME_DATABASE_Co)[['Display term','翻译','变异','变异翻译','SO_term']]
        DURG_NAME_dict = {'Sheet1': Sheet1, 'Sheet2': Sheet2, 'CLNSIG_dict':CLNSIG_dict, 'Consequence_dict':Consequence_dict}
        self.get_excel(DURG_NAME_dict, database_path, '实体瘤-药物名称')

        GENE_DESCRIPITON_dc = db.get_table("实体瘤-Gene_description", "description").get()  #description,Sheet1
        GENE_DESCRIPITO_s1 = db.get_table("实体瘤-Gene_description", "Sheet1").get()
        gene_description_dc = pd.DataFrame(GENE_DESCRIPITON_dc)[['校对者', 'SYMBOL', '校对后', '描述1', '描述2', 'Genen1', 'Genen2']]
        gene_description_s1 = pd.DataFrame(GENE_DESCRIPITO_s1)[['Gene']]
        gene_description_dict = {'description': gene_description_dc, 'Sheet1': gene_description_s1}
        self.get_excel(gene_description_dict, database_path, '实体瘤-Gene_description')

        VAR_DESCRIPITON = db.get_table("实体瘤-变异注释", "Sheet1").get() #Sheet1
        var_description = pd.DataFrame(VAR_DESCRIPITON)[['gene', 'var', 'des']]
        var_description_dict = {'Sheet1': var_description}
        self.get_excel(var_description_dict, database_path, '实体瘤-变异注释')

        IMMU_DATABASE_HLA = db.get_table("实体瘤-免疫", "HLA").get() #HLA,免疫治疗临床意义,NSCLC,HCC,Breast Cancer,Esophagogastric Cancer,Colorectal Cancer
        IMMU_DATABASE_LC = db.get_table("实体瘤-免疫", "免疫治疗临床意义").get()
        IMMU_DATABASE_NSCLC = db.get_table("实体瘤-免疫", "NSCLC").get()
        IMMU_DATABASE_HCC = db.get_table("实体瘤-免疫", "HCC").get()
        IMMU_DATABASE_BC = db.get_table("实体瘤-免疫", "Breast Cancer").get()
        IMMU_DATABASE_EC = db.get_table("实体瘤-免疫", "Esophagogastric Cancer").get()
        IMMU_DATABASE_CC = db.get_table("实体瘤-免疫", "Colorectal Cancer").get()
        HLA = pd.DataFrame(IMMU_DATABASE_HLA)[['HLA', 'Supertype']]
        LC = pd.DataFrame(IMMU_DATABASE_LC)[['基因', '相关性', '临床解释', '参考文献']]
        NSCLC = pd.DataFrame(IMMU_DATABASE_NSCLC)[['编号', '分期', '癌种', '国家', '相关药物']]
        HCC = pd.DataFrame(IMMU_DATABASE_HCC)[['编号', '分期', '癌种', '国家', '相关药物']]
        BC = pd.DataFrame(IMMU_DATABASE_BC)[['编号', '分期', '癌种', '国家', '相关药物']]
        EC = pd.DataFrame(IMMU_DATABASE_EC)[['编号', '分期', '癌种', '国家', '相关药物']]
        CC = pd.DataFrame(IMMU_DATABASE_CC)[['编号', '分期', '癌种', '国家', '相关药物']]
        DURG_NAME_dict = {'HLA': HLA, '免疫治疗临床意义': LC, 'NSCLC': NSCLC, 'HCC': HCC, 'Breast Cancer':BC, \
                          'Esophagogastric Cancer':EC, 'Colorectal Cancer':CC}
        self.get_excel(DURG_NAME_dict, database_path, '实体瘤-免疫')

        CLINICALTAILS_NSCLC = db.get_table("实体瘤-clinicaltrails", "NSCLC").get() #NSCLC,HCC,Breast Cancer,Esophagogastric Cancer,Colorectal Cancer,solid tumor
        CLINICALTAILS_HCC = db.get_table("实体瘤-clinicaltrails", "HCC").get()
        CLINICALTAILS_BC = db.get_table("实体瘤-clinicaltrails", "Breast Cancer").get()
        CLINICALTAILS_EC = db.get_table("实体瘤-clinicaltrails", "Esophagogastric Cancer").get()
        CLINICALTAILS_CC = db.get_table("实体瘤-clinicaltrails", "Colorectal Cancer").get()
        CLINICALTAILS_ST = db.get_table("实体瘤-clinicaltrails", "solid tumor").get()
        NSCLC = pd.DataFrame(CLINICALTAILS_NSCLC)[['Rank', 'NCT Number', 'PMID', 'Title_EN', 'Title', 'Status', 'Study Results', 'Conditions', 'Interventions', 'Phases', 'Locations', 'URL', 'Brief Summary', 'Detailed Description', 'Gene', 'Variation', 'Mutation']]
        HCC = pd.DataFrame(CLINICALTAILS_HCC)[['Rank', 'NCT Number', 'PMID', 'Title_EN', 'Title', 'Status', 'Study Results', 'Conditions', 'Interventions', 'Phases', 'Locations', 'URL', 'Brief Summary', 'Detailed Description', 'Gene', 'Variation', 'Mutation']]
        BC = pd.DataFrame(CLINICALTAILS_BC)[['Rank', 'NCT Number', 'PMID', 'Title_EN', 'Title', 'Status', 'Study Results', 'Conditions', 'Interventions', 'Phases', 'Locations', 'URL', 'Brief Summary', 'Detailed Description', 'Gene', 'Variation', 'Mutation']]
        EC = pd.DataFrame(CLINICALTAILS_EC)[['Rank', 'NCT Number', 'PMID', 'Title_EN', 'Title', 'Status', 'Study Results', 'Conditions', 'Interventions', 'Phases', 'Locations', 'URL', 'Brief Summary', 'Detailed Description', 'Gene', 'Variation', 'Mutation']]
        CC = pd.DataFrame(CLINICALTAILS_CC)[['Rank', 'NCT Number', 'PMID', 'Title_EN', 'Title', 'Status', 'Study Results', 'Conditions', 'Interventions', 'Phases', 'Locations', 'URL', 'Brief Summary', 'Detailed Description', 'Gene', 'Variation', 'Mutation']]
        ST = pd.DataFrame(CLINICALTAILS_ST)[['Rank', 'NCT Number', 'PMID', 'Title_EN', 'Title', 'Status', 'Study Results', 'Conditions', 'Interventions', 'Phases', 'Locations', 'URL', 'Brief Summary', 'Detailed Description', 'Gene', 'Variation']]
        clinicaltrails_dict = {'NSCLC': NSCLC, 'HCC': HCC, 'Breast Cancer': BC, 'Esophagogastric Cancer': EC, \
                               'Colorectal Cancer': CC, 'solid tumor':ST}
        self.get_excel(clinicaltrails_dict, database_path, '实体瘤-clinicaltrails')

        GENE_LIST_DDR = db.get_table("实体瘤-genelist", "DDR相关基因").get() #DDR相关基因,靶向药相关基因,化疗药相关基因,融合基因,免疫治疗,遗传易感,驱动基因,Sheet5,肺癌核心基因,ALL,Sheet1
        GENE_LIST_BXY = db.get_table("实体瘤-genelist", "靶向药相关基因").get()
        GENE_LIST_HLY = db.get_table("实体瘤-genelist", "化疗药相关基因").get()
        GENE_LIST_RH = db.get_table("实体瘤-genelist", "融合基因").get()
        GENE_LIST_MY = db.get_table("实体瘤-genelist", "免疫治疗").get()
        GENE_LIST_YC = db.get_table("实体瘤-genelist", "遗传易感").get()
        GENE_LIST_QD = db.get_table("实体瘤-genelist", "驱动基因").get()
        GENE_LIST_FA = db.get_table("实体瘤-genelist", "肺癌核心基因").get()
        GENE_LIST_ALL = db.get_table("实体瘤-genelist", "ALL").get()
        GENE_LIST_Sheet1 = db.get_table("实体瘤-genelist", "Sheet1").get()
        GENE_LIST_Sheet5 = db.get_table("实体瘤-genelist", "Sheet5").get()
        DDR = pd.DataFrame(GENE_LIST_DDR)[['DDR_gene', 'MMR', 'BER', 'NER', 'HRR', 'NHEJ', 'MSH_gene']]
        BXY = pd.DataFrame(GENE_LIST_BXY)[['Gene name']]
        HLY = pd.DataFrame(GENE_LIST_HLY)[['化疗药相关基因']]
        RH = pd.DataFrame(GENE_LIST_RH)[['融合基因', 'Intron', 'Exon', '上下游', 'VAR', 'ref']]
        MY = pd.DataFrame(GENE_LIST_MY)[['免疫治疗']]
        YC = pd.DataFrame(GENE_LIST_YC)[['所有基因', '乳腺癌-卵巢癌综合征', '结直肠癌', '前列腺癌', '胰腺癌', '胃癌', '子宫内膜癌', '肾癌', '食道癌', '胃肠道间质瘤', '黑色素瘤', '遗传性副神经节瘤/嗜铬细胞瘤综合征', '视网膜母细胞瘤', '多发性内分泌腺瘤', '家族性甲状腺髓样癌', '多发性神经纤维瘤', '骨肉瘤']]
        QD = pd.DataFrame(GENE_LIST_QD)[['驱动基因']]
        FA = pd.DataFrame(GENE_LIST_FA)[['核心基因']]
        ALL = pd.DataFrame(GENE_LIST_ALL)[['基因', '臻和', '诺禾']]
        Sheet1 = pd.DataFrame(GENE_LIST_Sheet1)[['癌种', 'EN']]
        Sheet5 = pd.DataFrame(GENE_LIST_Sheet5)[['Gene']]
        GENE_LIST_dict = {'DDR相关基因': DDR, '靶向药相关基因': BXY, '化疗药相关基因': HLY, '融合基因': RH, '免疫治疗': MY, \
                          '遗传易感': YC, '驱动基因': QD, '肺癌核心基因': FA, 'ALL': ALL, 'Sheet1': Sheet1, 'Sheet5': Sheet5}
        self.get_excel(GENE_LIST_dict, database_path, '实体瘤-genelist')

        NCCN_DATABASE_all = db.get_table("实体瘤-NCCN", "汇总").get() #汇总,NCCN,FDA,汇总-变异描述
        NCCN_DATABASE_NCCN = db.get_table("实体瘤-NCCN", "NCCN").get()
        NCCN_DATABASE_FDA = db.get_table("实体瘤-NCCN", "FDA").get()
        NCCN_DATABASE_VR = db.get_table("实体瘤-NCCN", "汇总-变异描述").get()
        all = pd.DataFrame(NCCN_DATABASE_all)[['基因', '突变位点', '癌种', '药物', 'NCCN指南汇总', 'FDA汇总', 'NMPA汇总']]
        NCCN = pd.DataFrame(NCCN_DATABASE_NCCN)[['基因', '突变位点', '癌种', '首选药物', '治疗', '证据', '其他推荐药物', '指南', 'EGFR突变', '汇总']]
        FDA = pd.DataFrame(NCCN_DATABASE_FDA)[['VAR', 'FDA']]
        VR = pd.DataFrame(NCCN_DATABASE_VR)[['基因', '核苷酸', '氨基酸', '癌种', '药物', 'NCCN指南汇总', 'FDA汇总', 'NMPA汇总']]
        NCCN_dict = {'汇总': all, 'NCCN': NCCN, 'FDA': FDA, '汇总-变异描述': VR}
        self.get_excel(NCCN_dict, database_path, '实体瘤-NCCN')

        CHEMOTHERAPY_DATABASE_YW = db.get_table("实体瘤-化疗药", "药物顺序").get() #药物顺序,Pgx,rs,变量,Sheet5,Sheet1,Sheet2,单药+联合
        CHEMOTHERAPY_DATABASE_Pgx = db.get_table("实体瘤-化疗药", "Pgx").get()
        CHEMOTHERAPY_DATABASE_rs = db.get_table("实体瘤-化疗药", "rs").get()
        CHEMOTHERAPY_DATABASE_BL = db.get_table("实体瘤-化疗药", "变量").get()
        CHEMOTHERAPY_DATABASE_DL = db.get_table("实体瘤-化疗药", "单药+联合").get()
        CHEMOTHERAPY_DATABASE_Sheet1 = db.get_table("实体瘤-化疗药", "Sheet1").get()
        CHEMOTHERAPY_DATABASE_Sheet2 = db.get_table("实体瘤-化疗药", "Sheet2").get()
        CHEMOTHERAPY_DATABASE_Sheet5 = db.get_table("实体瘤-化疗药", "Sheet5").get()
        YW = pd.DataFrame(CHEMOTHERAPY_DATABASE_YW)[['药物']]
        Pgx = pd.DataFrame(CHEMOTHERAPY_DATABASE_Pgx)[['药物', '基因', '位点', '基因型', '证据等级', '描述', '毒副作用', '毒副作用-影响', '功效', '功效-影响', '分类']]
        rs = pd.DataFrame(CHEMOTHERAPY_DATABASE_rs)[['位点', 'Allele']]
        BL = pd.DataFrame(CHEMOTHERAPY_DATABASE_BL)[['药物', '基因', '位点', '基因型', '毒性', '有效性', '证据等级']]
        DL = pd.DataFrame(CHEMOTHERAPY_DATABASE_DL)[['药物', '基因', '位点', '基因型', '证据等级', '描述', '毒副作用', '毒副作用-影响', '功效', '功效-影响']]
        Sheet1 = pd.DataFrame(CHEMOTHERAPY_DATABASE_Sheet1)[['rs号', '尿嘧啶']]
        Sheet2 = pd.DataFrame(CHEMOTHERAPY_DATABASE_Sheet2)[['药物', '基因', '位点', '基因型', '证据等级', '描述', '毒副作用', '毒副作用-影响', '功效', '功效-影响']]
        Sheet5 = pd.DataFrame(CHEMOTHERAPY_DATABASE_Sheet5)[['药物', '基因', '位点', '基因型', '证据等级', '描述', '毒副作用', '毒副作用-影响', '功效', '功效-影响']]
        CHEMOTHERAPY_dict = {'药物顺序': YW, 'Pgx': Pgx, 'rs': rs, '变量': BL, '单药+联合': DL,'Sheet1': Sheet1, \
                             'Sheet2': Sheet2,'Sheet5':Sheet5}
        self.get_excel(CHEMOTHERAPY_dict, database_path, '实体瘤-化疗药')

        TMB_DATABASE_NSCLC = db.get_table("实体瘤-TMB", "NSCLC").get() #NSCLC,HCC,Breast Cancer,Esophagogastric Cancer,Colorectal Cancer
        TMB_DATABASE_HCC = db.get_table("实体瘤-TMB", "HCC").get()
        TMB_DATABASE_BC = db.get_table("实体瘤-TMB", "Breast Cancer").get()
        TMB_DATABASE_EC = db.get_table("实体瘤-TMB", "Esophagogastric Cancer").get()
        TMB_DATABASE_CC = db.get_table("实体瘤-TMB", "Colorectal Cancer").get()
        NSCLC = pd.DataFrame(TMB_DATABASE_NSCLC)[['Tumor_Sample_Barcode', 'TB_num']]
        HCC = pd.DataFrame(TMB_DATABASE_HCC)[['Tumor_Sample_Barcode', 'TB_num']]
        BC = pd.DataFrame(TMB_DATABASE_BC)[['Tumor_Sample_Barcode', 'TB_num']]
        EC = pd.DataFrame(TMB_DATABASE_EC)#[['Tumor_Sample_Barcode', 'TB_num']]
        CC = pd.DataFrame(TMB_DATABASE_CC)[['Tumor_Sample_Barcode', 'TB_num']]
        TMB_DATABASE_dict = {'NSCLC': NSCLC, 'HCC': HCC, 'Breast Cancer': BC, 'Esophagogastric Cancer': EC, 'Colorectal Cancer': CC}
        self.get_excel(TMB_DATABASE_dict, database_path, '实体瘤-TMB')

        GENE_DISEASE_gene = db.get_table("实体瘤-医检所遗传病", "基因").get() #基因,疾病
        GENE_DISEASE_dis = db.get_table("实体瘤-医检所遗传病", "疾病").get()
        gene = pd.DataFrame(GENE_DISEASE_gene)[['recordId_x', '基因名称', '染色体号', '染色体位置', '基因全长', '全部外显子数', '常见转录本', '编码蛋白_EN', '编码蛋白_CN', '蛋白功能_EN', '蛋白功能_CN', '候选疾病类型', 'LOF是否使其致病机制', '斜体_x', '基因与疾病的有效性', 'pLI']]
        dise = pd.DataFrame(GENE_DISEASE_dis)[['recordId_x', '基因名称', '染色体号', '疾病_CN', '疾病_EN', '疾病名称', 'OMIM', '遗传', '疾病详细介绍', 'index']]
        GENE_DISEASE_dict = {'基因': gene, '疾病': dise}
        self.get_excel(GENE_DISEASE_dict, database_path, '实体瘤-医检所遗传病')

        PROGNOSIS = db.get_table("实体瘤-预后计算", "Sheet1").get() #Sheet1
        Sheet1 = pd.DataFrame(PROGNOSIS)[['Gene', 'Bladder Carcinoma', 'Breast Cancer', 'Cervical squamous cell carcinoma', 'Colorectal Cancer', 'Cutaneous melanoma', 'Head-neck squamous cell carcinoma', 'Kidney renal clear cell carcinoma', 'Kidney renal papillary cell carcinoma', 'HCC', 'Low grade glioma', 'NSCLC', 'Lung squamous cell carcinoma', 'Ovarian cancer', 'Prostate adenocarcinoma', 'Sarcoma', 'Esophagogastric Cancer', 'Thyroid carcinoma', 'Uterine corpus endometrial carcinoma']]
        PROGNOSIS_dict = {'Sheet1': Sheet1}
        self.get_excel(PROGNOSIS_dict, database_path, '实体瘤-预后计算')