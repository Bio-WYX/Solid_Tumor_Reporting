from PcPreprocess.PcPreModules.PcPreBaseinit import PcPreBaseinit
from PcPreprocess.PcPreFuctions.PcRun import Run
from PcPreprocess.PcPreFuctions.PcClinical import PcClinical
from PcPreprocess.PcPreFuctions.PcIntroduce import PcIntroduce
from PcPreprocess.PcPreFuctions.PcCancer import PcCancer
class PcPreprocess(PcPreBaseinit):
    def __init__(self):
        super(PcPreprocess, self).__init__()
        self._raw_maf = None
        self._clinical_file = None
        self._introduce = None
        self._maf = None
        self._cancer = None
    
    @property
    def maf(self):
        self._maf = self._raw_maf + ".oncokb_out"
        _clinical_file = self._raw_maf + ".clinical.txt"
        PcClinical(_clinical_file,self._mode)


        command = "python3 {MafAnnotator} -i {maf} -o {oncokb_out} -c {clinical_file_oncokb} -b {ONCOKB_TOKEN}".format(MafAnnotator=self._mafannotator,
                                                                                maf=self._raw_maf,
                                                                                oncokb_out=self._maf,
                                                                                clinical_file_oncokb=_clinical_file ,
                                                                                ONCOKB_TOKEN=self._oncokb_token) #oncokb api 注释
        Run(command)
        return self._maf

    @property
    def cnv(self):
        pass

    @property
    def sv(self):
        pass    
    
    @property
    def introduce(self):
        self._introduce = {'introduce':PcIntroduce(self._mode)}
        return self._introduce
    @property
    def cancer(self):
        self._cancer = PcCancer(self._mode)
        return self._cancer 
    





                