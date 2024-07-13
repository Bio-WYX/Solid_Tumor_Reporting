import re
def get_protein_id(element):
    """提取蛋白质名称

    Args:
        element (str): 原始注释结果中信息

    Returns:
        str: hgvs.p格式的变异
    """
    pep = ""
    if re.match(".*?:(.*)",element):
        element = re.match(".*?:(.*)",element)
        pep = element.group(1)
    return pep