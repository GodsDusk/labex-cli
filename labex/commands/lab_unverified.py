import json
from rich import print
from rich.progress import track
from .utils.labex_api import AdminData, UserData
from .utils.auth import AuthGitHub
from github import Github


class LabForTesting:
    def __init__(self, repo_name: str) -> None:
        # for labex
        self.__admin_data = AdminData()
        all_paths = UserData().get_all_path()
        self.path_alias = [p["alias"] for p in all_paths["paths"]]
        # for github
        GITHUB_TOKEN = AuthGitHub().read_github_token()
        g = Github(login_or_token=GITHUB_TOKEN, retry=10)
        self.repo = g.get_repo(repo_name)

    def __get_all_labs(self, hidden: str, namespace_ids: list, page_size: int) -> list:
        print(f"Get Labs from Namespace: {namespace_ids}")
        all_labs = []
        for namespace_id in namespace_ids:
            # filter params
            filters = f"%7B%22Hidden%22%3A%5B{hidden}%5D%2C%22NamespaceID%22%3A%22{namespace_id}%22%7D"
            first_page = self.__admin_data.get_lab_objects(
                params=f"?pagination.current=1&pagination.size={page_size}&filters={filters}"
            )
            total_pages = first_page["pagination"]["total_pages"]
            namespace_labs = first_page["objects"]
            for page in track(
                range(2, total_pages + 1),
                description=f"Namespace: {namespace_id}, Total Pages: {total_pages}",
            ):
                page_data = self.__admin_data.get_lab_objects(
                    params=f"?pagination.current={page}&pagination.size={page_size}&filters={filters}"
                )
                namespace_labs.extend(page_data["objects"])
            print(f"Namespace: {namespace_id}, Labs: {len(namespace_labs)}")
            all_labs.extend(namespace_labs)
        # filter labs
        unverified_labs = [lab for lab in all_labs if lab["IsUnverified"] == True]
        unverified_labs_learned = [
            lab for lab in unverified_labs if lab["LearnedUsers"] > 0
        ]
        verified_labs = [lab for lab in all_labs if lab["IsUnverified"] == False]
        print(
            f"All Labs: {len(all_labs)}, Verified Labs: {len(verified_labs)}, Unverified Labs: {len(unverified_labs)}, Unverified Labs Learned: {len(unverified_labs_learned)}"
        )
        return verified_labs, unverified_labs, unverified_labs_learned

    def __get_issues_title(self, state: str) -> list:
        issues = self.repo.get_issues(state=state)
        all_issues = []
        for issue in issues:
            all_issues.append(issue.title)
        return list(set(all_issues))

    def __parse_lab(self, lab_data: dict) -> list:
        """Parse lab data"""
        lab_id = lab_data["id"]
        lab_title = lab_data["Title"]
        lab_path = lab_data["Path"]
        lab_derection = lab_path.split("/")[0]
        if lab_derection in self.path_alias:
            lab_alias = lab_derection
        else:
            lab_alias = "python"
        lab_type = lab_data["Type"]
        lab_url = f"https://labex.io/skilltrees/{lab_alias}/labs/{lab_id}"
        return lab_title, lab_path, lab_url, lab_derection, lab_type

    def __create_issue(
        self, lab_title, lab_path, lab_url, lab_derection, lab_type
    ) -> None:
        issue_body = f"""# {lab_title}

## 测试说明

1. 点击 Issue 右侧 Assignees，将测试 Issue 分配给自己，请勿选择已被别人认领的 Issue；
2. 请在 **认领后的 12 小时** 内完成 Issue 所关联的 Lab 测试，超期系统会自动取消认领；
4. 测试完成后，请编辑和补充下方的【测试检查单】和【测试报告】；
5. 测试完成后，请在右侧 Labels 里选择 `verified` 标签标记已完成测试，同时取消默认的 `unverified` 标签。如果相应 lab 存在问题需要修复，则同时添加 `needfix` 标签，如果无问题则添加 `wontfix` 标签；
7. 系统将进行测试完成状态核对，我们会对反馈问题进行修复；

## 测试地址

- 测试地址（右键新标签页面打开，若无法学习请联系我们）：{lab_url}

## 测试检查单

> 请点击复选框，勾选后自动保存。

1. 我以**用户视角**在默认环境中完成了 Lab 的学习，直到最后一步。
   - [ ] 是
2. 我确认此 Lab 存在以下问题：
   - [ ] 检测脚本在用户未操作时可以直接通过；
   - [ ] 检测脚本在操作正确时无法通过；
   - [ ] 检测脚本的提示不够明确和清晰；
   - [ ] 步骤无法走通，内容和代码不明晰，甚至错误；
   - [ ] 存在明显的格式问题；
   - [ ] 无任何上述问题，但我认为此 Lab 用户可以正常学习。
3. 评价此 Lab 的质量：
   - [ ] 我认为此 Lab 的质量不错，建议保留；
   - [ ] 我认为此 Lab 的质量还行，建议修复；
   - [ ] 我认为此 Lab 的质量不佳，建议移除；

## 测试报告

请以评论的方式，将您测试的问题反馈到此 issue 中。

请务必详细描述问题和复现方法，并补充截图（直接粘贴到本评论框）或录屏（可以使用 [芦笋](https://lusun.com) 分享录屏链接）。

问题记录模板可以参考下方，也可以根据需要自定义格式，确保我们不需要多余的沟通就能看懂即可。

- 问题描述：
- 复现方法：
- 截图或录屏：
"""
        # create issue
        issue = self.repo.create_issue(
            title=lab_path,
            body=issue_body,
            labels=["unverified", lab_type, lab_derection],
        )
        print(issue)

    def main(self):
        all_issues = self.__get_issues_title(state="all")
        print(f"All Issues: {len(all_issues)}")
        # get all labs by below params
        hidden = "false"
        page_size = 100
        namespace_ids = [2, 3, 455]
        verified_labs, unverified_labs, unverified_labs_learned = self.__get_all_labs(
            hidden, namespace_ids, page_size
        )
        # create issue for new unverified learned labs
        for lab in unverified_labs_learned:
            (
                lab_title,
                lab_path,
                lab_url,
                lab_derection,
                lab_type,
            ) = self.__parse_lab(lab)
            if lab_path not in all_issues:
                self.__create_issue(
                    lab_title, lab_path, lab_url, lab_derection, lab_type
                )
                print(
                    f"Create Issue: {lab_path}, it has been learned {lab['LearnedUsers']} times."
                )
        # close issue for verified labs without assignees
        open_issues = self.repo.get_issues(state="open")
        verified_labs_path = [lab["Path"] for lab in verified_labs]
        close_issue_count = 0
        for issue in open_issues:
            issue_title = issue.title
            issue_assignees = issue.assignees
            if issue_title in verified_labs_path and len(issue_assignees) == 0:
                issue.create_comment(
                    "This issue is closed by system, because it is verified."
                )
                issue_labels = [label.name for label in issue.labels]
                issue_labels.remove("unverified")
                issue_labels.extend(["verified", "wontfix", "autoclosed"])
                issue.edit(state="closed", labels=issue_labels)
                print(f"Close Issue: {issue_title}, because it is verified.")
                close_issue_count += 1
        print(
            f"Open Issues: {open_issues.totalCount}, Auto Close Issues: {close_issue_count}"
        )
