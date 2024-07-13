class PcPreBaseinit():
    def __init__(self):
        self._raw_maf = None
        self._mafannotator = None
        self._oncokb_token = None
        self._cnv = None
        self._mode = None
        self._cancer = None
        self._raw_sv = None

    
    @property
    def raw_maf(self):
        return self._raw_maf
    @raw_maf.setter
    def raw_maf(self,raw_maf):
        self._raw_maf = raw_maf
    
    @property
    def raw_sv(self):
        return self._raw_sv
    @raw_sv.setter
    def raw_sv(self,raw_sv):
        self._raw_sv = raw_sv
        
    @property
    def mafannotator(self):
        return self._mafannotator
    @mafannotator.setter
    def mafannotator(self,mafannotator):
        self._mafannotator = mafannotator
    
    @property
    def fusionannotator(self):
        return self._fusionannotator
    @fusionannotator.setter
    def fusionannotator(self,fusionannotator):
        self._fusionannotator = fusionannotator
    
    
    
    @property
    def oncokb_token(self):
        return self._oncokb_token
    @oncokb_token.setter
    def oncokb_token(self,oncokb_token):
        self._oncokb_token = oncokb_token
    
    @property
    def mode(self):
        return self._mode 
    @mode.setter
    def mode(self,mode):
        self._mode = mode


    