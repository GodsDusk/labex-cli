import re
from rich import print
from datetime import datetime, timedelta
from .utils.feishu_api import Feishu
from .utils.github_api import GitHub


class SyncPRToFeishu:
    def __init__(self, app_id: str, app_secret: str, ghtoken: str) -> None:
        self.ghtoken = ghtoken
        self.github = GitHub(token=ghtoken)
        self.feishu = Feishu(app_id, app_secret)
        self.app_token = "bascnNz4Nqjqgqm1Nm5AYke6xxb"
        self.table_id = "tblExqBjw46rHCre"

    def __unix_ms_timestamp(self, time_str: str) -> int:
        if time_str != None:
            date_obj = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ") + timedelta(
                hours=8
            )
            unix_ms_timestamp = int(date_obj.timestamp() * 1000)
        else:
            unix_ms_timestamp = 946656000000
        return unix_ms_timestamp

    def __date_milestone(self, date_str: str) -> int:
        """获取日期所在周数组成 milestone

        Args:
            date_str (str): 2023-04-21T07:06:13Z

        Returns:
            int: 16
        """
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        year = date_obj.year
        week_num = date_obj.isocalendar()[1]
        milestone = f"{year}W{week_num}"
        return milestone

    def __sunday_of_date(self, date_str: str) -> str:
        """根据日期推算出当周的周日

        Args:
            date_str (str): 2023-10-04T08:30:00Z

        Returns:
            str: 2023-10-08T23:59:59Z
        """
        # Parse the input date string
        input_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        # Calculate the day of the week (0 = Monday, 6 = Sunday)
        day_of_week = input_date.weekday()
        # Calculate the number of days to add to reach the next Sunday (6 - day_of_week)
        days_until_sunday = (6 - day_of_week) % 7
        # Calculate the date of the next Sunday
        next_sunday = input_date + timedelta(days=days_until_sunday)
        # Set the time to 23:59:59
        next_sunday = next_sunday.replace(hour=23, minute=59, second=59)
        # Format the result as a string
        result_date_string = next_sunday.strftime("%Y-%m-%dT%H:%M:%SZ")
        return result_date_string

    def __get_pr_assign_issue_id(self, pr_body: str) -> int:
        issue_id_str_1 = re.findall(r"- fix #(\d+)", pr_body)
        issue_id_str_2 = re.findall(
            r"- fix https:\/\/github\.com\/labex-labs\/scenarios\/issues\/(\d+)",
            pr_body,
        )
        try:
            issue_id = int(issue_id_str_1[0])
        except:
            try:
                issue_id = int(issue_id_str_2[0])
            except:
                issue_id = 0
        return issue_id

    def sync_pr(self, repo_name: str) -> None:
        print(f"[yellow]➜ TASKS:[/yellow] Sync PR to Feishu")
        print(f"[yellow]➜ TASK1:[/yellow] Get data from Feishu")
        # Get all records from feishu
        records = self.feishu.get_bitable_records(
            self.app_token, self.table_id, params=""
        )
        # Make a dict of PR_NUMBER and record_id
        num_id_dicts = {r["fields"]["PR_NUM"]: r["record_id"] for r in records}
        print(f"[yellow]➜ TASK2:[/yellow] Get data from GitHub")
        print(f"[yellow]➜ REPO:[/yellow] {repo_name}")
        # Get all pr from github
        pr_list = self.github.get_pr_list(repo_name)
        print(f"[green]✔ PRs:[/green] {len(pr_list)}")
        # Get all milestone from github
        milestones = self.github.list_milestone(repo_name)
        print(f"[green]✔ MILESTONE:[/green] {len(milestones)}")
        # List all collaborators
        collaborators = self.github.list_collaborators(repo_name)
        print(f"[green]✔ COLLABORATORS:[/green] {len(collaborators)}")
        print(f"[yellow]➜ TASK3:[/yellow] Processing data")
        # Feishu 未关闭的 PR
        feishu_not_closed_pr_nums = [
            str(r["fields"]["PR_NUM"])
            for r in records
            if r["fields"]["PR_STATE"] == "OPEN"
            and r["fields"]["REPO_NAME"] == repo_name
        ]
        # 忽略已经关闭的 PR
        pr_list = [
            pr
            for pr in pr_list
            if pr["state"] == "open" or str(pr["number"]) in feishu_not_closed_pr_nums
        ]
        # 忽略 locked 的 PR
        pr_list = [pr for pr in pr_list if pr["locked"] == False]
        print(f"[green]✔ OPEN PRs:[/green] {len(pr_list)}")
        print(f"[yellow]➜ TASK4:[/yellow] Loop all PRs")
        # Loop all PRs
        for pr in pr_list:
            try:
                ###################
                # STEP1 解析 PR 数据
                ###################

                pr_number = pr["number"]
                pr_user = pr["user"]["login"]
                pr_state = pr["state"]
                # assignees
                assignees = pr["assignees"]
                if len(assignees) == 0 or assignees == None:
                    assignees_list = []
                else:
                    assignees_list = [a["login"] for a in assignees]
                # labels
                pr_labels = pr["labels"]
                if len(pr_labels) == 0:
                    pr_labels_list = []
                else:
                    pr_labels_list = [l["name"] for l in pr_labels]
                print(f"\n[yellow]➜ PR NUM:[/yellow] {pr_number}")
                print(
                    f"[yellow]➜ PR URL:[/yellow] https://github.com/{repo_name}/pull/{pr_number}"
                )
                # 从 PR 中获取 index.json
                index_json, lab_path = self.github.pr_index_json(repo_name, pr_number)
                # 如果 index.json 不存在
                if index_json == None:
                    print(f"[red]➜ SKIPPED:[/red] No index.json found.")
                    return

                ###################
                # STEP2 更新 PR 状态
                ###################

                # 判断 PR 是否已经合并或关闭
                if pr_state != "open":
                    print(f"[red]➜ SKIPPED:[/red] PR is not open.")
                    return
                # 判断 PR 是否已经测试完成
                if "Test Completed" not in pr_labels_list:
                    print(f"[red]➜ SKIPPED:[/red] PR is not tested completed.")
                    return
                # 判断 PR 是否正确关联了 issue 或者选择了 noissue
                if issue_id == 0 and "noissue" not in pr_labels_list:
                    comment = f"Hi, @{pr_user} \n\n该 PR 未检测到正确关联 Issue, 无法分配 Reviewer。请你在 PR 描述中按要求添加, 如有问题请及时联系 LabEx 的同事。如果该 PR 无需关联 Issue, 请在 Labels 中选择 `noissue`, 系统将会忽略 Issue 绑定检查。\n\n[❓ 如何提交](https://www.labex.wiki/zh/advanced/how-to-submit) | [✍️ LabEx 手册](https://www.labex.wiki/zh/advanced/how-to-review) | [🏪 LabEx 网站](https://labex.io) \n\n> 这是一条自动消息, 如有疑问可以直接回复本条评论, 或者微信联系。"
                    self.github.comment_pr(repo_name, pr_number, comment)
                    print(f"→ No issue id found in {pr_number}, comment to {pr_user}")
                    return
                # 如果检查通过, 则更新 PR 状态

                # STEP1 更新 Milestone
                # 获取已经存在的 milestone
                pr_milestone = pr.get("milestone")
                # 如果 PR 原本存在 milestone
                if pr_milestone != None:
                    print(f"[red]➜ SKIPPED:[/red] PR already has a milestone.")
                    return
                # 如果 PR 原本不存在 milestone
                # 使用更新日期所在的周作为 milestone
                date_milestone_str = self.__date_milestone(pr["updated_at"])
                pr_milestone_number = milestones.get(date_milestone_str, None)
                # 如果 pr_milestone_number 不存在, 则创建 milestone
                if pr_milestone_number == None:
                    # 获取周日日期
                    due_on = self.__sunday_of_date(pr["updated_at"])
                    # 创建 milestone
                    self.github.create_milestone(repo_name, date_milestone_str, due_on)
                    # 重新获取 pr_milestone_number
                    milestones = self.github.list_milestone(repo_name)
                    pr_milestone_number = milestones.get(date_milestone_str, None)
                # 如果 pr_milestone_number 依然不存在, 则跳过
                if pr_milestone_number == None:
                    print(f"[red]➜ SKIPPED:[/red] PR milestone still not found.")
                    return
                # 如果 pr_milestone_number 存在, 则更新 milestone
                payloads = {"milestone": pr_milestone_number}
                self.github.patch_pr(
                    repo_name,
                    pr_number,
                    payloads,
                )
                print(
                    f"[green]➜ UPDATED:[/green] PR milestone to {date_milestone_str}, {pr_milestone_number}"
                )
                # STEP2 为 PR 添加 Reviewer
                # 从 PR 描述中获取 issue id
                pr_body = pr["body"]
                issue_id = self.__get_pr_assign_issue_id(pr_body)
                # 如果 issue_id 不为 0, 则获取 issue user
                if issue_id != 0:
                    issue = self.github.get_issue(repo_name, issue_id)
                    issue_user = issue["user"]["login"]
                # 如果 issue_id 为 0, 则将 issue_user 设置为 huhuhang
                else:
                    issue_user = "huhuhang"

                # 选择设置 reviewer
                # 一般情况下, 如果 issue user 为 reviewer
                reviewer = issue_user
                # 如果 issue user 不在 collaborators 里, 则设置 reviewer 为 huhuhang
                if issue_user not in collaborators:
                    reviewer = "huhuhang"
                # 检查 issue user 是否和 pr user 相同，则添加 huhuhang 为 reviewer
                if issue_user == pr_user:
                    reviewer = "huhuhang"
                # 准备更新 assignees
                # 如果 reviewer 已经是 assignees, 则跳过添加
                if reviewer in assignees_list:
                    print(f"[green]➜ SKIPPED:[/green] {reviewer} already in assignees.")
                    return
                # 如果 reviewer 不在 assignees 里, 则添加 reviewer
                assignees_list.append(reviewer)
                payloads = {"assignees": assignees_list}
                self.github.patch_pr(
                    repo_name,
                    pr_number,
                    payloads,
                )
                # 添加评论通知 reviewer
                comment = f"Hi, @{pr_user} \n\n系统已将 @{reviewer} 自动分配为 Reviewer。一般情况下，@{reviewer} 会在 2 个工作日内完成 Review, 并与你沟通。如果一直没有进展，请及时通过评论或微信群与 @{reviewer} 联系确认。\n\n[❓ 如何 Review](https://www.labex.wiki/zh/advanced/how-to-review) | [✍️ LabEx 手册](https://www.labex.wiki/zh/advanced/how-to-review) | [🏪 LabEx 网站](https://labex.io) \n\n> 这是一条自动消息, 如有疑问可以直接回复本条评论, 或者微信联系。"
                self.github.comment_pr(repo_name, pr_number, comment)
                print(f"[green]➜ UPDATED:[/green] {reviewer} added as a reviewer.")

                #######################
                # STEP3 更新 Feishu 记录
                #######################

                # 解析 index.json
                lab_title = index_json.get("title")
                lab_type = index_json.get("type")
                lab_steps = index_json.get("details").get("steps")
                pr_title = pr["title"]
                pr_html_url = pr["html_url"]
                approved_by, changes_requested_by = self.github.pr_reviews(
                    repo_name, pr_number
                )
                # created at
                created_at = self.__unix_ms_timestamp(pr["created_at"])
                updated_at = self.__unix_ms_timestamp(pr["updated_at"])
                merged_at = self.__unix_ms_timestamp(pr["merged_at"])
                # payloads
                payloads = {
                    "fields": {
                        "SCENARIO_TITLE": lab_title,
                        "SCENARIO_PATH": lab_path,
                        "SCENARIO_SLUG": lab_path.split("/")[-1],
                        "SCENARIO_TYPE": lab_type,
                        "SCENARIO_STEP": len(lab_steps),
                        "PR_TITLE": pr_title,
                        "PR_USER": pr_user,
                        "PR_NUM": pr_number,
                        "PR_STATE": pr_state.upper(),
                        "PR_LABELS": pr_labels_list,
                        "REPO_NAME": repo_name,
                        "ASSIGNEES": assignees_list,
                        "MILESTONE": date_milestone_str,
                        "CHANGES_REQUESTED": changes_requested_by,
                        "APPROVED": approved_by,
                        "CREATED_AT": created_at,
                        "UPDATED_AT": updated_at,
                        "MERGED_AT": merged_at,
                        "HTML_URL": {
                            "link": pr_html_url,
                            "text": "OPEN IN GITHUB",
                        },
                    }
                }
                # Update record
                if str(pr_number) in num_id_dicts.keys():
                    r = self.feishu.update_bitable_record(
                        self.app_token,
                        self.table_id,
                        num_id_dicts[str(pr_number)],
                        payloads,
                    )
                    print(f"[green]➜ UPDATED:[/green] {lab_path} {r['msg'].upper()}")
                else:
                    # Add record
                    r = self.feishu.add_bitable_record(
                        self.app_token, self.table_id, payloads
                    )
                    print(f"[green]➜ ADDED:[/green] {lab_path} {r['msg'].upper()}")

            except Exception as e:
                print(f"Exception: {e}")
                continue
