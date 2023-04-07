import json
from .utils.feishu import Feishu
from rich import print
import pandas as pd


class Course:
    def __init__(self, app_id, app_secret) -> None:
        self.feishu = Feishu(app_id, app_secret)
        self.app_token = "bascnNz4Nqjqgqm1Nm5AYke6xxb"
        self.table_id = "tblW2umsCYJWzzUX"

    def lab_skills_weight(self) -> None:
        """计算 lab 的 skills 权重

        Returns:
            _type_: _description_
        """
        # Get all labs from feishu
        records = self.feishu.get_bitable_records(
            self.app_token, self.table_id, params=""
        )
        # 处理 Skills
        lab_skills_dict = {}
        for l in records:
            lab_skills_dict[f"{l['fields']['REPO_NAME']}:{l['fields']['PATH']}"] = {
                "skills": l["fields"]["SKILLS_ID"],
                "type": l["fields"]["TYPE"],
            }
        # 计算权重
        for r in records:
            # 处理 skills raw
            r_name = f"{r['fields']['REPO_NAME']}:{r['fields']['PATH']}"
            skills_raw = json.loads(r["fields"]["SKILLS_RAW"])
            # 初始化权重的空白字典
            skills_weight = {}
            # 初始化存储位置权重的空白字典
            skills_position_weight = {}
            # 初始化存储占比权重的空白字典
            skills_proportion_weight = {}
            # 取出 lab 的全部 skills
            lab_skills = lab_skills_dict[r_name]["skills"]
            # 为每个 skill 创建存储权重的空白列表
            for lab_skill in lab_skills:
                skills_position_weight[lab_skill] = []
                skills_proportion_weight[lab_skill] = []
            # 遍历全部步骤，计算位置权重
            all_skills = []  # 存储全部 skills, 用于计算占比权重
            for step_num, step_skills_list in skills_raw.items():
                all_skills.extend(step_skills_list)
                # 遍历全部 skills
                for lab_skill in lab_skills:
                    # 初始化位置权重为 0
                    skill_position_weight = 0
                    # 遍历步骤的 skills
                    for i, step_skill in enumerate(step_skills_list):
                        # 如果 lab_skill 在步骤的 skills 中
                        if lab_skill == step_skill:
                            # 计算位置权重
                            skill_position_weight = 1 / (i + 1)
                    skills_position_weight[lab_skill].append(
                        round(skill_position_weight, 3)
                    )
            lab_skills_dict[r_name]["skills_position_weight"] = skills_position_weight
            # 计算占比权重
            for lab_skill in lab_skills:
                skill_proportion_weight = all_skills.count(lab_skill) / len(all_skills)
                skills_proportion_weight[lab_skill] = round(skill_proportion_weight, 3)
            lab_skills_dict[r_name][
                "skills_proportion_weight"
            ] = skills_proportion_weight
            # 对位置权重求平均值，并与占比权重相加
            for lab_skill in lab_skills:
                skill_position_weight_avg = sum(
                    skills_position_weight[lab_skill]
                ) / len(skills_position_weight[lab_skill])
                skill_weight = (
                    skill_position_weight_avg + skills_proportion_weight[lab_skill]
                )
                skills_weight[lab_skill] = round(skill_weight, 3)
            # 对权重进行排序
            skills_weight = dict(
                sorted(skills_weight.items(), key=lambda item: item[1], reverse=True)
            )
            lab_skills_dict[r_name]["skills_weight"] = skills_weight
        print(f"已经计算出 {len(lab_skills_dict)} 个 labs 的 skills 权重")
        return lab_skills_dict

    def export_to_csv(self, skills: list) -> None:
        lab_skills_dict = self.lab_skills_weight()
        course_labs = []
        for s in skills:
            for r_name, r in lab_skills_dict.items():
                if s in r["skills"]:
                    course_labs.append(r_name)
        # 对 course_labs 去重
        course_labs = list(set(course_labs))
        # 对 course_labs 进行排序
        course_labs = sorted(course_labs, key=lambda x: x.split(":")[1], reverse=True)
        new_course_labs = []
        for lab in course_labs:
            lab_type = lab_skills_dict[lab]["type"]
            lab_weight = lab_skills_dict[lab]["skills_weight"]
            new_course_labs.append(
                {"lab_name": lab, "lab_type": lab_type, "lab_weight": lab_weight}
            )
        # 生成 course_labs 的 dataframe
        course_labs_df = pd.DataFrame(new_course_labs)
        print(course_labs_df)
        # 生成 course_labs 的 csv
        course_labs_df.to_csv("course_labs.csv", index=False)
        print("已经生成 course_labs.csv")
