import sys
sys.path.append("D:\肿瘤产品调研\测试模板\pan_cancer\pc")
from PcClassificationHome.PcModules.PcBaseclassify import PcBaseclassify
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
                print(line)
                _p = float(line.split("\t")[2])
                print(_p)
                if _p >= 23 :
                    self._msi = "MSI-H"  
                elif _p <= 17:
                    self._msi = "MSS"  
                else:
                    self._msi = 'MSS'         
        return self._msi,_p


if __name__== "__main__":
    var = PcGet_MSI()
    var.msi_out = "D:\肿瘤产品调研\测试数据\诺禾数据\ZXR.msi_15.txt"
    print(var.msi)