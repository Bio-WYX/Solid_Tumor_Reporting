from ar.doc.WtComponentFactory import WtComponentFactory
from ar.db.WtDatabase import WtDatabase
from component.database.WtReferencePumdComponent import WtReferencePumdComponent
from component.database.WtToUserComponent import WtToUserComponent
from component.database.WtTestProjectComponent import WtTestProjectComponent
from component.database.WtDetectComponent import WtDetectComponent
from component.database.WtHPVcomprehensiveadviceComponent import WtHPVcomprehensiveadviceComponent
from component.sample_info.WtBasicInfoComponent import WtBasicInfoComponent
from component.sample_info.WtBasicInfoCoverComponent import WtBasicInfoCoverComponent
from component.sample_info.WtWSWbasicinfocoverComponent import WtWSWbasicinfocoverComponent
from component.test_result_db.WtResultsSummaryComponent import WtResultsSummaryComponent
from component.database.WtGeneticCounselingComponent import WtGeneticCounselingComponent
from component.database.WtGeneticSuggestComponent import WtGeneticSuggestComponent
from component.test_result.WtGeneticSangerComponent import WtGeneticSangerComponent
from component.test_result.WtWSWtestresultComponent import WtWSWtestresultComponent
from component.test_result_db.WtTestResultAnalysisComponent import WtTestResultAnalysisComponent
from component.test_result_db.WtTestResultIllInfoComponent import WtTestResultIllInfoComponent
from component.test_result_db.WtBloodTumorResultComponent import WtBloodTumorResultComponent
from component.test_result.WtBloodTumorTestResultComponent import WtBloodTumorTestResultComponent
from component.test_result.WtMedicationAdviceComponent import WtMedicationAdviceComponent
from component.test_result.WtDetectMedicationSuggestComponent import WtDetectMedicationSuggestComponent
from component.test_result_db.WtResultAnalysisComponent import WtResultAnalysisComponent
from component.test_result_db.WtTestResultIllPComponent import WtTestResultIllPComponent
from component.test_result_db.WtTestResultNutritionComponent import WtTestResultNutritionComponent
from component.test_result_db.WtDrugRelevenceGeneOfBigHealthComponent import WtDrugRelevenceGeneOfBigHealthComponent
from component.test_result_db.WtDrugResultAnalysisOfBigHealthComponent import WtDrugResultAnalysisOfBigHealthComponent
from component.test_result_db.WtDrugResultsSummaryOfBigHealthComponent import WtDrugResultsSummaryOfBigHealthComponent
from component.test_result_db.WtNutritionResultsSummaryOfBigHealthComponent import \
    WtNutritionResultsSummaryOfBigHealthComponent
from component.test_result.WtTechnicalParametersComponent import WtTechnicalParametersComponent
from component.test_result.WtHPVtestresultComponent import WtHPVtestresultComponent
from component.test_result.WtNewCrownTestResultsComponent import WtNewCrownTestResultsComponent
from component.test_result.WtTestResultComponent import WtTestResultComponent
from component.test_result_db.WtTestResultDrugComponent import WtTestResultDrugComponent
from component.sample_info.WtHPVbasicinfocoverComponent import WtHPVbasicinfocoverComponent
from component.sample_info.WtHPVbasicinfoComponent import WtHPVbasicinfoComponent
from component.test_result_db.WtDrugRiskComponent import WtDrugRiskComponent
from component.test_result_db.WtNutrientMetabolismComponent import WtNutrientMetabolismComponent
from component.test_result_db.WtDrugGenelndicationsComponent import WtDrugGenelndicationsComponent
from component.test_result_db.WtCardioCerebralVesselsRiskComponent import WtCardioCerebralVesselsRiskComponent
from configs import config
from component.test_result_db.WtBigHealthV2MoveComponent import WtBigHealthV2MoveComponent
from component.test_result_db.WtBigHealthV2SkinComponent import WtBigHealthV2SkinComponent


