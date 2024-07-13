class PcBaseclassify():
    """检查输入文件
    """
    def __init__(self):
        self._report = None
        self._maf = None
        self._durg_name_database = None
        self._gene_description = None
        self._var_description = None
        self._immu_database = None
        self._clinicaltrils_database = None
        self._gene_list= None
        self._nccn_database = None
        self._chemotherapy_database = None
        self._sv = None
        self._msi_out = None
        self._cancer = None
        self._mode =None
        self._cancer_cn = None
        self._gvcf = None
        self._fastp_json_file = None 
        self._bamdst_report = None
        self._fusion_json = None
        self._result = None
        self._gene_disease = None
        self._prognosis = None

    def check_filetype(self,file,suffix):
        """[summary]

        Args:
            file ([type]): 输入文件
            suffix ([type]): 文件后缀

        Raises:
            ValueError: 格式错误
        """
        if file == None:
            pass
        elif file !=None:
            _file_type = file.split(".")[-1]
            if _file_type != suffix:
                raise ValueError(file+"格式错误")
            else:
                pass
    @property   
    def mode(self):
        return self.mode 
    @mode.setter
    def mode(self,mode):
        try:
            self._mode = mode
            if mode == None:
                pass
            elif mode != None:
                if mode not in [357,358,359,360,361,362,363,364,365,366]:
                    raise ValueError("mode号错误")
                else:
                    pass
        except ValueError as e:
            print("引发异常：",repr(e))   

    @property   
    def report(self):
        return self._report 
    @report.setter
    def report(self,report):
        try:
            self._report = report
            self.check_filetype(report,"xls")        
        except ValueError as e:
            print("引发异常：",repr(e)) 

    @property
    def maf(self):
        return self._maf
    @maf.setter
    def maf(self,maf):
        try:
            self._maf = maf
            self.check_filetype(maf,"oncokb_out")
        except ValueError as e:
            print("引发异常：",repr(e))

    @property
    def durg_name_database(self):
        return self._durg_name_database
    @durg_name_database.setter
    def durg_name_database(self,durg_name_database):
        try:
            self._durg_name_database = durg_name_database
            self.check_filetype(durg_name_database,"xlsx")
        except ValueError as e:
            print("引发异常：",repr(e))
    
    @property
    def gene_description(self):
        return self._gene_description
    @gene_description.setter
    def gene_description(self,gene_description):
        try:
            self._gene_description = gene_description
            self.check_filetype(gene_description,"xlsx")
        except ValueError as e:
            print("引发异常：",repr(e))
    
    @property
    def var_description(self):
        return self._var_description
    @var_description.setter
    def var_description(self,var_description):
        try:
            self._var_description = var_description
            self.check_filetype(var_description,"xlsx")
        except ValueError as e:
            print("引发异常：",repr(e))
    
    @property
    def immu_database(self):
        return self._immu_database
    @immu_database.setter
    def immu_database(self,immu_database):
        try:
            self._immu_database = immu_database
            self.check_filetype(immu_database,"xlsx")
        except ValueError as e:
            print("引发异常：",repr(e))
            
    @property
    def tmb_database(self):
        return self._tmb_database
    @tmb_database.setter
    def tmb_database(self,tmb_database):
        try:
            self._tmb_database = tmb_database
            self.check_filetype(tmb_database,"xlsx")
        except ValueError as e:
            print("引发异常：",repr(e))
    
    @property
    def tmb_png(self):
        return self._tmb_png
    @tmb_png.setter
    def tmb_png(self,tmb_png):
        try:
            self._tmb_png = tmb_png
            self.check_filetype(tmb_png,"png")
        except ValueError as e:
            print("引发异常：",repr(e))
            
    @property
    def clinicaltrils_database(self):
        return self._clinicaltrils_database
    @clinicaltrils_database.setter
    def clinicaltrils_database(self,clinicaltrils_database):
        try:
            self._clinicaltrils_database = clinicaltrils_database
            self.check_filetype(clinicaltrils_database,"xlsx")
        except ValueError as e:
            print("引发异常：",repr(e))
    
    @property
    def gene_list(self):
        return self._gene_list
    @gene_list.setter
    def gene_list(self,gene_list):
        try:
            self._gene_list = gene_list
            self.check_filetype(gene_list,"xlsx")
        except ValueError as e:
            print("引发异常：",repr(e))
    
    @property
    def nccn_database(self):
        return self._nccn_database
    @nccn_database.setter
    def nccn_database(self,nccn_database):
        try:
            self._nccn_database = nccn_database
            self.check_filetype(nccn_database,"xlsx")
        except ValueError as e:
            print("引发异常：",repr(e))
    
    @property
    def cancer(self):
        return self._cancer
    @cancer.setter
    def cancer(self,cancer):
        try:
            self._cancer = cancer
            if cancer in ["Breast Cancer","Colorectal Cancer","NSCLC","HCC","EGC"] == False:
                raise ValueError("癌种输入错误，请输入下列癌种之一：Breast Cancer,Colorectal Cancer,NSCLC,HCC,EGC")
        except ValueError as e:
            print("引发异常：",repr(e))  
   
    @property
    def cancer_cn(self):
        cancer_dict = {'NSCLC':"肺癌",
                    'Breast Cancer':'乳腺癌',
                    'Colorectal Cancer':'结直肠癌',
                    'HCC':"肝癌",
                    "Esophagogastric Cancer":"胃癌"}    
        if self._cancer == None:
            cancer_cn = None
        else:
            cancer_cn = cancer_dict[self._cancer]
        return cancer_cn

    @property
    def msi_out(self):
        return self._msi_out
    @msi_out.setter
    def msi_out(self,msi_out):
        try:
            self._msi_out = msi_out
            self.check_filetype(msi_out,"txt")
        except ValueError as e:
            print("引发异常:",repr(e))  

    @property
    def chemotherapy_database(self):
        return self._chemotherapy_database
    @chemotherapy_database.setter
    def chemotherapy_database(self,chemotherapy_database):
        try:
            self._chemotherapy_database = chemotherapy_database
            self.check_filetype(chemotherapy_database,"xlsx")         
        except ValueError as e:
            print("引发异常:",repr(e)) 

    @property
    def gvcf(self):
        return self._gvcf
    @gvcf.setter
    def gvcf(self,gvcf):
        try:
            self._gvcf = gvcf
            self.check_filetype(gvcf,"gz")
        except ValueError as e:
            print("引发异常:",repr(e)) 
    
    @property
    def sv(self):
        return self._sv
    @sv.setter
    def sv(self,sv):
        try:
            self._sv = sv
            self.check_filetype(sv,"oncokb_out")
        except ValueError as e:
            print("引发异常:",repr(e))

    @property
    def cancer(self):
        return self._cancer
    @cancer.setter
    def cancer(self,cancer):
        try:
            self._cancer = cancer
            if cancer in ["Breast Cancer","Colorectal Cancer","NSCLC","HCC","EGC"] == False:
                raise ValueError("癌种输入错误，请输入下列癌种之一：Breast Cancer,Colorectal Cancer,NSCLC,HCC,EGC")
        except ValueError as e:
            print("引发异常：",repr(e))
    
    @property
    def fastp_json_file(self):
        return self._fastp_json_file
    @fastp_json_file.setter
    def fastp_json_file(self,fastp_json_file):
        try:
            self._fastp_json_file = fastp_json_file
            self.check_filetype(fastp_json_file,"json")
        except ValueError as e:
            print("引发异常:",repr(e)) 
    
    @property
    def bamdst_report(self):
        return self._bamdst_report
    @bamdst_report.setter
    def bamdst_report(self,bamdst_report):
        try:
            self._bamdst_report = bamdst_report
            self.check_filetype(bamdst_report,"report")
        except ValueError as e:
            print("引发异常:",repr(e)) 
            
    @property
    def fusion_json(self):
        return self._fusion_json
    @fusion_json.setter
    def fusion_json(self,fusion_json):
        try:
            self._fusion_json = fusion_json
            self.check_filetype(fusion_json,"json")
        except ValueError as e:
            print("引发异常:",repr(e))

    @property
    def result(self):
        return self._result
    @result.setter
    def result(self, result):
        try:
            self._result = result
            self.check_filetype(result, "xls")
        except ValueError as e:
            print("引发异常:", repr(e))

    @property
    def gene_disease(self):
        return self._gene_disease
    @gene_disease.setter
    def gene_disease(self, gene_disease):
        try:
            self._gene_disease = gene_disease
            self.check_filetype(gene_disease, "xlsx")
        except ValueError as e:
            print("引发异常:", repr(e))

    @property
    def prognosis(self):
        return self._prognosis
    @prognosis.setter
    def prognosis(self, prognosis):
        try:
            self._prognosis = prognosis
            self.check_filetype(prognosis, "xlsx")
        except ValueError as e:
            print("引发异常:", repr(e))