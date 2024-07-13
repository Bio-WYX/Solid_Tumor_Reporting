import sys
sys.path.append("/data/autoReportV2/")
sys.path.append("/data/autoReportV2/reporter/guanhaowen/pan_cancer/pc/")
from PcClassification.PcFuctions.PcBaseinit import PcBaseinit
from PcClassification.PcFuctions.PcTranslate import Translate
from PcClassification.PcFuctions.PcGet_return_dict import get_return_dict 
from PcClassification.PcModules.PcBaseclassify import PcBaseclassify
from PcClassification.PcFuctions.PcFilter_level3 import PcFilter_level3
from PcClassification.PcFuctions.PcGet_disease import PcGet_disease
from functools import partial
import pandas as pd
from ar.db.WtDatabaseInstance import db

class PcGermline_var(PcBaseclassify):
    def __init__(self):
        super(PcGermline_var, self).__init__()
    
    @property
    def number(self):
        array_db = db.get_table(self._gene_list, "遗传易感").get()
        _db = pd.DataFrame(array_db)
       #_db = pd.read_excel(self._gene_list,sheet_name="遗传易感")
        _df = PcBaseinit(self._report,self._maf).get_classified(all)
        _df = PcFilter_level3(_df)
        _var = _df[_df["SYMBOL"].isin(_db["所有基因"])]
        _var = _var[_var["AF"] > 20]
        self._number = _var.shape[0]
        return self._number
    
    @property
    def var_dict(self):
        array_db = db.get_table(self._gene_list, "遗传易感").get()
        _db = pd.DataFrame(array_db)
        #_db = pd.read_excel(self._gene_list,sheet_name="遗传易感")
        _df = PcBaseinit(self._report,self._maf).get_classified(all)
        _df = PcFilter_level3(_df)
        _var = _df[_df["SYMBOL"].isin(_db["所有基因"])]
        _var = _var[_var["AF"] > 20]
        translate_clinvar = partial(Translate().translate_clinvar,DURG_NAME_DATABASE=self._durg_name_database)
        _var["ClinVar_CLNSIG"] = _var["ClinVar_CLNSIG"].apply(translate_clinvar)
        get_disease = partial(PcGet_disease,gene_list_ycyg = self._gene_list)
        _var["疾病"] = _var["SYMBOL"].apply(get_disease)
        _var['chr'] = _var['Allele'].str.split(":",expand=True)[0].str.split("chr",expand=True)[1]
        self._var_dict = get_return_dict(_var)
        return self._var_dict

