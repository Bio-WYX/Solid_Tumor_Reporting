def get_type(gene):
    _dict = {
    'ALK':'点突变/基因重排/插入/缺失/拷贝数变异',
    'BRAF':'点突变/插入/缺失',
    'EGFR':'点突变/插入/缺失/拷贝数变异',
    'ERBB2':'点突变/插入/缺失/拷贝数变异',
    'KRAS':'点突变/插入/缺失/拷贝数变异',
    'MET':'点突变/插入/缺失/拷贝数变异',
    'NTRK1':'点突变/基因重排',
    'NTRK2':'点突变/基因重排',
    'NTRK3':'点突变/基因重排',
    'RET':'基因重排',
    'ROS1':'点突变/基因重排/插入/缺失/拷贝数变异'
    }
    _type = _dict[gene]
    return _type
def get_text(cancer):
    if cancer == 'NSCLC':
        text = """1.以上列出了NCCN指南{{ cancer }}推荐的11个基因变异，其他基因的检测结果请参见基因变异汇总。
（1）ALK基因检测包含但不限于ALK基因重排EML4-ALK、KIF5B-ALK和HIP1-ALK等；C1156Y、G1202R和G1269A等点突变以及拷贝数扩增。
（2）BRAF基因检测包含但不限于V600E、K601E和G469V等点突变。
（3）EGFR基因检测包含但不限于L858R、T790M、G719X、S768I、L861Q和C797S等点突变，exon19del，exon20ins以及拷贝数扩增。
（4）ERBB2基因检测包含但不限于S310F、V842I和S855I等点突变，exon20ins以及拷贝数扩增。
（5）KRAS基因检测包含但不限于G12X、G13X和Q61X等点突变以及拷贝数扩增。
（6）MET基因检测包含但不限于MET基因14号外显子跳跃突变、插入/缺失等变异类型以及拷贝数扩增。
（7）NTRK基因检测包含但不限于NTRK基因重排TPM3-NTRK1、AGBL4-NTRK2和ETV6-NTRK3等。
（8）RET基因检测包含但不限于RET基因重排CCDC6-RET、KIF5B-RET和NCOA4-RET等。
（9）ROS1基因检测包含但不限于ROS1基因重排CD74-ROS1、SLC34A2-ROS1和SDC4-ROS1以及D2033N、G2032R和S1986Y等点突变。
2.证据等级变异解读详见靶向治疗相关检测结果。"""
        return text