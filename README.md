# Solid_Tumor_Reporting

## 脚本介绍

- 主程序：`main.py`

- PcInfo模块：PcInfo
  
  - PcInfo.py #*读取临床信息、输入文件路径（网页输入），存储为字典并返回结果*

- PcDatabase模块：PcDatabase
  
  - PcDatabase.py #*读取数据库内容，并转化为excel文件保存（数据库内容详见数据库介绍部分）*

- PcPreprocess模块：PcPreprocess
  
  - PcPreBaseinit.py #*PcInfo模块传入的输入文件载入程序*
  
  - PcPreprocessScript.py #*调用oncokb api对maf文件进行注释；根据mode号提取癌种信息*

- oncokb模块：oncokb
  
  - MafAnnotator.py #*oncokb api突变位点注释脚本*
  
  - FusionAnnotator.py #*oncokb api融合基因注释脚本*

- PcClassification模块：PcClassificationHome
  
  - PcClassification.py #*程序传入参数转化*
  
  - PcBaseclassify.py #*载入输入数据与数据库文件；检查文件格式是否正确*
  
  - PcClinicaltrils.py #*检索”实体瘤-clinicaltrails“数据库对应的变异位点信息*
  
  - PcCoregene.py #*筛选癌种对应关注的基因*
  
  - PcDDR_var.py #*检索”实体瘤-genelist“数据库并分析DDR与MSH对应的变异位点*
  
  - PcDisease_var.py #*解析变异注释结果，统计致病位点*
  
  - PcDurg.py #*检索”实体瘤-药物名称“数据库并分析突变位点与用药药物信息*
  
  - PcGeneDisease_var.py #*检索”实体瘤-Gene_description“与”实体瘤-药物名称“数据库，分析变异位点的突变与与用药信息*
  
  - PcGermline_var.py #*检索”实体瘤-genelist“数据库并分析不同癌种遗传易感基因*
  
  - PcImmu_var.py #*检索”实体瘤-免疫“数据库并分析突变位点关联的免疫信息*
  
  - PcLevel1_var.py #*一级变异位点筛选及相关数据库信息注释*
  
  - PcLevel2_var.py #*二级变异位点筛选及相关数据库信息注释*
  
  - PcLevel3_var.py #*三级变异位点筛选及相关数据库信息注释*
  
  - PcMSI.py #*MSI结果计算*
  
  - PcOverall.py #*检索”实体瘤-NCCN“数据库及变异位点信息注释*
  
  - PcPgx_new.py #*检索”实体瘤-化疗药“数据库及化疗药相关位点信息注释和整合（解析gvcf文件）*
  
  - PcQC.py #*质控相关的信息整合*
  
  - PcSummary.py #*检索”实体瘤-药物名称“数据库并翻译*
  
  - PcSv.py #*融合基因变异的注释和筛选*
  
  - PcTMB.py #*进行TMB计算，并作图*

## 数据库介绍

- 实体瘤-clinicaltrails
  
  - ClinicalTrails数据库，链接地址：[clinicaltrails](https://clinicaltrials.gov/)
  
  - 数据库下载及整理：雅楠

- 实体瘤-Gene_description
  
  - 基因及描述
  - 数据下载及整理：[oncokb数据库](https://www.oncokb.org/)搜索基因并查看描述，翻译后由医学部核对

- 实体瘤-genelist
  
  - 基因列表及分类
  - 不同类型的基因列表

- 实体瘤-NCCN
  
  - 致病基因描述、用药指南
  
  - NCCN指南描述，链接地址：[NCCN](http://www.nccnchina.org.cn/nccn-guidelines-china.aspx)

- 实体瘤-TMB
  
  - 不同癌种的TB_num
  
  - TCGA数据库：[TCGA]([Center for Cancer Genomics - NCI](https://www.cancer.gov/ccg/))

- 实体瘤-变异注释
  
  - 变异位点描述
  - 文献报道等总结：[COSMIC]([COSMIC | Catalogue of Somatic Mutations in Cancer](https://cancer.sanger.ac.uk/cosmic))

- 实体瘤-化疗药
  
  - 化疗药物用药描述
  - 化疗药数据库：[pharmgkb](https://www.pharmgkb.org/)

- 实体瘤-免疫
  
  - 免疫治疗研究报道
  - 免疫治疗数据库：[clinicaltrials](https://clinicaltrials.gov/)

- 实体瘤-药物名称
  
  - 变异及致病性描述翻译对照

- 实体瘤-医检所遗传病
  
  - 基因区域对应的疾病描述

- 实体瘤-预后计算
  
  - 预后计算结果数据库，计算网址链接：[Kaplan-Meier plotter](http://kmplot.com/analysis/)
  
  ------------------------------------------------------------------------------------------------------------------------
  
  

 附件 

- 生成报告流程

- LIS系统生成报告

- 报告类别：
  
  - 实体瘤-医检所

- 报告模板：
  
  - 妇科肿瘤
  
  - 结直肠癌
  
  - 肺癌
  
  - 肝癌
  
  - 食道癌

- 上传所需文件：
  
  - 标准注释解读结果Excel（.xlsx）
  
  - gvcf文件（.g.vcf.gz）
  
  - 微卫星不稳定性检测结果msi.txt文件（.msi.txt）
  
  - MAF原始文件（.maf）
  
  - cnv检测结果文件（暂时不分析，文件只作占位）
  
  - 融合基因检测结果文件（.fusion.json）
  
  - 测序数据质控结果文件（.json）
  
  - 数据比对结果文件（coverage.report）
