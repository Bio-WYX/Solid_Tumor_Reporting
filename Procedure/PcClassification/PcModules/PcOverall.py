import pandas as pd
import sys
sys.path.append("/data/autoReportV2/")
sys.path.append("/data/autoReportV2/reporter/guanhaowen/pan_cancer/pc/")
from ar.db.WtDatabaseInstance import db
from PcClassification.PcModules.PcBaseclassify import PcBaseclassify
from PcClassification.PcFuctions.PcBaseinit import PcBaseinit
from PcClassification.PcFuctions.PcNCCN import *

class PcOverall(PcBaseclassify):
    def __init__(self):
         super(PcOverall, self).__init__()
    @property
    def var_dict(self):
        _var_df_1 = PcBaseinit(self._report,self._maf).get_classified(1)
        _var_df_2 = PcBaseinit(self._report,self._maf).get_classified(2)
        _var_df = pd.concat([_var_df_1,_var_df_2])
        array_db = db.get_table(self._nccn_database, "汇总").get()
        _db = pd.DataFrame(array_db)
        #_db = pd.read_excel(self._nccn_database)
        _dict = get_nccn(_var_df,_db,self._cancer)
        return _dict
