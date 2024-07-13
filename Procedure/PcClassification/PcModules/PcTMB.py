import sys
sys.path.append("/data/autoReportV2/")
sys.path.append("/data/autoReportV2/reporter/guanhaowen/pan_cancer/pc/")
from PcClassification.PcModules.PcBaseclassify import PcBaseclassify
import pandas as pd



class PcGet_TMB(PcBaseclassify):
    def __init__(self):
        super(PcGet_TMB, self).__init__()
    def substr(element):
        #替换列中的"-"
        if element == "-":
            element = 0
        else:
            pass
        return element
    @property
    def tmb(self):
        _df = pd.read_excel(self._report, sheet_name = "variant")
        #黑名单 SCZ算法
        # _df_b = pd.read_excel(blacklist)
        # _df = _df[~_df["HGVSp"].isin(_df_b["HGVSp"])]
        _df = _df[_df["rmsk"]=="-"]
        #区域及变异类型筛选外显子区域的体细胞非同义突变
        _df = _df[(_df['Consequence']=="missense_variant") & (_df["EXON"]!="-")]
        #筛选突变频率大于5，覆盖深度大于60的位点，并过滤掉dbSNP（胚系）以及Cosmic（驱动基因）中出现的位点。
        _df = _df[(_df['AlterRatio(%)'] > 10) & (_df['CoverageDepth'] > 60) & (_df['Existing_variation']=="-")] #& (_df['Cosmic']=="-")]
        _df = _df[_df["Existing_variation"] == "-"]
        #过滤掉出现在Gnomad数据库中（东亚人群）并且突变频率大于0.01%的位点。
        _df['GnomadWES_AF_EAS'] = _df['GnomadWES_AF_EAS'].replace("-",0)
        _df = _df[(_df['Gnomad_AF_EAS'] < 0.0001)]
        # _df['GnomadWES_AF_EAS'].replace("-",0, inplace=True)
        _df = _df[_df['GnomadWES_AF_EAS'].map(lambda x: x < 0.0001)]
        #过滤掉出现在千人基因组数据库中东亚人群频率中大于0.01%的位点。
        if _df.shape == (0,0):
            TMB_result = 0
        else:
            _df['1KG_EAS_AF'] = _df['1KG_EAS_AF'].replace("-",0)
            # _df['1KG_EAS_AF'].replace("-",0,inplace=True)
            _df = _df[_df['1KG_EAS_AF'] < 0.0001]
            #过滤掉ChinaMap数据库中的人群频率大于0.01%的位点
            _df['ChinaMap_AF'] = _df['ChinaMap_AF'].replace("-",0)
            _df = _df[_df['ChinaMap_AF'].map(lambda x: x < 0.0001)]
            TMB_result = _df.shape[0] / 2.2
            TMB_result = '%.2f' % TMB_result
        if float(TMB_result) > 10:
            TMB_type = "TMB-H"
        elif float(TMB_result) < 10:
            TMB_type = "TMB-L"
        return TMB_result,TMB_type

