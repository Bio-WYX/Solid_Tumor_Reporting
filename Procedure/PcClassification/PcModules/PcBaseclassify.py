class PcBaseclassify():
    """检查输入文件
    """
    def __init__(self):
        self._report = None
        self._maf = None
        self._durg_name_database = "实体瘤-药物名称数据库"
        self._gene_description = "实体瘤-基因描述数据库"
        self._var_description = "实体瘤-变异注释数据库"
        self._immu_database = "实体瘤-免疫数据库"
        self._clinicaltrils_database = "实体瘤-临床试验数据库"
        self._gene_list= "实体瘤-基因列表"
        self._nccn_database = "实体瘤-指南数据库"
        self._chemotherapy_database = "实体瘤-化疗药数据库"
        self._gvcf = None
        self._msi_out = None
        self._cancer = None
        self._mode =None
        self._cancer_cn = None
        print(self._clinicaltrils_database)
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
    def gvcf(self):
        return self._gvcf
    @gvcf.setter
    def gvcf(self,gvcf):
        try:
            self._gvcf = gvcf
            self.check_filetype(gvcf,"gz")
        except ValueError as e:
            print("引发异常:",repr(e))

    #------------初始化数据库名称---------------
    # @property
    # def durg_name_database(self):
    #     self._durg_name_database = "实体瘤-药物名称数据库"
    #     return self._durg_name_database
    # @property
    # def gene_description(self):
    #     self._gene_description = "实体瘤-基因描述数据库"
    #     return self._gene_description
    # @property
    # def var_description(self):
    #     self._var_description = "实体瘤-变异注释数据库"
    #     return self._var_description
    # @property
    # def immu_database(self):
    #     self._immu_database = "实体瘤-免疫数据库"
    #     return self._immu_database
    # @property
    # def clinicaltrils_database(self):
    #     self._clinicaltrils_database = "实体瘤-临床试验数据库"
    #     return self._clinicaltrils_database
    # @property
    # def gene_list(self):
    #     self._gene_list = "实体瘤-基因列表"
    #     return self._gene_list
    # @property
    # def nccn_database(self):
    #     self._nccn_database = "实体瘤-指南数据库"
    #     return self._nccn_database
    # @property
    # def chemotherapy_database(self):
    #     self._chemotherapy_database = "实体瘤-化疗药数据库"
    #     return self._chemotherapy_database
