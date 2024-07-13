import sys
#sys.path.append("/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/pc")
from PcClassificationHome.PcModules.PcBaseclassify import PcBaseclassify
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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
        _df.drop(_df.columns[[0, 1]], axis=1, inplace=True)
        _df = _df[_df['FILTER']=="PASS"]
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
       
        #################
        # 作图
        #################
        if self._cancer == 'Esophagogastric Cancer':
            _cancer = 'NSCLC'
        else:
            _cancer = self._cancer
        tmb1 = pd.read_excel(self._tmb_database,sheet_name=_cancer)
        tmb = tmb1[['Tumor_Sample_Barcode', 'TB_num']]
        cutoff = tmb.quantile(q=0.75)
        pic_hight_dict = {"Colorectal Cancer":0.05,
                     "NSCLC":0.1,
                     "Breast Cancer":0.16,
                     "HCC":0.16,
                     "Esophagogastric Cancer": 0.1   
                     }
        pic_hight = pic_hight_dict[_cancer]
        plt.xlim(0,150)
        sns.kdeplot(tmb['TB_num'],fill=True,common_norm=False, palette="crest", alpha=.5, color='blue')
        plt.vlines(float(TMB_result),0,0.05,colors='r',linestyles='dashed')
        plt.vlines(cutoff,0,0.05,colors='black',linestyles='dashed')
        plt.savefig(self._tmb_png,format='png')
        # plt.show()
        if float(TMB_result) > float(cutoff):
                TMB_type = "TMB-H"
        elif float(TMB_result) < float(cutoff):
            TMB_type = "TMB-L"
        # print(TMB_result,TMB_type)
        return TMB_result,TMB_type

if __name__== "__main__":
    var = PcGet_TMB()
    var.tmb_database = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/dependent/database/TMB_baseline.xlsx"
    var.report = "/Users/guanhaowen/Desktop/pancancer_data/20220422/03/Sample_tumorANN20220418-1-SP20416W03.Analyses.xls"
    var.tmb_png = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试数据/诺禾数据/tmb_test.png"
    var.cancer = "Colorectal Cancer"
    # var.cancer = "NSCLC"
    # var.cancer = "Breast Cancer"
    # var.cancer = "HCC"
    # var.cancer = "Esophagogastric Cancer"
    print(var.tmb)