import xlrd

from ar.loader.WtVariantInfoLoader import WtVariantInfoLoader


class WtBloodVariantLoader(WtVariantInfoLoader):
    @staticmethod
    def getAllele(Allele):
        dic_allele = {
            'chr_id': Allele.split(':')[0],
            'chr_position': Allele.split(':')[1],
            'chr_all': Allele
        }
        return dic_allele

    @staticmethod
    def getHGVSc(HGVSc):
        dic_hgvsc = {
            'nuc': HGVSc.split(':')[-1],
            'hgvsc': HGVSc
        }
        return dic_hgvsc

    @staticmethod
    def getHGVSp(HGVSp):
        dic_hgvsp = {
            'pep': HGVSp.split(':')[-1],
            'hgvsp': HGVSp
        }
        return dic_hgvsp

    @staticmethod
    def getEXON(EXON):
        if EXON != '-':
            dic_exon = {
                'EXON_num': EXON.split()[-1].split('/')[0],
                'EXON_all': EXON.split()[-1].split('/')[1]
            }
        else:
            dic_exon = {
                'EXON_num': '-',
                'EXON_all': '-'
            }
        return dic_exon

    @staticmethod
    def getINTRON(INTRON):
        if INTRON != '-':
            dic_intron = {
                'INTRON_num': INTRON.split()[-1].split('/')[0],
                'INTRON_all': INTRON.split()[-1].split('/')[1]
            }
        else:
            dic_intron = {
                'INTRON_num': '-',
                'INTRON_all': '-'
            }
        return dic_intron

    def getSpecialTitle(self, Title, Detail):
        if Title == 'Allele':
            return self.getAllele(Detail)
        elif Title == 'HGVSc':
            return self.getHGVSc(Detail)
        elif Title == 'HGVSp':
            return self.getHGVSp(Detail)
        elif Title == 'EXON':
            return self.getEXON(Detail)
        elif Title == 'INTRON':
            return self.getINTRON(Detail)
        elif Title == 'SAMPLE':
            return str(Detail).replace(".0", "")
        else:
            pass

    @staticmethod
    def openSheet(inputfile, sheetName):
        table = inputfile.sheet_by_name(sheetName)
        getinput = {
            'table': inputfile.sheet_by_name(sheetName),
            'head': table.row_values(0),
            'nrows': table.nrows
        }
        return getinput

    def load(self, variantInput, loader_config):
        NGS_info = {}
        if variantInput["customFiles"]["inputPath"] != "":
            inputXlsx = variantInput["customFiles"]["inputPath"]
            excel = xlrd.open_workbook(inputXlsx)
            sheet_names = excel.sheet_names()
            # ===>get judge-variant info<====
            special_col = ['人工致病性注释', '人工排序', 'SAMPLE', 'Allele', 'HGVSc', 'HGVSp', 'EXON', 'INTRON']
            for sheet_name in sheet_names:
                if sheet_name == "judge-variant":
                    judge_variant = self.openSheet(excel,'judge-variant')
                    variant_table = judge_variant['table']
                    variant_nrows = judge_variant['nrows']
                    variant_head = judge_variant['head']
                    for i in range(1, variant_nrows):
                        Dict_NGS = {}
                        line = variant_table.row_values(i)
                        for title in variant_head:
                            if title not in special_col:
                                Dict_NGS[title] = line[variant_head.index(title)]
                            else:
                                if title in special_col[3:]:
                                    Dict_NGS[title] = self.getSpecialTitle(title,line[variant_head.index(title)])
                                else:
                                    pass
                        SAMPLE = self.getSpecialTitle('SAMPLE',line[variant_head.index('SAMPLE')])
                        Pathogenicity = line[variant_head.index('人工致病性注释')]
                        SortNumber = line[variant_head.index('人工排序')]
                        NGS_info.setdefault('code', SAMPLE)
                        NGS_info.setdefault('judge-variant',{})
                        NGS_info['judge-variant'].setdefault(Pathogenicity,{})
                        NGS_info['judge-variant'][Pathogenicity].setdefault(SortNumber,[]).append(Dict_NGS)
                elif sheet_name == "coverage" or sheet_name == "qc":
                    # ===>get co    verage info<====
                    coverage = self.openSheet(excel, sheet_name)
                    coverage_table = coverage['table']
                    coverage_nrows = coverage['nrows']
                    Dict_coverage = {}
                    NGS_info["coverage"] = {}
                    for i in range(coverage_nrows):
                        array_line = coverage_table.row_values(i)
                        if array_line[0] == "#Sample" or array_line[0] == "#Sample Name":
                            array_head = array_line
                            NGS_info["coverage"]["样本详细质控信息"] = {}
                            array_line = coverage_table.row_values(i+1)
                            for j in range(len(array_head)):
                                NGS_info["coverage"]["样本详细质控信息"][array_head[j]] = array_line[j]
                        else:
                            NGS_info["coverage"][array_line[0]] = array_line[1]
                else:
                    sheet_data = self.openSheet(excel, sheet_name)
                    variant_table = sheet_data['table']
                    variant_nrows = sheet_data['nrows']
                    variant_head = sheet_data['head']
                    array_sheet = []
                    for i in range(1, variant_nrows):
                        dist_line = {}
                        array = variant_table.row_values(i)
                        for i in range(len(variant_head)):
                            if sheet_name == "variant":
                                if variant_head[i] in special_col and variant_head[i] in special_col[3:]:
                                    dist_line[variant_head[i]] = self.getSpecialTitle(variant_head[i], array[variant_head.index(variant_head[i])])
                                else:
                                    dist_line[variant_head[i]] = array[i]
                            else:
                                dist_line[variant_head[i]] = array[i]
                        array_sheet.append(dist_line)
                    NGS_info[sheet_name] = array_sheet
            self.data = NGS_info