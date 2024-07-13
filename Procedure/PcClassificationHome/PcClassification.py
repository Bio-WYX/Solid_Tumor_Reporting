import sys
sys.path.append("/data/auto_reporter_V2/reporter/guanhaowen/pan_cancer/pc")
from PcClassificationHome.PcModules.PcQC import PcGetQC
from PcClassificationHome.PcModules.PcLevel1_var import PcGet_level1_var
from PcClassificationHome.PcModules.PcLevel2_var import PcGet_level2_var
from PcClassificationHome.PcModules.PcDurg import PcDurg
from PcClassificationHome.PcModules.PcDDR_var import PcDDR_var
from PcClassificationHome.PcModules.PcGermline_var import PcGermline_var
from PcClassificationHome.PcModules.PcOverall import PcOverall
from PcClassificationHome.PcModules.PcImmu_var import PcImmu_var
from PcClassificationHome.PcModules.PcLevel3_var import PcGet_level3_var
from PcClassificationHome.PcModules.PcCoregene import PcCoregene
from PcClassificationHome.PcModules.PcClinicaltrils import PcClinicaltrils
from PcClassificationHome.PcModules.PcMSI import PcGet_MSI
from PcClassificationHome.PcModules.PcTMB import PcGet_TMB
from PcClassificationHome.PcModules.PcPgx import PcChemotherapy
from PcClassificationHome.PcModules.PcSummary import PcSummary
from PcClassificationHome.PcModules.PcSv import PcSv
from PcClassificationHome.PcModules.PcBaseclassify import PcBaseclassify
from PcClassificationHome.PcModules.PcPgx_new import PcPgx
from PcClassificationHome.PcModules.PcDisease_var import PcGet_Disease
from PcClassificationHome.PcModules.PcGeneDisease_var import PcGet_GeneDisease
import configparser

