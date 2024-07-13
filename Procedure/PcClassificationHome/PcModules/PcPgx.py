import sys
sys.path.append("/Users/guanhaowen/Desktop/肿瘤产品调研/测试模板/pan_cancer/pc")
from PcClassificationHome.PcModules.PcBaseclassify import PcBaseclassify
import re
import gzip
import xlrd
import pandas as pd
class PcChemotherapy(PcBaseclassify):
	def __init__(self):
		super(PcChemotherapy, self).__init__()
	def read_database(self,databaseFile):
		data = xlrd.open_workbook(databaseFile)
		table = data.sheet_by_name("Pgx")
		nrows = table.nrows
		head = table.row_values(0)
		database = {
			"pgx": [],
			"rs": {}
		}
		for i in range(1, nrows):
			array = table.row_values(i)  # 药物	基因	位点	基因型	毒性	有效性	证据等级
			药物 = array[head.index("药物")]
			基因 = array[head.index("基因")]
			位点 = array[head.index("位点")]
			基因型 = array[head.index("基因型")]
			毒性 = array[head.index("毒副作用")]
			有效性 = array[head.index("功效")]
			证据等级 = array[head.index("证据等级")]
			dist = {
				"药物": 药物,
				"基因": 基因,
				"位点": 位点,
				"基因型": 基因型,
				"毒性": 毒性,
				"有效性": 有效性,
				"证据等级": 证据等级
			}
			database["pgx"].append(dist)

		table = data.sheet_by_name("rs")
		nrows = table.nrows
		head = table.row_values(0)
		for i in range(1, nrows):
			array = table.row_values(i)
			rs = array[head.index("位点")]
			Allele = array[head.index("Allele")]
			database["rs"][rs] = Allele
		return(database)

	def tiqu_gvcf(self,gvcfFile):
		suffix = gvcfFile.rsplit('.', 1)[1]
		if(suffix == "gz"):
			with gzip.open(gvcfFile, "rt", encoding='utf-8') as f:
				lines = f.readlines()
		elif(suffix == "vcf"):
			with open(gvcfFile, "r", encoding='utf-8') as f:
				lines = f.readlines()
		else:
			lines = []
		head = []
		野生型区域 = []
		distGT = {}
		for line in lines:
			line = line.strip()
			array = line.split("\t")
			if(re.match("^##", array[0])):
				continue
			elif(re.match("^#CHROM", array[0])):
				head = array
				continue
			else: pass  # #CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	SP00820W01-13484
			chrom = array[head.index("#CHROM")]
			position = array[head.index("POS")]
			ref = array[head.index("REF")]
			alt = array[head.index("ALT")]
			info = array[head.index("INFO")]
			format = array[head.index("FORMAT")].split(":")
			results = array[9].split(":")
			GT = results[format.index("GT")]
			GT1 = int(GT.split("/")[0])
			GT2 = int(GT.split("/")[1])
			DP = results[format.index("DP")]
			if("NOCALL" in line  or GT == "./."): continue
			else: pass
			alt = alt.replace(",<NON_REF>", "")
			alt = alt.replace("<NON_REF>", "")
			alts = alt.split(",")
			if(GT == "0/0"):
				if(re.match("END=(\d+)", info)):
					a = re.match("END=(\d+)", info)
					start = int(position)
					stop = int(a.group(1))
				else:
					start = int(position)
					stop = start+len(ref)-1
				if(野生型区域 == []):
					野生型区域 = [start, stop]
				elif(start >= 野生型区域[0] and start <= 野生型区域[-1]+1):
					野生型区域 += [start, stop]
				else:
					distKey2 = str(野生型区域[0])+"-"+str(野生型区域[-1])

					if(chrom not in distGT):
						distGT[chrom] = {
							distKey2: "野生型"
						}
					else:
						distGT[chrom][distKey2] = "野生型"
					野生型区域 = [start, stop]
			else:
				if(野生型区域 != []):
					distKey2 = str(野生型区域[0])+"-"+str(野生型区域[-1])
					if(chrom not in distGT):
						distGT[chrom] = {
							distKey2: "野生型"
						}
					else:
						distGT[chrom][distKey2] = "野生型"
					野生型区域 = []
				else: pass
				
				Altss = []
				for Alt in alts:
					Refs = list(ref)
					Alts = list(Alt)
					lenRefs = len(Refs)
					for i in range(lenRefs):
						if(i == len(Alts)): break
						if(Refs[i] == Alts[i]):
							ref = ref[1:]
							Alt = Alt[1:]
							position = int(position)+1
						if(Refs[-(i+1)] == Alts[-(i+1)]):
							ref = ref[:-(i+1)]
							Alt = Alt[:-(i+1)]
						else: pass
					Altss.append(Alt)

				if(GT1 == 0):
					if(len(Altss) < GT2): continue
					else: pass
					Alt = Altss[GT2-1]
					het = "杂合"
					keyPgx = str(position)+":"+ref+":"+Alt
					if(chrom not in distGT):
						distGT[chrom] = {
							keyPgx: het
						}
					distGT[chrom][keyPgx] = het
				elif(GT1 == GT2):
					if(len(Altss) < GT2): continue
					else: pass
					Alt = Altss[GT1-1]
					het = "纯合"
					keyPgx = str(position)+":"+ref+":"+Alt
					if(chrom not in distGT):
						distGT[chrom] = {
							keyPgx: het
						}
					distGT[chrom][keyPgx] = het
				else:
					if(len(Altss) < GT1 or len(Altss) < GT2): continue
					else: pass
					Alt1 = Altss[GT1-1]
					Alt2 = Altss[GT2-1]
					het = "杂合"
					keyPgx1 = str(position)+":"+ref+":"+Alt1
					keyPgx2 = str(position)+":"+ref+":"+Alt2
					if(chrom not in distGT):
						distGT[chrom] = {
							keyPgx1: het
						}
					distGT[chrom][keyPgx1] = het
					if(chrom not in distGT):
						distGT[chrom] = {
							keyPgx2: het
						}
					distGT[chrom][keyPgx2] = het
		print(distGT)
		return(distGT)

	def chaxun_rs_genotype(self,database, distGT):
		dist_基因型格式化 = {
			"AA": "AA",
			"AC": "AC",
			"AG": "AG",
			"AT": "AT",
			"CA": "AC",
			"CC": "CC",
			"CG": "CG",
			"CT": "CT",
			"GA": "AG",
			"GC": "CG",
			"GG": "GG",
			"GT": "GT",
			"TA": "AT",
			"TC": "CT",
			"TG": "GT",
			"TT": "TT"
		}
		mark_array = []
		distDocx = {}
		for distPgx in database["pgx"]:
			药物 = distPgx["药物"]
			基因 = distPgx["基因"]
			位点 = distPgx["位点"]
			基因型_db = distPgx["基因型"]
			毒性 = distPgx["毒性"]
			有效性 = distPgx["有效性"]
			证据等级 = distPgx["证据等级"]
			GT = ""
			Allele = database["rs"][位点]
			a = re.match("(.*):(.*):(.*):(.*)", Allele)
			chrom = a.group(1)
			pos = int(a.group(2))
			ref = a.group(3)
			alt = a.group(4)
			基因型_gvcf = ""
			
			if(chrom in distGT): 
				for keyPgx in distGT[chrom]:
					gtGvcf = distGT[chrom][keyPgx]
					if(re.match("(\d+)-(\d+)", keyPgx)):
						a = re.match("(\d+)-(\d+)", keyPgx)
						start = int(a.group(1))
						stop = int(a.group(2))
						if(pos >= start and pos <= stop):
							GT = ref+ref
						else: continue
					elif(re.match("(\d+):(.*?):(.*)", keyPgx)):
						
						a = re.match("(\d+):(.*?):(.*)", keyPgx)
						posGvcf = int(a.group(1))
						refGvcf = a.group(2)
						altGvcf = a.group(3)
						
						if(pos == posGvcf and ref == refGvcf and alt == altGvcf):
							if(gtGvcf == "杂合"):
								GT = ref+alt
							elif(gtGvcf == "纯合"):
								GT = alt+alt
							else: 
								GT = "NOCALL"
						else: continue
						
					else: continue
			else:
				GT = "NOCALL"
			
			if(基因型_db in dist_基因型格式化):
				基因型_db = dist_基因型格式化[基因型_db]
			else: pass

			if(GT in dist_基因型格式化):
				GT = dist_基因型格式化[GT]
			else: pass

			证据等级 = str(证据等级).replace(".0", "")
			keyDocx = 药物+"_"+位点
			keyDocx = keyDocx.replace("+", "_")
			keyDocx = keyDocx.replace("、", "_")
			if(GT == 基因型_db):
				distDocx["CJQ_"+keyDocx+"_g"] = 基因型_db
				distDocx["CJQ_"+keyDocx+"_t"] = 毒性
				distDocx["CJQ_"+keyDocx+"_e"] = 有效性
				distDocx["CJQ_"+keyDocx+"_l"] = 证据等级
				continue
			else: 
				if(keyDocx not in mark_array): 
					mark_array = [keyDocx]
				else:
					mark_array.append(keyDocx)
				# line = 药物+"\t"+基因+"\t"+位点+"\t"+基因型_db+"\t"+毒性+"\t"+有效性+"\t"+str(证据等级)+"\t"+"NOCALL"
			
			if(len(mark_array) == 3):
				distDocx["CJQ_"+keyDocx+"_g"] = "NOCALL"
				distDocx["CJQ_"+keyDocx+"_t"] = 毒性
				distDocx["CJQ_"+keyDocx+"_e"] = 有效性
				distDocx["CJQ_"+keyDocx+"_l"] = 证据等级
		return(distDocx)
	
	@property
	def chemo_dict(self):
		database = self.read_database(self._chemotherapy_database)
		distGT = self.tiqu_gvcf(self._gvcf)
		self._chemo_dict = self.chaxun_rs_genotype(database, distGT)
		return self._chemo_dict

if __name__ == '__main__':
    var= PcChemotherapy()
    var.gvcf="/Users/guanhaowen/Desktop/肿瘤产品调研/测试数据/R21110452-LXF-LXF.Haplotyper.g.vcf.gz"
    var.chemotherapy_database="/Users/guanhaowen/Downloads/化疗药最终版-2021.04.07.xls"
    var.chemo_dict


