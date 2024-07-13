from ar.doc.WtComponent import WtComponent
"""
常用组件实例，自定义组件都可以按照下面形式进行编写
"""


class WtBasicComponent(WtComponent):
    def render(self):
        input = self.get_input()
        return {
            "sample_id":    input.get_sample("样本编号"),
            "name":         input.get_sample("姓名"),
            "sex":          input.get_sample("性别"),
            "nation":       input.get_sample("民族"),
            "age":          input.get_sample("年龄"),
            "family_id":    input.get_sample("家系编号"),
            "clinical_feature":     input.get_sample("临床表现"),
            "clinical_diagnosis":   input.get_sample("临床诊断"),
            "family_history":       input.get_sample("家族史"),
            "get_time":             input.get_sample("采样日期"),
            "receive_time":         input.get_sample("接收日期"),
        }


class WtTestItemsComponent(WtComponent):
    def render(self):
        mode = self.get_input().get_other('mode')

        t1 = self.get_table('血液病', '套餐种类-检测项目页表格').get(mode)
        format_data = []
        for i, item in enumerate(t1):
            node = {
                'ill': item['检测疾病'],
                'gene': item['检测基因'],
            }
            if i % 2 == 0:
                node.update({'bg1': "#F2F2F2", 'bg2': "#FFFFFF"})
            else:
                node.update({'bg1': "#D9D9D9", 'bg2': "#D9D9D9"})

            format_data.append(node)

        t2 = self.get_table('血液病', '血液病套餐种类').first(mode)
        project_explain = t2['检测项目页文字']

        return {
            'genes': format_data,
            'project_explain': project_explain,
        }


class WtMainTestResultComponent(WtComponent):
    def render(self):
        input = self.get_input()

        result = []
        p_list = {
            '致病': {},
            '可能致病': {},
        }

        for item in input.get_variant():
            if item['人工致病性注释'] == "致病":
                p_list["致病"][item['序号']] = item
            elif item['人工致病性注释'] == "可能致病":
                p_list["可能致病"][item['序号']] = item

        for level in ["致病", "可能致病"]:
            v = p_list[level]
            if not len(v):
                continue

            num = 0
            for note in sorted(v.keys()):
                num += 1
                result.append({
                    "gene": v[note]["基因"],
                    "tran": v[note]["转录本"],
                    "local": v[note]["染色体位置"],
                    "hgvsc": v[note]["核苷酸变异"],
                    "hgvsp": v[note]["氨基酸变异"],
                    "pathogenicity": level,
                    "num": num,
                })

        return {
            "result": result,
            "gene_type": '',
        }