from docxtpl import DocxTemplate,InlineImage
import configparser
import datetime
from docx.shared import Mm
class PcClassification(PcBaseclassify):
    def __init__(self):
        super(PcClassification,self).__init__()     

    @property
    def pgx(self):
        """化疗药结果字典生成

        Returns:
            [dict]: [description]
        """
        _var = PcPgx()
        _var.gvcf = self._gvcf
        _var.chemotherapy_database = self._chemotherapy_database
        chemodic = {"toxic_dict":_var.chemo_dict["toxic_dict"].values(),
                    "effic_dict":_var.chemo_dict["effic_dict"].values(),
                    "info_dict": _var.chemo_dict['info_dict']}
                #"info_dict":_var.chemo_dict['info_dict'].values()}
        context = {"pgx_dict":chemodic}
        return context
    
    
    @property
    def out(self):
        """变异相关信息结果生成

        Returns:
            [dict]: [description]
        """
        # --------------*--一级变异处理--*-------------
        _lvl1 = PcGet_level1_var()
        _lvl1.report = self._report
        _lvl1.maf = self._maf
        _lvl1.cancer = self._cancer
        _lvl1.durg_name_database = self._durg_name_database
        _lvl1.gene_description = self._gene_description
        _lvl1.var_description = self._var_description
        _lvl1.prognosis = self._prognosis
        _lvl1.nccn_database = self._nccn_database
        _lvl1.clinicaltrils_database = self._clinicaltrils_database
        # --------------*--二级变异处理--*----------------
        _lvl2 = PcGet_level2_var()
        _lvl2.report = self._report
        _lvl2.maf = self._maf
        _lvl2.cancer = self._cancer
        _lvl2.durg_name_database = self._durg_name_database
        _lvl2.gene_description = self._gene_description
        _lvl2.var_description = self._var_description
        _lvl2.prognosis = self._prognosis
        _lvl2.nccn_database = self._nccn_database
        _lvl2.clinicaltrils_database = self._clinicaltrils_database
        # --------------*--三级变异处理--*-----------------
        _lvl3 = PcGet_level3_var()
        _lvl3.report = self._report
        _lvl3.maf = self._maf
        _lvl3.cancer = self._cancer
        _lvl3.gene_list = self._gene_list
        _lvl3.durg_name_database = self._durg_name_database
        _lvl3.gene_description = self._gene_description
        _lvl3.var_description = self._var_description
        _lvl3.prognosis = self._prognosis
        _lvl3.nccn_database = self._nccn_database
        _lvl3.clinicaltrils_database = self._clinicaltrils_database
        # ---------------*--TMB处理--*---------------------
        _tmb = PcGet_TMB()
        _tmb.report = self._report
        _tmb.tmb_database = self._tmb_database
        _tmb.tmb_png = self._tmb_png
        _tmb.cancer = self._cancer
        # ---------------*--MSI处理--*---------------------
        _msi = PcGet_MSI()
        _msi.msi_out = self._msi_out
        # --------------*--免疫相关处理--*-----------------
        _immu = PcImmu_var()
        _immu.report = self._report
        _immu.maf = self._maf
        _immu.cancer = self._cancer
        _immu.immu_database = self._immu_database
        # --------------*--临床试验相关处理--*-------------
        _cli = PcClinicaltrils()
        _cli.report = self._report
        _cli.maf = self._maf
        _cli.cancer = self._cancer
        _cli.clinicaltrils_database = self._clinicaltrils_database
        _cli.durg_name_database = self._durg_name_database
        # ---------------*--DDR相关处理--*------------
        _ddr = PcDDR_var()
        _ddr.maf = self._maf
        _ddr.report = self._report
        _ddr.durg_name_database = self._durg_name_database
        _ddr.gene_list = self._gene_list
        _ddr.cancer = self._cancer
        # ---------------*--胚系变异相关处理--*---------
        _ger = PcGermline_var()
        _ger.report = self._report
        _ger.maf = self._maf
        _ger.durg_name_database = self._durg_name_database
        _ger.gene_list = self._gene_list
        _ger.result = self._result
        # ---------------*--质控信息处理--*--------------
        _qc = PcGetQC()
        _qc.fastp_json_file = self._fastp_json_file
        _qc.bamdst_report = self._bamdst_report
        #----------------*--Fusion信息处理--*=------------
        _sv = PcSv()
        _sv.sv = self._sv 
        _sv.gene_list = self._gene_list
        _sv.durg_name_database = self._durg_name_database
        _sv.var_description = self._var_description
        _sv.gene_description = self._gene_description
        #----------------*--变异解读结果处理--*=------------
        _dis = PcGet_Disease()
        print (self._result)
        _dis.result = self._result
        _dis.durg_name_database = self._durg_name_database
        # ----------------*--基因疾病解读结果处理--*=------------
        _genedis = PcGet_GeneDisease()
        _genedis.result = self._result
        _genedis.gene_disease = self._gene_disease
        _genedis.durg_name_database = self._durg_name_database
        # ---------------*--核心基因相关变异处理--*-------
        # _core = PcCoregene()
        # _core.maf = self._maf
        # _core.gene_list = self._gene_list
        # _core.report = self._report
        # _core.cancer = self._cancer
        # ---------------*--变异汇总相关处理--*----------
        # _sum = PcSummary()
        # _sum.report = self._report
        # _sum.maf = self._maf
        # _sum.durg_name_database = self._durg_name_database
        # ---------------*--诺禾版变异信息相关处理--*----------
        # _nova = PcDurg()
        # _nova.report = self._report
        # _nova.maf = self._maf
        # _nova.durg_name_database = self._durg_name_database
        # _nova.gene_description = self._gene_description
        # _nova.var_description = self._var_description
        # lvl1_number = int(int(_lvl1.number)+int(_sv.var_dict["level_1_fusion_number"]))
        # lvl2_number = int(int(_lvl2.number)+int(_sv.var_dict["level_2_fusion_number"]))
        context = {"level1_var_dict":_lvl1.var_dict.values(),
                "level2_var_dict":_lvl2.var_dict.values(),
                "level1_var_number":int(int(_lvl1.number)+int(_sv.var_dict["level_1_fusion_number"])),
                "level2_var_number":int(int(_lvl2.number)+int(_sv.var_dict["level_2_fusion_number"])),
                "level3_var_dict":_lvl3.var_dict.values(),
                "level3_var_number":_lvl3.number,
                # "durg_overall_var_dict":_all_durg.var_dict.values(),
                "TMB_result":_tmb.tmb[0],
                "TMB_type":_tmb.tmb[1],
                "MSI_type":_msi.msi[0],
                "MSI_result":_msi.msi[1],
                "immu_cli_dict":_immu.immu_clinicaltrials.values(),
                "immu_postive_dict":_immu.immu_postive_dict.values(),
                "immu_negtive_dict":_immu.immu_negtive_dict.values(),
                "immu_supper_dict":_immu.immu_supper_dict.values(),
                "clinical_dict":_cli.clinical_dict.values(),
                "ddr_var_number":_ddr.number,
                "ddr_var_dict":_ddr.var_dict.values(),
                "msh_var_dict": _ddr.msh_dict.values(),
                "dis_dict": _dis.disease.values(),
                "unk_dict": _dis.unknown.values(),
                "gene_dis_dict": _genedis.ge_disease.values(),
                "gene_unk_dict": _genedis.ge_unknown.values(),
                "germline_var_number":_ger.number,
                "germline_num_dict":_ger.pathogenic,
                "germline_var_dict":_ger.var_dict.values(),
                "q30":_qc.fasta_qc_result['q30'],
                "raw_data":_qc.fasta_qc_result['raw_data'],
                "depth":_qc.bam_qc_result['depth'],
                "coverage":_qc.bam_qc_result['coverage'],
                "level1_fusion_dict":_sv.var_dict['level_1_fusion'].values(),
                "level2_fusion_dict":_sv.var_dict['level_2_fusion'].values(),
                # 'core_list':_core.var_dict,
                # "huizong_dict":_sum.var_dict.values(),
                # "nova_dict":_nova.var_dict.values(),
                # "cancer":_core.cancer_cn
        }
        return context

        
