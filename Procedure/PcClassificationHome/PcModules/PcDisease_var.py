import sys

sys.path.append("/mnt/e/ansaisi/641panel/pan_cancer/pc")
from PcClassificationHome.PcModules.PcBaseclassify import PcBaseclassify
from PcClassificationHome.PcFuctions.PcTranslate import Translate
from functools import partial
import pandas as pd
import seaborn as sns


class PcGet_Disease(PcBaseclassify):
    def __init__(self):
        super(PcGet_Disease, self).__init__()

    @property
    def disease(self):
        _df = pd.read_excel(self._result, sheet_name="variant")
        ######筛选人群频率######
        #_df = _df[_df['Gnomad_AF_POPMAX'] <= 0.01]

        ######解读结果处理######
        _df = _df.dropna(axis=0, subset=["致病性"])
        _df.致病性 = _df.致病性.astype(str)
        _df_dis = _df[_df['致病性'].str.contains('致病')]
        _df_dis = _df_dis.sort_values(by = '致病性', ascending = False)
        _df_dis["AF"] = _df_dis["AlterRatio(%)"].map(lambda x: round(x/1, 4))
        translate_clinvar = partial(Translate().translate_clinvar, DURG_NAME_DATABASE=self.durg_name_database)
        translate_consequence_1 = partial(Translate().translate_consequence, DURG_NAME_DATABASE=self.durg_name_database)
        _df_dis['Consequence_cn'] = _df_dis["Consequence"].apply(translate_consequence_1)
        _df_dis["ClinVar_CLNSIG"] = _df_dis["ClinVar_CLNSIG"].apply(translate_clinvar)
        _df_dis["ClinVar_CLNSIG"] = _df_dis["ClinVar_CLNSIG"].astype('category')
        _df_chr = _df_dis['Allele'].str.extract('(?P<chr>chr.*):\d+:.*', expand=True)
        _df_dis.insert(loc=len(_df_dis.columns), column='chr', value=_df_chr['chr'])

        #_df_dis.rename(columns={'SYMBOL': 'SYMBOL_m'}, inplace=True)
        _df_dis['Index'] = _df_dis['Allele']
        _df_dis.set_index(['Index'], inplace=True)
        self._dis_dict = _df_dis.T.to_dict()

        return self._dis_dict

    @property
    def unknown(self):
        unk_add = {'VUS1':'临床意义未明1级（VUS1）', 'VUS2':'临床意义未明2级（VUS2）', 'VUS3':'临床意义未明3级（VUS3）', \
                   '良性':'良性', '可能良性':'可能良性'}
        _df = pd.read_excel(self._result, sheet_name="variant")
        ######筛选人群频率######
        #_df = _df[_df['Gnomad_AF_POPMAX'] <= 0.01]

        ######解读结果处理######
        _df = _df.dropna(axis=0, subset=["致病性"])
        _df.致病性 = _df.致病性.astype(str)
        _df_unk = _df[_df['致病性'].str.contains('VUS|良性')]
        _df_unk['致病性_add'] = _df_unk['致病性'].apply(lambda x: unk_add[x])
        _df_unk = _df_unk.sort_values(by="致病性", ascending=True)
        _df_unk["AF"] = _df_unk["AlterRatio(%)"].map(lambda x: round(x/1, 4))
        translate_clinvar = partial(Translate().translate_clinvar, DURG_NAME_DATABASE=self.durg_name_database)
        translate_consequence_1 = partial(Translate().translate_consequence, DURG_NAME_DATABASE=self.durg_name_database)
        _df_unk['Consequence_cn'] = _df_unk["Consequence"].apply(translate_consequence_1)
        _df_unk["ClinVar_CLNSIG"] = _df_unk["ClinVar_CLNSIG"].apply(translate_clinvar)
        _df_unk["ClinVar_CLNSIG"] = _df_unk["ClinVar_CLNSIG"].astype('category')
        _df_chr = _df_unk['Allele'].str.extract('(?P<chr>chr.*):\d+:.*', expand=True)
        _df_unk.insert(loc=len(_df_unk.columns), column='chr', value=_df_chr['chr'])

        #_df_unk.rename(columns={'SYMBOL': 'SYMBOL_m'}, inplace=True)
        _df_unk['Index'] = _df_unk['Allele']
        _df_unk.set_index(['Index'], inplace=True)
        self._unk_dict = _df_unk.T.to_dict()

        return self._unk_dict


if __name__ == "__main__":
    var = PcGet_Disease()
    var.result = '/mnt/e/ansaisi/641panel/Sample_tumorANN20220418-1-SP20416W04.Analyses-筛.xls'
    var.disease
    var.unknown
