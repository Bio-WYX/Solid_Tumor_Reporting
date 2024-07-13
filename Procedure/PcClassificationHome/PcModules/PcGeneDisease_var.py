import sys
sys.path.append("/mnt/e/ansaisi/641panel/pan_cancer/pc")
from PcClassificationHome.PcModules.PcBaseclassify import PcBaseclassify
from PcClassificationHome.PcFuctions.PcTranslate import Translate
from functools import partial
import pandas as pd
import seaborn as sns


class PcGet_GeneDisease(PcBaseclassify):
    def __init__(self):
        super(PcGet_GeneDisease, self).__init__()

    @property
    def ge_disease(self):
        _df = pd.read_excel(self._result, sheet_name="variant")
        _gene_d = pd.read_excel(self._gene_disease, sheet_name="基因")
        _dis_d = pd.read_excel(self._gene_disease, sheet_name="疾病")
        _gene_d.fillna('', inplace=True)
        _dis_d.fillna('', inplace=True)

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
        _df_c = _df_dis['HGVSc'].str.extract('N.*:(?P<c>c.*)', expand=True)
        _df_p = _df_dis['HGVSp'].str.extract('N.*:(?P<p>p.*)', expand=True)
        _df_e = _df_dis['EXON'].str.extract('Exon\s+(?P<exon_e>\d+)\/\d+', expand=True)
        _df_n = _df_dis['EXON'].str.extract('Exon\s+\d+\/(?P<exon_n>\d+)', expand=True)
        #_df_chr = _df_dis['Allele'].str.extract('(?P<chr>chr.*):\d+:.*', expand=True)
        #_df_dis.insert(loc=len(_df_dis.columns), column='chr', value=_df_chr['chr'])
        _df_dis.insert(loc=len(_df_dis.columns), column='c', value=_df_c['c'])
        _df_dis.insert(loc=len(_df_dis.columns), column='p', value=_df_p['p'])
        _df_dis.insert(loc=len(_df_dis.columns), column='exon_e', value=_df_e['exon_e'])
        _df_dis.insert(loc=len(_df_dis.columns), column='exon_n', value=_df_n['exon_n'])
        _df_dis['杂合性'] = ''
        _df_dis.loc[_df_dis[_df_dis.AF >= 80].index.tolist(), '杂合性'] = '纯和'
        _df_dis.loc[_df_dis[_df_dis.AF < 80].index.tolist(), '杂合性'] = '杂合'
        _df_dis1 = _df_dis.groupby(['SYMBOL', '杂合性']).size().reset_index(name='计数')
        _df_merge = pd.merge(_df_dis, _df_dis1, on=['SYMBOL', '杂合性'], how="left")
        _df_dis = _df_merge

        ######基因对应数据库整理######
        _df_gene = _gene_d[_gene_d['基因名称'].isin(_df_dis['SYMBOL'].tolist())]
        match_chr = _df_gene['染色体位置'].str.extract('(?P<chr>[\d+|X|Y])[p|q].*', expand=True)
        match_pos = _df_gene['染色体位置'].str.extract('[\d+|X|Y](?P<pos>[p|q].*)', expand=True)
        _df_gene.insert(loc=len(_df_gene.columns), column='chr', value=match_chr['chr'])
        _df_gene.insert(loc=len(_df_gene.columns), column='pos', value=match_pos['pos'])
        _df_gene.rename(columns={'基因名称': 'SYMBOL'}, inplace=True)
        _df_merge = pd.merge(_df_dis, _df_gene, on=['SYMBOL'], how="left")
        _df_dis = _df_merge

        ######生成字典######
        _df_dis['Index'] = _df_dis['Allele']
        _df_dis.set_index(['Index'], inplace=True)
        self._gene_dis_dict = _df_dis.T.to_dict()

        ######疾病对应数据库整理######
        _df_ea_dis = _dis_d[_dis_d['基因名称'].isin(_df_dis['SYMBOL'].tolist())]
        # _df_ea_dis.rename(columns={'基因名称': 'SYMBOL'}, inplace=True)
        # _df_merge = pd.merge(_df_dis, _df_ea_dis, on=['SYMBOL'], how="right")
        _df_ea_dis['Index'] = _df_ea_dis['index']
        _df_ea_dis.set_index(['Index'], inplace=True)
        tmp_dict = _df_ea_dis.T.to_dict()
        for key1 in self._gene_dis_dict.keys():
            tmp = []
            for key2 in tmp_dict.keys():
                if tmp_dict[key2]['基因名称'] == self._gene_dis_dict[key1]['SYMBOL']:
                    tmp.append(tmp_dict[key2])
                else:
                    continue
            self._gene_dis_dict[key1]['疾病'] = tmp

        return self._gene_dis_dict

    @property
    def ge_unknown(self):
        unk_add = {'VUS1':'临床意义未明1级（VUS1）', 'VUS2':'临床意义未明2级（VUS2）', 'VUS3':'临床意义未明3级（VUS3）', \
                   '良性':'良性', '可能良性':'可能良性'}
        _df = pd.read_excel(self._result, sheet_name="variant")
        _gene_d = pd.read_excel(self._gene_disease, sheet_name="基因")
        _dis_d = pd.read_excel(self._gene_disease, sheet_name="疾病")

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
        #_df_chr = _df_unk['Allele'].str.extract('(?P<chr>chr.*):\d+:.*', expand=True)
        _df_c = _df_unk['HGVSc'].str.extract('N.*:(?P<c>c.*)', expand=True)
        _df_p = _df_unk['HGVSp'].str.extract('N.*:(?P<p>p.*)', expand=True)
        _df_e = _df_unk['EXON'].str.extract('Exon\s+(?P<exon_e>\d+)\/\d+', expand=True)
        _df_n = _df_unk['EXON'].str.extract('Exon\s+\d+\/(?P<exon_n>\d+)', expand=True)
        #_df_unk.insert(loc=len(_df_unk.columns), column='chr', value=_df_chr['chr'])
        _df_unk.insert(loc=len(_df_unk.columns), column='c', value=_df_c['c'])
        _df_unk.insert(loc=len(_df_unk.columns), column='p', value=_df_p['p'])
        _df_unk.insert(loc=len(_df_unk.columns), column='exon_e', value=_df_e['exon_e'])
        _df_unk.insert(loc=len(_df_unk.columns), column='exon_n', value=_df_n['exon_n'])
        _df_unk['杂合性'] = ''
        _df_unk.loc[_df_unk[_df_unk.AF >= 80].index.tolist(),'杂合性'] = '纯和'
        _df_unk.loc[_df_unk[_df_unk.AF < 80].index.tolist(), '杂合性'] = '杂合'
        _df_unk1 = _df_unk.groupby(['SYMBOL', '杂合性']).size().reset_index(name='计数')
        _df_merge = pd.merge(_df_unk, _df_unk1, on=['SYMBOL', '杂合性'], how="left")
        _df_unk = _df_merge

        ######基因对应数据库整理######
        _df_gene = _gene_d[_gene_d['基因名称'].isin(_df_unk['SYMBOL'].tolist())]
        match_chr = _df_gene['染色体位置'].str.extract('(?P<chr>[\d*|X|Y])[p|q].*', expand=True)
        match_pos = _df_gene['染色体位置'].str.extract('[\d*|X|Y](?P<pos>[p|q].*)', expand=True)
        _df_gene.insert(loc=len(_df_gene.columns), column='chr', value=match_chr['chr'])
        _df_gene.insert(loc=len(_df_gene.columns), column='pos', value=match_pos['pos'])
        _df_gene.rename(columns={'基因名称': 'SYMBOL'}, inplace=True)
        _df_merge = pd.merge(_df_unk, _df_gene, on=['SYMBOL'], how="left")
        _df_unk = _df_merge

        ######生成字典######
        _df_unk['Index'] = _df_unk['Allele']
        _df_unk.set_index(['Index'], inplace=True)
        self._gene_unk_dict = _df_unk.T.to_dict()

        ######疾病对应数据库整理######
        # _df_un_dis = _dis_d[_dis_d['基因名称'].isin(_df_unk['SYMBOL'].tolist())]
        # _df_un_dis.rename(columns={'基因名称': 'SYMBOL'}, inplace=True)
        # _df_merge = pd.merge(_df_unk, _df_un_dis, on=['SYMBOL'], how="right")
        # _df_un_dis = _df_merge
        # _df_un_dis['Index'] = _df_un_dis['OMIM']
        # _df_un_dis.set_index(['Index'], inplace=True)
        # self._gene_unk_dict = _df_un_dis.T.to_dict()

        _df_un_dis = _dis_d[_dis_d['基因名称'].isin(_df_unk['SYMBOL'].tolist())]
        _df_un_dis['Index'] = _df_un_dis['OMIM']
        _df_un_dis.set_index(['Index'], inplace=True)
        tmp_dict = _df_un_dis.T.to_dict()

        for key1 in self._gene_unk_dict.keys():
            tmp = []
            for key2 in tmp_dict.keys():
                if tmp_dict[key2]['基因名称'] == self._gene_unk_dict[key1]['SYMBOL']:
                    tmp.append(tmp_dict[key2])
                else:
                    continue
            self._gene_unk_dict[key1]['疾病'] = tmp
        #print (self._gene_unk_dict)
        return self._gene_unk_dict


if __name__ == "__main__":
    var = PcGet_GeneDisease()
    var.result = '/mnt/e/ansaisi/641panel/Sample_tumorANN20220418-1-SP20416W04.Analyses-筛.xls'
    var.gene_disease = '/mnt/e/ansaisi/641panel/pan_cancer/dependent/database/基因-疾病_医检所遗传病.xlsx'

    #var.ge_disease
    var.ge_unknown