def initial():
    # component register

    WtComponentFactory().register('basic_info_cover', WtBasicInfoCoverComponent)  # 医检所报告封面上的基本信息
    WtComponentFactory().register('to_user', WtToUserComponent)  # 医检所报告的致用户
    WtComponentFactory().register('test_project', WtTestProjectComponent)  # 医检所报告的主要检测结果
    WtComponentFactory().register('zhan_jiang_project', WtDetectComponent)  # 湛江报告的主要检测结果
    WtComponentFactory().register('basic_info', WtBasicInfoComponent)
    WtComponentFactory().register('results_summary', WtResultsSummaryComponent)
    WtComponentFactory().register('遗传病一代验证', WtGeneticSangerComponent)
    WtComponentFactory().register('genetic_counseling', WtGeneticCounselingComponent)
    WtComponentFactory().register('遗传建议组件', WtGeneticSuggestComponent)
    WtComponentFactory().register('test_result_analysis', WtTestResultAnalysisComponent)
    WtComponentFactory().register('technical_parameters', WtTechnicalParametersComponent)
    WtComponentFactory().register('reference_pumd', WtReferencePumdComponent)
    WtComponentFactory().register('HPV检测结果', WtHPVtestresultComponent)
    WtComponentFactory().register('新冠检测结果', WtNewCrownTestResultsComponent)
    WtComponentFactory().register('HPV封面信息', WtHPVbasicinfocoverComponent)
    WtComponentFactory().register('HPV基本信息', WtHPVbasicinfoComponent)
    WtComponentFactory().register('HPV综合健康建议', WtHPVcomprehensiveadviceComponent)
    WtComponentFactory().register('样本基本信息', WtBasicInfoComponent)
    WtComponentFactory().register('位点信息表格', WtTestResultComponent)
    WtComponentFactory().register('血液肿瘤位点信息表格', WtBloodTumorTestResultComponent)
    WtComponentFactory().register('个体化用药建议', WtMedicationAdviceComponent)
    WtComponentFactory().register('检测药物', WtDetectMedicationSuggestComponent)
    WtComponentFactory().register('相关疾病信息表格', WtTestResultIllInfoComponent)
    WtComponentFactory().register('血液肿瘤结果说明', WtBloodTumorResultComponent)
    WtComponentFactory().register('位点详细解析', WtResultAnalysisComponent)
    WtComponentFactory().register('相关疾病信息段落', WtTestResultIllPComponent)
    WtComponentFactory().register('测序参数', WtTechnicalParametersComponent)
    WtComponentFactory().register('用药基因检测结果', WtTestResultDrugComponent)
    WtComponentFactory().register('营养与代谢基因检测结果', WtTestResultNutritionComponent)
    WtComponentFactory().register('大健康用药与基因的相关性', WtDrugRelevenceGeneOfBigHealthComponent)
    WtComponentFactory().register('检测结果分析', WtDrugResultAnalysisOfBigHealthComponent)
    WtComponentFactory().register('大健康药物反应风险结果小结', WtDrugResultsSummaryOfBigHealthComponent)
    WtComponentFactory().register('大健康营养与代谢特征结果小结', WtNutritionResultsSummaryOfBigHealthComponent)
    WtComponentFactory().register('微生物封面信息', WtWSWbasicinfocoverComponent)
    WtComponentFactory().register('微生物检测结果', WtWSWtestresultComponent)
    WtComponentFactory().register('HPV综合健康建议', WtHPVcomprehensiveadviceComponent)
    WtComponentFactory().register('药物反应性风险', WtDrugRiskComponent)
    WtComponentFactory().register('营养与代谢特征', WtNutrientMetabolismComponent)
    WtComponentFactory().register('药物反应性风险检测结果分析', WtDrugGenelndicationsComponent)
    WtComponentFactory().register('心脑血管风险', WtCardioCerebralVesselsRiskComponent)
    WtComponentFactory().register('大健康V2皮肤概述表格', WtBigHealthV2SkinComponent)
    WtComponentFactory().register('大健康V2运动', WtBigHealthV2MoveComponent)

    import importlib
    from ar.db.WtDatabaseInstance import db
    array_db = db.get_table("报告模板配置", "模块配置").get()
    for dist_db in array_db:
        mokuai_type = dist_db["类型"]
        mokuai_project_name = dist_db["模块-类"]
        mokuai_word_name = dist_db["模块-报告"]
        mokuai_project_module = importlib.import_module("component." + mokuai_type + "." + mokuai_project_name)
        mokuai_project = getattr(mokuai_project_module, mokuai_project_name)
        WtComponentFactory().register(mokuai_word_name, mokuai_project)

    default_db_config = {
        'mysql': {
            'host': '192.168.0.102',
            'user': '***',
            'passwd': '***',
            'db': 'ar',
            'port': 3307,
            'charset': 'utf8'
        },
        'api': {
            'url': 'http://127.0.0.1:8016/api/v1/web'
        }
    }

    db_type = config.db_type

    WtDatabase().instance(db_type, {**default_db_config[db_type], **config.db_config[db_type]})