if __name__== "__main__":
    config = configparser.ConfigParser()
    config_path = r'/data/autoReportV2/reporter/guanhaowen/pan_cancer/dependent/config/config.ini'
    config.read(config_path,encoding='utf-8')
    #DURG_NAME_DATABASE = config['PATH']['path'] + config['DATABASE']['durg_name_database']
    #GENE_DESCRIPITON = config['PATH']['path'] + config['DATABASE']['gene_description']
    #VAR_DESCRIPITON = config['PATH']['path'] + config['DATABASE']['var_description']
    #IMMU_DATABASE = config['PATH']['path'] + config['DATABASE']['immu_database']
    #CLINICALTAILS_DATABASE = config['PATH']['path'] + config['DATABASE']['clinicaltrail_database']
    #GENE_LIST = config['PATH']['path'] + config['DATABASE']['gene_list']
    #NCCN_DATABASE = config['PATH']['path'] + config['DATABASE']['nccn_database']
    #CHEMOTHERAPY_DATABASE = config['PATH']['path'] + config['DATABASE']['chemotherapy_database']
    #MAFANNOTATOR = config['PATH']['path'] + config['SCRIPT']['MafAnnotator']
    #ONCOKB_TOKEN = config['FILE']['oncokb_token']
    #TMB_DATABASE = config['PATH']['path'] + config['DATABASE']['tmb_database']
    #TMP_PNG = config['PATH']['path'] + config['FILE']['tmp_png']
    #TEMPLATE_1 = config['PATH']['path'] + config['FILE']['template_1']
    #TEMPLATE_2 = config['PATH']['path'] + config['FILE']['template_2']
    
    DURG_NAME_DATABASE = "/data/autoReportV2/reporter/guanhaowen/database_ST/实体瘤-药物名称.xlsx"
    GENE_DESCRIPITON = "/data/autoReportV2/reporter/guanhaowen/database_ST/实体瘤-Gene_description.xlsx"
    VAR_DESCRIPITON = "/data/autoReportV2/reporter/guanhaowen/database_ST/实体瘤-变异注释.xlsx"
    IMMU_DATABASE = "/data/autoReportV2/reporter/guanhaowen/database_ST/实体瘤-免疫.xlsx"
    CLINICALTAILS_DATABASE = "/data/autoReportV2/reporter/guanhaowen/database_ST/实体瘤-clinicaltrails.xlsx"
    GENE_LIST = "/data/autoReportV2/reporter/guanhaowen/database_ST/实体瘤-genelist.xlsx"
    NCCN_DATABASE = "/data/autoReportV2/reporter/guanhaowen/database_ST/实体瘤-NCCN.xlsx"
    CHEMOTHERAPY_DATABASE = "/data/autoReportV2/reporter/guanhaowen/database_ST/实体瘤-化疗药.xlsx"
    MAFANNOTATOR = "/data/autoReportV2/reporter/guanhaowen/pan_cancer/pc/oncokb/oncokb-annotator-master/MafAnnotator.py"
    ONCOKB_TOKEN = "4e9508e0-cc76-47d9-ae1b-8fd180b43e53"
    TMB_DATABASE = "/data/autoReportV2/reporter/guanhaowen/database_ST/实体瘤-TMB.xlsx"
    TMP_PNG = "/data/autoReportV2/reporter/guanhaowen/pan_cancer/dependent/template/tmp_png.png"
    TEMPLATE_1 = "/data/autoReportV2/reporter/guanhaowen/pan_cancer/dependent/template/nova_type_template.docx"
    TEMPLATE_2 = "/data/autoReportV2/reporter/guanhaowen/pan_cancer/dependent/template/genecast_type_template.docx"
    PROGNOSIS_DATABASE = "/data/autoReportV2/reporter/guanhaowen/database_ST/实体瘤-预后计算.xlsx"
    GENED_DATABASE = "/data/autoReportV2/reporter/guanhaowen/database_ST/实体瘤-医检所遗传病.xlsx"


    cls=PcClassification()
    cls.report = "/data/download/lis/report/王月星/2023-06-01/41481/8df71b5bfa115dd359ee33171c90b029.xls" #vep注释结果
    cls.result = "/data/download/lis/report/王月星/2023-06-01/41481/8df71b5bfa115dd359ee33171c90b029.xls"
    cls.maf = "/data/download/lis/report/王月星/2023-06-01/41481/2dca21870bf758a4e7e70b8bd557295e.maf.clean.oncokb_out" #得到oncokb注释后的maf文件
    cls.cancer = "Esophagogastric Cancer"
    cls.gvcf =  "/data/download/lis/report/王月星/2023-06-01/41481/8f2c0d787c8ae463c360189074ffca66.gz" #gvcf路径
    cls.msi_out = "/data/download/lis/report/王月星/2023-06-01/41481/9a8f93d4fea299841ba25bb0b0999d98.txt" #msi检测结果文件
    cls.bamdst_report = "/data/download/lis/report/王月星/2023-06-01/41481/c0d7d048c37d2f662ada5f0871827304.report"
    cls.fastp_json_file = "/data/download/lis/report/王月星/2023-06-01/41481/ed5bad68da3f75c2ba63f425ee6a9551.json"
    cls.sv = "/data/download/lis/report/王月星/2023-06-01/41481/7d66cb7dc85f23872e94c86f5c4d4231.json.clean.oncokb_out"
    
    # --*--2.传入数据库--*--
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
    cls.prognosis = PROGNOSIS_DATABASE
    cls.gene_disease = GENED_DATABASE
    
    #tpl = DocxTemplate("/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/dependent/template/模板.docx")
    tpl = DocxTemplate(TEMPLATE_1)
    context = cls.out
    context.update(cls.pgx)
    tpl.render(context)
    set_of_variables = tpl.get_undeclared_template_variables()
    tpl.save("/data/download/lis/report/王月星/2023-06-01/41481/BLA02193.docx")
    
    
    
    
    
    

