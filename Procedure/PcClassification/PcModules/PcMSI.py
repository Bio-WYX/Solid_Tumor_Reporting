import sys
sys.path.append("/data/autoReportV2/")
sys.path.append("/data/autoReportV2/reporter/guanhaowen/pan_cancer/pc/")
from PcClassification.PcModules.PcBaseclassify import PcBaseclassify
class PcGet_MSI(PcBaseclassify):
    def __init__(self):
        super(PcGet_MSI, self).__init__()
    @property
    def msi(self):
        _f = open(self._msi_out,'r')
        for line in _f.readlines():
            if line.startswith("Total"):
                pass
            else:
                _p = float(line.split("\t")[2])
                if _p >= 20 :
                    self._msi = "MSI-H"
                elif _p < 20 and _p > 0:
                    self._msi = "MSI-L"
                elif _p == 0:
                    self._msi = "MSS"            
        return self._msi,_p

