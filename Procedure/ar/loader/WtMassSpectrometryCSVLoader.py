import csv

from ar.loader.WtVariantInfoLoader import WtVariantInfoLoader

'''
读取csv文件
'''
class WtMassSpectrometryCSVLoader(WtVariantInfoLoader):
    
    def load(self, variantInput, loader_config):
        NGS_info =[]
        array_info=[]
        sample = "Sample Id"
        if variantInput["customFiles"]["inputPath"] != "":
            inputcsv = variantInput["customFiles"]["inputPath"]
            with open(inputcsv) as f:
                object_csv_data = csv.reader(f)
                key_head = 0
                for array_csv_data in object_csv_data:
                    if array_csv_data[0] == sample:
                        array_info = array_csv_data
                        key_head = 1
                        continue
                    elif key_head == 0:
                        continue
                    else:
                        # 此处这个是把俩个数组使用函数来键值对相互对应赋值好的
                        dist = dict(map(lambda x,y:[x,y],array_info,array_csv_data))
                        NGS_info.append(dist)
        self.data = NGS_info
