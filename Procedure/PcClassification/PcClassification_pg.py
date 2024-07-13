import sys
sys.path.append("/data/autoReportV2/")
sys.path.append("/data/autoReportV2/reporter/guanhaowen/pan_cancer/pc/")
from PcClassification.PcModules.PcLevel1_var import PcGet_level1_var
from PcClassification.PcModules.PcLevel2_var import PcGet_level2_var
from PcClassification.PcModules.PcDurg import PcDurg
from PcClassification.PcModules.PcDDR_var import PcDDR_var
from PcClassification.PcModules.PcGermline_var import PcGermline_var
from PcClassification.PcModules.PcOverall import PcOverall
from PcClassification.PcModules.PcImmu_var import PcImmu_var
from PcClassification.PcModules.PcLevel3_var import PcGet_level3_var
from PcClassification.PcModules.PcCoregene import PcCoregene
from PcClassification.PcModules.PcClinicaltrils import PcClinicaltrils
from PcClassification.PcModules.PcMSI import PcGet_MSI
from PcClassification.PcModules.PcTMB import PcGet_TMB
from PcClassification.PcModules.PcPgx import PcChemotherapy
from PcClassification.PcModules.PcSummary import PcSummary
from PcClassification.PcModules.PcBaseclassify import PcBaseclassify
class PcClassification(PcBaseclassify):
    def __init__(self):
        super(PcClassification,self).__init__()     

    @property
    def pgx(self):
        """化疗药结果字典生成

        Returns:
            [dict]: [description]
        """
        _var = PcChemotherapy()
        _var.gvcf = self._gvcf
        _var.chemotherapy_database = self._chemotherapy_database
        return _var.chemo_dict
    
    
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
        _lvl1.durg_name_database = self._durg_name_database
        _lvl1.gene_description = self._gene_description
        _lvl1.var_description = self._var_description
        # --------------*--二级变异处理--*----------------
        _lvl2 = PcGet_level2_var()
        _lvl2.report = self._report
        _lvl2.maf = self._maf
        _lvl2.durg_name_database = self._durg_name_database
        _lvl2.gene_description = self._gene_description
        _lvl2.var_description = self._var_description
        # --------------*--三级变异处理--*-----------------
        _lvl3 = PcGet_level3_var()
        _lvl3.report = self._report
        _lvl3.maf = self._maf
        # ---------------*--靶向药小结相关处理--*----------
        _all_durg = PcOverall()
        _all_durg.report = self._report
        _all_durg.maf = self._maf
        _all_durg.cancer = self._cancer
        _all_durg.nccn_database = self._nccn_database
        # ---------------*--TMB处理--*---------------------
        _tmb = PcGet_TMB()
        _tmb.report = self._report
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
        # ---------------*--胚系变异相关处理--*---------
        _ger = PcGermline_var()
        _ger.report = self._report
        _ger.maf = self._maf
        _ger.durg_name_database = self._durg_name_database
        _ger.gene_list = self._gene_list
        # ---------------*--核心基因相关变异处理--*-------
        _core = PcCoregene()
        _core.maf = self._maf
        _core.gene_list = self._gene_list
        _core.report = self._report
        _core.cancer = self._cancer
        # ---------------*--变异汇总相关处理--*----------
        _sum = PcSummary()
        _sum.report = self._report
        _sum.maf = self._maf
        _sum.durg_name_database = self._durg_name_database
        # ---------------*--诺禾版变异信息相关处理--*----------
        _nova = PcDurg()
        _nova.report = self._report
        _nova.maf = self._maf
        _nova.durg_name_database = self._durg_name_database
        _nova.gene_description = self._gene_description
        _nova.var_description = self._var_description
       
        context = {"level1_var_dict":_lvl1.var_dict.values(),
                "level2_var_dict":_lvl2.var_dict.values(),
                "level1_var_number":_lvl1.number,
                "level2_var_number":_lvl2.number,
                "level3_var_dict":_lvl3.var_dict.values(),
                "level3_var_number":_lvl3.number,
                "durg_overall_var_dict":_all_durg.var_dict.values(),
                "TMB_result":_tmb.tmb[0],
                "TMB_type":_tmb.tmb[1],
                "MSI_type":_msi.msi[0],
                "MSI_score":_msi.msi[1],
                "immu_cli_dict":_immu.immu_clinicaltrials.values(),
                "immu_postive_dict":_immu.immu_postive_dict.values(),
                "immu_negtive_dict":_immu.immu_negtive_dict.values(),
                "immu_supper_dict":_immu.immu_supper_dict.values(),
                "clinical_dict":_cli.clinical_dict.values(),
                "ddr_var_number":_ddr.number,
                "ddr_var_dict":_ddr.var_dict.values(),
                "germline_var_number":_ger.number,
                "germline_var_dict":_ger.var_dict.values(),
                'core_list':_core.var_dict,
                "huizong_dict":_sum.var_dict.values(),
                "nova_dict":_nova.var_dict.values(),
                "cancer":_core.cancer_cn
                }

        return context

var = PcClassification()
var.cancer = 'NSCLC'
var.report = '/data/autoReportV2/reporter/guanhaowen/Sample_R21110452-LXF-LXF.Analyses.xls'
var.maf = '/data/autoReportV2/reporter/guanhaowen/R21110452-LXF-LXF.umi_consensus.oncokb_out'
var.gvcf = '/data/autoReportV2/reporter/guanhaowen/TSVC_variants_IonXpress_001.genome.vcf.gz'
var.msi_out = '/data/autoReportV2/reporter/guanhaowen/20211013cap901-21R83866.msi_15.txt'
print (var.pgx)
print (var.out)


