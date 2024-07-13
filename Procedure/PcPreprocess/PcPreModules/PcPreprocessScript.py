import sys
sys.path.append("/mnt/e/ansaisi/641panel/pan_cancer/pc")
from PcPreprocess.PcPreModules.PcPreBaseinit import PcPreBaseinit
from PcPreprocess.PcPreFuctions.PcRun import Run
from PcPreprocess.PcPreFuctions.PcClinical import PcClinical
from PcPreprocess.PcPreFuctions.PcIntroduce import PcIntroduce
from PcPreprocess.PcPreFuctions.PcCancer import PcCancer
from PcPreprocess.PcPreFuctions.PcFusion import get_clean_fusion
import pandas as pd
class PcPreprocess(PcPreBaseinit):
    def __init__(self):
        super(PcPreprocess, self).__init__()
        self._clinical_file = None
        self._introduce = None 
    
    @property
    def maf(self):
        self._maf = self._raw_maf + ".clean.oncokb_out"
        _clinical_file = self._raw_maf + ".clinical.txt"
        PcClinical(_clinical_file,self._mode)
        command1 = "python3 {MafAnnotator} \
            -i {maf} \
            -c {clinical_file}  \
            -o {oncokb_out} \
            -b {ONCOKB_TOKEN}".format(MafAnnotator=self._mafannotator,
                                    # maf=self._raw_maf+".clean",
                                    maf=self._raw_maf,
                                    oncokb_out=self._maf,
                                    ONCOKB_TOKEN=self._oncokb_token,
                                    # cancer=_cancer,
                                    clinical_file = _clinical_file) #oncokb api 注释
        Run(command1)
        return self._maf

    @property
    def cnv(self):
        pass

    @property
    def sv(self):
        if self._raw_sv == None:
            self._sv = None
        else:
            self._sv = self._raw_sv+".clean.oncokb_out"
            get_clean_fusion(self._raw_sv)
            _clinical_file = self._raw_maf + ".clinical.txt"
            command = "python3 {FusionAnnotator} \
                -i {sv} \
                -o {oncokb_out} \
                -c {clinical_file_oncokb} \
                -b {ONCOKB_TOKEN}".format(FusionAnnotator=self._fusionannotator,
                                        sv=self._raw_sv+".clean",
                                        oncokb_out=self._sv,
                                        clinical_file_oncokb=_clinical_file ,
                                        ONCOKB_TOKEN=self._oncokb_token) #oncokb api 注释
            Run(command)
        return self._sv
    
    
    @property
    def introduce(self):
        self._introduce = {'introduce':PcIntroduce(self._mode)}
        return self._introduce
    @property
    def cancer(self):
        self._cancer = PcCancer(self._mode)
        return self._cancer 
    
if __name__ == '__main__':
    pre = PcPreprocess()
    pre.mode = 357 #传递mode号
    pre.fusionannotator = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/pc/oncokb/oncokb-annotator-master/FusionAnnotator.py"
    pre.mafannotator = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/pc/oncokb/oncokb-annotator-master/MafAnnotator.py" #传递api脚本路径 
    pre.oncokb_token = "4e9508e0-cc76-47d9-ae1b-8fd180b43e53" #传递api toke
    # pre.cnv = info.cnv_out   #传递cnv路径
    pre.raw_sv = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试数据/诺禾数据/MAF测试/SP20308W01.fusion.json"
    pre.raw_maf = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试数据/诺禾数据/MAF测试/NLF.output_tnscope.filter.vep.maf" #传递sv路径
    # pre.raw_maf = "/Users/guanhaowen/Desktop/肿瘤产品调研/测试数据/诺禾数据/MAF测试/SP20308W01.output_tnscope.filter.vep.maf"
    # pre.maf
    pre.sv
   



                