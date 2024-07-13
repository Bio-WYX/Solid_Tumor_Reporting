from PcClassificationHome.PcClassification import PcClassification
from PcClassificationHome.PcModules import PcBaseclassify
from PcInfo import PcInfo
from PcPreprocess.PcPreModules.PcPreprocessScript import PcPreprocess
from PcDatabase.PcDatabase import PcDatabase
from docxtpl import DocxTemplate,InlineImage
import configparser
import datetime
from docx.shared import Mm
import pandas as pd
from ar.db.WtDatabaseInstance import db
import os
# array_db = db.get_table("实体瘤大报告", "OncoKB_FDA").get()
pd.set_option('mode.chained_assignment', None)
config = configparser.ConfigParser()
#config_path = "/data/autoReportV2/reporter/guanhaowen/pan_cancer/dependent/config/config.ini"
config_path = "/data/auto_reporter_V2/reporter/guanhaowen/pan_cancer/dependent/config/config.ini"
config.read(config_path,encoding='utf-8')

MAFANNOTATOR = config['PATH']['path'] + config['SCRIPT']['MafAnnotator']
#ONCOKB_TOKEN = config['PATH']['path'] + config['FILE']['oncokb_token']
ONCOKB_TOKEN = config['FILE']['oncokb_token']
TEMPLATE_1 = config['PATH']['path'] + config['FILE']['template_1']
TEMPLATE_2 = config['PATH']['path'] + config['FILE']['template_2']

FUSIONANNOTATOR = config['PATH']['path'] + config['SCRIPT']['FusionAnnotator']
TMP_PNG = config['PATH']['path'] + config['FILE']['tmp_png']

database = PcDatabase()
database.database_dict()
database_path = config['PATH']['path'] + config['DATABASE']['database_ST']
DURG_NAME_DATABASE = os.path.join(database_path, '实体瘤-药物名称.xlsx')
GENE_DESCRIPITON = os.path.join(database_path, "实体瘤-Gene_description.xlsx")
VAR_DESCRIPITON = os.path.join(database_path, "实体瘤-变异注释.xlsx")
IMMU_DATABASE = os.path.join(database_path, "实体瘤-免疫.xlsx")
CLINICALTAILS_DATABASE = os.path.join(database_path, "实体瘤-clinicaltrails.xlsx")
GENE_LIST = os.path.join(database_path, "实体瘤-genelist.xlsx")
NCCN_DATABASE = os.path.join(database_path, "实体瘤-NCCN.xlsx")
CHEMOTHERAPY_DATABASE = os.path.join(database_path, "实体瘤-化疗药.xlsx")
TMB_DATABASE = os.path.join(database_path, "实体瘤-TMB.xlsx")
GENE_DISEASE = os.path.join(database_path, "实体瘤-医检所遗传病.xlsx")
PROGNOSIS = os.path.join(database_path, "实体瘤-预后计算.xlsx")

# config_path = '/mnt/e/ansaisi/641panel/pan_cancer/dependent/config/config.ini'
# config.read(config_path,encoding='utf-8')
# DURG_NAME_DATABASE = config['PATH']['path'] + config['DATABASE']['durg_name_database']
# GENE_DESCRIPITON = config['PATH']['path'] + config['DATABASE']['gene_description']
# VAR_DESCRIPITON = config['PATH']['path'] + config['DATABASE']['var_description']
# IMMU_DATABASE = config['PATH']['path'] + config['DATABASE']['immu_database']
# CLINICALTAILS_DATABASE = config['PATH']['path'] + config['DATABASE']['clinicaltrail_database']
# GENE_LIST = config['PATH']['path'] + config['DATABASE']['gene_list']
# NCCN_DATABASE = config['PATH']['path'] + config['DATABASE']['nccn_database']
# CHEMOTHERAPY_DATABASE = config['PATH']['path'] + config['DATABASE']['chemotherapy_database']
# MAFANNOTATOR = config['PATH']['path'] + config['SCRIPT']['MafAnnotator']
# ONCOKB_TOKEN = config['FILE']['oncokb_token']
# TMB_DATABASE = config['PATH']['path'] + config['DATABASE']['tmb_database']
#
# TMP_PNG = config['PATH']['path'] + config['FILE']['tmp_png']
# TEMPLATE_1 = config['PATH']['path'] + config['FILE']['template_1']
# TEMPLATE_2 = config['PATH']['path'] + config['FILE']['template_2']
# GENE_DISEASE = config['PATH']['path'] + config['DATABASE']['gene_disease_database']
# PROGNOSIS = config['PATH']['path'] + config['DATABASE']['prognosis_database']

