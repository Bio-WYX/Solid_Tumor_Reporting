import sys
sys.path.append("/data/autoReportV2/")
sys.path.append("/data/autoReportV2/reporter/guanhaowen/pan_cancer/pc/")
from ar.db.WtDatabaseInstance import db
from PcClassification.PcFuctions.PcBaseinit import PcBaseinit
from PcClassification.PcFuctions.PcTranslate import Translate
from PcClassification.PcFuctions.PcGet_return_dict import get_return_dict 
from PcClassification.PcModules.PcBaseclassify import PcBaseclassify
from PcClassification.PcFuctions.PcFilter_level3 import PcFilter_level3
from functools import partial
import configparser
import pandas as pd
class PcDDR_var(PcBaseclassify):
    def __init__(self):
        super(PcDDR_var, self).__init__()
        print (PcDDR_var.__init__)
    @property
    def number(self):
        """获取DDR相关基因变异个数
        """
        try:
            _df = PcBaseinit(self._report,self._maf).get_classified(all)
            _df = PcFilter_level3(_df)
            _df.rename(columns={'AlterRatio(%)':'AF'},inplace=True)
            array_db = db.get_table(self._gene_list, "DDR相关基因").get()
            _ddr_db = pd.DataFrame(array_db)
            #_ddr_db = pd.read_excel(self._gene_list,sheet_name="DDR相关基因")
            _ddr_var = _df[_df["SYMBOL"].isin(_ddr_db["DDR_gene"])]
            self._number = _ddr_var.shape[0]
            if isinstance(self._number,int) == False:
                raise ValueError("DDR相关突变个数应为int")
            else:
                return self._number
        except ValueError as e:
            print("引发异常：",repr(e))
    @property
    def var_dict(self):
        """获取DDR基因相关变异信息字典
        """
        _df = PcBaseinit(self._report,self._maf).get_classified(all)
        _df = PcFilter_level3(_df)
        _df.rename(columns={'AlterRatio(%)':'AF'},inplace=True)
        array_db = db.get_table(self._gene_list, "DDR相关基因").get()
        _ddr_db = pd.DataFrame(array_db)
        #_ddr_db = pd.read_excel(self._gene_list,sheet_name="DDR相关基因")
        _ddr_var = _df[_df["SYMBOL"].isin(_ddr_db["DDR_gene"])]
        translate_clinvar = partial(Translate().translate_clinvar,DURG_NAME_DATABASE=self._durg_name_database)
        _ddr_var["ClinVar_CLNSIG"] = _ddr_var["ClinVar_CLNSIG"].apply(translate_clinvar)
        self._var_dict = get_return_dict(_ddr_var)
        return self._var_dict

