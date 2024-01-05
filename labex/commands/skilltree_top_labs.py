from rich import print
from .utils.feishu_api import Feishu
from .utils.labex_api import UserData, AdminData


class TopLabs:
    def __init__(self, app_id, app_secret) -> None:
        self.labex_user_data = UserData()
        self.labex_admin_data = AdminData()
        self.feishu = Feishu(app_id, app_secret)

    def __parse_skills_tree(self) -> dict:
        skills_tree = self.labex_admin_data.get_show_normal_paths()
        trees = []
        for tree in skills_tree:
            tree_id = tree["id"]
            tree_alias = tree["Meta"]["AliasURI"][0]
            tree_first_course = tree["Meta"]["Levels"][0]["Courses"][0]
            trees.append(
                {
                    "id": tree_id,
                    "alias": tree_alias,
                    "first_course": tree_first_course,
                }
            )
        return trees

    def __get_pro_labs(self, tree_alias: str, page_size: int) -> list:
        pro_labs = self.labex_user_data.get_path_labs(
            path_alias=tree_alias,
            params=f"?fee_types=2&pagination.current=1&pagination.size={page_size}",
        )
        labs_path = [lab["path"] for lab in pro_labs]
        return labs_path

    def __get_course_labs(self, course_alias: str) -> list:
        course_labs = self.labex_user_data.get_course_labs(course_alias)
        labs_path = [lab["path"] for lab in course_labs]
        return labs_path

    def __parse_lab_path(self) -> dict:
        # get all feishu records
        app_token = "bascnNz4Nqjqgqm1Nm5AYke6xxb"
        lab_table_id = "tblW2umsCYJWzzUX"
        records = self.feishu.get_bitable_records(app_token, lab_table_id, params="")
        # Drop Duplicate records
        records = list({v["fields"]["PATH"]: v for v in records}.values())
        print(f"Found {len(records)} labs in Feishu after deduplication.")
        # Make a full dict of path and record_id and repo_name
        path_dicts = {
            r["fields"]["PATH"]: f"{r['fields']['REPO_NAME']}:{r['fields']['PATH']}"
            for r in records
        }
        return path_dicts

    def main(self, pro_labs: int) -> None:
        path_dicts = self.__parse_lab_path()
        trees = self.__parse_skills_tree()
        print(f"Get {len(trees)} skills tree")
        for tree in trees:
            tree_id = tree["id"]
            tree_alias = tree["alias"]
            course_alias = tree["first_course"]
            # get first course labs
            first_course_labs = self.__get_course_labs(course_alias)
            # select first 5 labs
            first_five_labs = first_course_labs[:5]
            # get pro labs
            page_size = pro_labs - len(first_five_labs)
            pro_labs = self.__get_pro_labs(tree_alias, page_size)
            tree_lab_path = first_five_labs + pro_labs
            # get real lab path
            real_lab_path = [
                path_dicts.get(p) for p in tree_lab_path if path_dicts.get(p) != None
            ]
            print(
                f"Get {len(tree_lab_path)} labs for [red]{tree_alias}[/red], {len(first_five_labs)} from the first course, {len(pro_labs)} from the pro list. {len(real_lab_path)} labs will update to first page in skills tree."
            )
            if len(real_lab_path) > 0:
                # update skill tree top labs
                self.labex_user_data.set_top_labs(path_id=tree_id, labs=real_lab_path)