# if __name__ == '__main__':
#     start_time = datetime.datetime.now()
#     # test_json = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/data/input/sampleinfo.json"
#     # test_json = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/data/input/sampleinfo copy.json"
#     # test_json = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/data/input/sampleinfo copy 3.json"
#     test_json = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/data/input/sampleinfo copy 4.json"
#     #test_json = "/mnt/e/ansaisi/641panel/20220510/report.json"
#     #test_json = "/mnt/e/ansaisi/641panel/阅尔历史数据.2022.05.10/ANN20220418-1-SP20416W03/report.json"
def run_report(load_dict):
    start_time = datetime.datetime.now()
    # ===================================
    # --*--读取包含输入文件信息的字典--*--
    # ===================================
    info = PcInfo.PcInfo()
    info.load_dict = load_dict
    # ====================================================
    # --*--预处理，读取输入患者信息，存储至PcBaseclassify--*--
    # ====================================================
    clf = PcBaseclassify.PcBaseclassify()
    #clf.diagnosis = info.diagnosis
    clf.diagnosis = info.info_dict['diagnosis']
    # ================================================
    # --*--预处理，对maf文件利用oncokb api 进行注释--*--
    # ================================================
    pre = PcPreprocess()
    pre.raw_maf = info.raw_maf #传递raw_maf路径
    pre.mode = int(info.mode) #传递mode号
    pre.mafannotator = MAFANNOTATOR #传递api脚本路径 
    pre.fusionannotator = FUSIONANNOTATOR
    pre.oncokb_token = ONCOKB_TOKEN #传递api token
    pre.raw_sv = info.fusion_out   #传递fusion路径
    pre.cnv_out = info.cnv_out   #传递cnv路径
    # ========================================
    # --*--变异分级，生成报告模板所需的变量--*--
    # ========================================
    cls = PcClassification()
    # --*--1.传入文件--*--
    cls.report = info.report #vep注释结果  report
    cls.maf = pre.maf #得到oncokb注释后的maf文件
    cls.cancer = pre.cancer
    cls.gvcf = info.gvcf #gvcf路径
    cls.msi_out = info.msi_out #msi检测结果文件
    cls.sv = pre.sv #Fusion变异经过oncokb注释后的结果。
    cls.fastp_json_file = info.fastp_json_file #传入fastq质控结果json文件
    cls.bamdst_report = info.bamdst_report #传入bamdst质控结果report文件
    cls.result = info.report               #变异位点解读结果  result
    # =======================
    # --*--2.传入数据库--*--
    # =======================
    cls.durg_name_database = DURG_NAME_DATABASE
    cls.gene_description = GENE_DESCRIPITON
    cls.var_description = VAR_DESCRIPITON
    cls.immu_database = IMMU_DATABASE
    cls.clinicaltrils_database = CLINICALTAILS_DATABASE
    cls.gene_list = GENE_LIST
    cls.nccn_database = NCCN_DATABASE
    cls.chemotherapy_database = CHEMOTHERAPY_DATABASE  
    cls.tmb_database = TMB_DATABASE
    cls.tmb_png = TMP_PNG
    cls.gene_disease = GENE_DISEASE
    cls.prognosis = PROGNOSIS
    #===================
    # --*--生成报告--*--
    #===================
    context = pre.introduce #加入癌种对应的介绍文本
    context.update(info.info_dict) #模板加入样本信息
    context.update(cls.out) #模板加入变异相关信息
    context.update(cls.pgx) #模板加入化疗药物相关信息
    #print (context['gene_unk_dict'])
    
    if info.template == 1: #根据mode号选择对应的模板
        tpl=DocxTemplate(TEMPLATE_1)#诺禾版
    elif info.template == 2:
        tpl=DocxTemplate(TEMPLATE_2)#臻和版
    tmb_image = {'TMB_image':InlineImage(tpl, cls.tmb_png, width=Mm(100), height=Mm(80))}
    context.update(tmb_image)
    tpl.render(context)
    set_of_variables = tpl.get_undeclared_template_variables()
    tpl.save(info.docx_path)
    end_time = datetime.datetime.now()
    print("运行时间：",(end_time-start_time))
