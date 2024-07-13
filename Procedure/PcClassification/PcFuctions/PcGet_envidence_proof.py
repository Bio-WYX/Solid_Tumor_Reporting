def get_envidence_proof(element):
    """oncokb证据等级转换为ACMG证据等级

    Args:
        element (str): oncokb对变异位点的证据等级打分
    Returns:
        str: ACMG对变异位点的证据等级打分
    """
    if element == "LEVEL_1" or element == "LEVEL_2" or element == "LEVEL_R1":
        evidence_proof = "A"
    #oncokb LEVEL_1，LEVEL_2，LEVEL_R1 对应 ACMG A

    elif element == "LEVEL_3A":
        evidence_proof = "B"
    #oncokb LEVEL_3A 对应 ACMG B

    elif element == "LEVEL_3B":
        evidence_proof = "C"
    #oncokb LEVEL_3B 对应 ACMG C

    elif element == "LEVEL_4" or element == "LEVEL_R2":
        evidence_proof = "D"
    #oncokb LEVEL_4，LEVEL_R2 对应 ACMG D
    else:
        evidence_proof = "无致病等级"
    
    return evidence_proof