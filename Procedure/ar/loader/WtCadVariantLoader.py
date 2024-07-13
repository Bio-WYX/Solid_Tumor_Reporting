import xlrd

from ar.common.WtArError import WtArError
from ar.loader.WtVariantInfoLoader import WtVariantSubLoader, WtVariantInfoLoader


class WtCADVariantInfoFromExcel(WtVariantInfoLoader):
    def __init__(self):
        super().__init__()
        self.pgx_info = None
        self.cad_info = None
        self.coverage_info = None

    def get(self, code):
        data = super().get(code)
        if not data:
            return None
        data.update({
            'pgx': self.pgx_info,
            'cad': self.cad_info,
            'coverage': self.coverage_info,
        })

        return data

    def enumerate(self):
        for item in self.data:
            yield {
                'variant': item,
                'pgx': self.pgx_info,
                'cad': self.cad_info,
                'coverage': self.coverage_info,
            }

    def load(self, file, loader_config):
        default_loader = {
            'pgx_loader': WtPgxInfoFromExcel(),
            'cad_loader': WtCadInfoFromExcel(),
            'coverage_loader': WtCoverageInfoFromExcel(),
            'mutation_loader': WtJudgeVariantInfoFromExcel(),
        }

        default_loader.update(loader_config)

        xlsx = xlrd.open_workbook(file)

        self.pgx_info = default_loader.get('pgx_loader').load(xlsx)
        self.cad_info = default_loader.get('cad_loader').load(xlsx)
        self.coverage_info = default_loader.get('coverage_loader').load(xlsx)
        self.data = default_loader.get('mutation_loader').load(xlsx)


class WtJudgeVariantInfoFromExcel(WtVariantSubLoader):
    def load(self, xlsx):
        annotation = ['人工注释', '疾病判读']
        dist_list = []
        table = xlsx.sheet_by_name("judge-variant")
        nrows = table.nrows
        head = table.row_values(0)
        title = list(set(head).intersection(set(annotation)))  # 两个数组的交集，说明既是需要的，同时也在head中，这部分需要单独写
        for i in range(1, nrows):
            array = table.row_values(i)
            exon = array[head.index("EXON")]
            intron = array[head.index("INTRON")]
            sample = array[head.index("SAMPLE")]
            EXON_num = int(exon.replace('Exon ', '').split('/')[0]) if exon != '-' else 0
            INTRON_num = int(intron.replace('Intron ', '').split('/')[0]) if intron != '-' else 0
            temp_dict = {"bg": "ffffff" if i % 2 else 'f1f1f1',
                         'code': sample,
                         "sample": sample,
                         "gene": array[head.index("SYMBOL")],
                         "sequence": str(array[head.index("HGVSc")]).split(":")[0],
                         "chr_site": str(array[head.index("Allele")]).split(":")[0] + ":" +
                                     str(array[head.index("Allele")]).split(":")[1],
                         "nuc": str(array[head.index("HGVSc")]).split(":")[1] if array[head.index(
                             "HGVSc")] != '-' else '-',  # 核苷酸变异
                         "pep": str(array[head.index("HGVSp")]).split(":")[1] if array[head.index(
                             "HGVSp")] != '-' else '-',  # 氨基酸变异
                         "exon": exon,
                         'consequence': array[head.index("Consequence")],
                         "intron": intron,
                         "tran": array[head.index("Feature")],  # 转录本
                         "EXON_num": EXON_num,
                         "INTRON_num": INTRON_num,
                         "Heterozygosity":'杂合' if EXON_num > INTRON_num else '纯合'
                         }
            temp_ann = ''
            temp_pre = ''
            for item in title:
                temp_dict[item] = array[head.index(item)]
                if '注释' in item:
                    temp_ann = array[head.index(item)]
                if '判读' in item:
                    temp_pre = array[head.index(item)]

            if temp_ann == "" or temp_ann == "良性" or temp_ann == "可能良性" or temp_pre == '':
                continue
            dist_list.append(temp_dict)

        return dist_list


class WtCoverageInfoFromExcel(WtVariantSubLoader):
    def load(self, xlsx):
        if 'coverage' not in xlsx.sheet_names():
            return None
        table = xlsx.sheet_by_name("coverage")
        nrows = table.nrows
        head = table.row_values(0)
        dist = {}
        for i in range(1, nrows):
            array = table.row_values(i)
            if (array[0] == ""):
                break
            dist[array[0]] = array[1]
        return {
            "target_region": dist["TargetRegionSize:"],
            "covrage_depth": dist["AverageDepth:"],
            "covrage_4": dist["CoverageRatio(Depth >= 4 X):"],
            "covrage_20": dist["CoverageRatio(Depth >= 20 X):"],
            "covrage_30": dist["CoverageRatio(Depth >= 30 X):"]
        }


class WtPgxInfoFromExcel(WtVariantSubLoader):
    def load(self, xlsx):
        """
        :param xlsx:
        :return:
        """
        table = xlsx.sheet_by_name("pgx")
        nrows = table.nrows
        head = table.row_values(0)
        pgx_list = []

        first_row = table.row_values(2)
        suggest_list = [table.row_values(i)[head.index("用药建议")] for i in range(1, nrows) if table.row_values(i)[head.index("用药建议")]!='']
        pgx_dict = {}
        for i in range(1, nrows):
            row = table.row_values(i)
            if first_row[0] != row[0]:
                first_row = row
            else:
                for idx,value in enumerate(row):
                    if row[idx] == '':
                        row[idx] = first_row[idx]

            dict = {
                'drug': row[head.index("药物名称")],
                'suggest':row[head.index("用药建议")],
                'gene':row[head.index("相关基因")],
                'rs':row[head.index("rs")],
                'gene_type':row[head.index("检测结果")],
                'gene_fenxing':row[head.index('基因分型')],
                'ref_seq':row[head.index('参考序列')],
                'site':row[head.index('检测位点')]
            }
            pgx_list.append(dict)
            if dict['drug'] not in pgx_dict:
                pgx_dict[dict['drug']] = []
                pgx_dict[dict['drug']].append(dict)
            else:
                pgx_dict[dict['drug']].append(dict)


        return {
            'suggest': suggest_list,
            'pgx_list': pgx_list,
            'pgx_dict': pgx_dict
        }


class WtCadInfoFromExcel(WtVariantSubLoader):
    def load(self, xlsx):
        """
        :param xlsx:
        :return:
        """
        table = xlsx.sheet_by_name("cad")
        nrows = table.nrows
        head = table.row_values(4)
        risk = table.row_values(2)[1] if table.row_values(2)[1] != "" else -1
        cad_list = []
        for i in range(5, nrows):  # 因为cad的数据是从第五行开始的
            row = table.row_values(i)
            cad = {
                "bg": "ffffff" if i % 2 else 'f1f1f1',  # 背景颜色
                "site_num": row[0],
                "allele": row[1],
                "gene": str(row[2]).replace("&", ","),
                "gene_type": row[3],
            }
            cad_list.append(cad)

        return {
            'cad_list': cad_list,
            'risk': risk,
        }
