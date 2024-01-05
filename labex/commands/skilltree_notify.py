import json
import random
from rich import print
from .utils.labex_api import UserData, AdminData


class SkillTreeNotify:
    def __init__(self) -> None:
        self.labex_user_data = UserData()
        self.labex_admin_data = AdminData()
        self.page_size = 50
        self.lab_count = 3
        self.course_count = 2
        self.project_count = 2

    def __get_skilltree(self) -> list:
        """Get all skilltree

        Returns:
            list: list of skilltree
        """
        paths = self.labex_user_data.get_all_path()["paths"]
        print(f"→ Found {len(paths)} existed paths in LabEx")
        skill_trees = []
        for path in paths:
            skill_trees.append(
                {
                    "alias": path["alias"],
                    "name": path["name"],
                    "course_count": path["course_count"],
                    "projects_count": path["challenges_count"],
                    "labs_count": path["labs_count"] + path["challenges_count"],
                }
            )
        # delete alibabacloud
        skill_trees = [st for st in skill_trees if st["alias"] != "alibabacloud"]
        # delete labs_count < 20
        skill_trees = [st for st in skill_trees if st["labs_count"] >= 20]
        print(f"→ {len(skill_trees)} Skill Trees after filtered")
        return skill_trees

    def __random_labs(self, path_alias: str, page: int) -> list:
        """Get random labs

        Args:
            page (int): page number

        Returns:
            list: list of labs
        """
        params = f"?pagination.current={page}&pagination.size={self.page_size}"
        labs = self.labex_user_data.get_path_labs(path_alias, params)
        return labs

    def __get_existed_labs(self) -> list:
        """Get existed labs

        Returns:
            list: list of existed labs
        """
        all_notify = self.labex_admin_data.get_skilltree_notify()
        objects = all_notify["objects"]
        existed_labs = []
        existed_courses = []
        existed_projects = []
        for obj in objects:
            config = obj["Configs"]
            for con in config:
                labs = con["Labs"]
                courses = con["Courses"]
                projects = con["Projects"]
                existed_labs.extend(labs)
                existed_courses.extend(courses)
                existed_projects.extend(projects)
        existed_labs = list(set(existed_labs))
        existed_courses = list(set(existed_courses))
        existed_projects = list(set(existed_projects))
        print(
            f"→ Found {len(existed_labs)} existed labs, {len(existed_courses)} existed courses, {len(existed_projects)} existed projects\n"
        )
        return existed_labs, existed_courses, existed_projects

    def __pick_labs(self, skill_trees, existed_labs) -> list:
        print(
            f"[bold green]================ PICK RANDOM LABS ================[/bold green]"
        )
        notify_config = []
        for st in skill_trees:
            st_alias = st["alias"]
            st_labs_count = st["labs_count"]
            st_config = {"skilltree": st_alias, "labs": []}
            print(f"→ Found {st_labs_count} labs in {st_alias}")
            get_random_labs = True
            get_random_count = 0
            while get_random_labs:
                # Get random page
                page_count = st_labs_count // self.page_size + 1
                random_page = random.randint(1, page_count)
                # Get random labs
                labs = self.__random_labs(st_alias, random_page)
                print(f"✔ Get {len(labs)} labs in page {random_page} of {st_alias}")
                labs_id = [l["id"] for l in labs]
                if get_random_count < 5:
                    # Remove existed labs
                    labs_without_existed = list(set(labs_id) - set(existed_labs))
                else:
                    labs_without_existed = labs_id
                # Check labs count
                if len(labs_without_existed) >= self.lab_count:
                    keep_random_min_labs = random.sample(
                        labs_without_existed, self.lab_count
                    )
                    print(
                        f"✔ Pick {len(keep_random_min_labs)} randoms labs in {st_alias}"
                    )
                    st_config["labs"] = keep_random_min_labs
                    get_random_labs = False
                else:
                    print(
                        f"[bold yellow]→[/bold yellow] Pick {len(labs_without_existed)} randoms labs in {st_alias}, Try {get_random_count + 1} times more"
                    )
                    get_random_count += 1
                    continue
            notify_config.append(st_config)
        return notify_config

    def __pick_courses(self, skill_trees, notify_config) -> list:
        print(
            f"[bold green]================== PICK COURSES ==================[/bold green]"
        )
        for st in skill_trees:
            st_alias = st["alias"]
            st_name = st["name"]
            print(f"→ Process [bold]{st_name}[/bold] Skill Tree")
            # Get courses
            all_courses = self.labex_user_data.get_skilltree_courses(tags=st_name)
            # Pick courses
            courses = [p for p in all_courses if p["type"] == 0]
            if len(courses) == 0:
                print(
                    f"[bold yellow]→[/bold yellow] Not found courses, random pick one from all projects"
                )
                all_courses = self.labex_user_data.get_skilltree_courses(tags=None)
                courses = [p for p in all_courses if p["type"] == 0]
            if len(courses) > self.course_count:
                random_courses = random.sample(courses, self.course_count)
            else:
                random_courses = courses
            random_courses_name = [p["name"] for p in random_courses]
            print(
                f"[bold green]✔ COURSES[/bold green]: {', '.join(random_courses_name)}"
            )
            # Pick project
            projects = [p for p in all_courses if p["type"] == 3]
            if len(projects) == 0:
                print(
                    f"[bold yellow]→[/bold yellow] Not found projects, random pick one from all projects"
                )
                all_courses = self.labex_user_data.get_skilltree_courses(tags=None)
                projects = [p for p in all_courses if p["type"] == 3]
            if len(projects) > self.project_count:
                random_projects = random.sample(projects, self.project_count)
            else:
                random_projects = projects
            random_projects_name = [p["name"] for p in random_projects]
            print(
                f"[bold green]✔ PROJECTS[/bold green]: {', '.join(random_projects_name)}"
            )
            for nc in notify_config:
                if nc["skilltree"] == st_alias:
                    nc["courses"] = [p["id"] for p in random_courses]
                    nc["projects"] = [p["id"] for p in random_projects]
        return notify_config

    def main(self):
        skill_trees = self.__get_skilltree()
        existed_labs, _, _ = self.__get_existed_labs()
        notify_config = self.__pick_labs(skill_trees, existed_labs)
        notify_config = self.__pick_courses(skill_trees, notify_config)
        print(notify_config)
        # save notify_config to yaml
        with open("notify_config.yaml", "w") as f:
            f.write("# Skilltree notify config\n")
            f.write("# This file is auto generated by labex-cli\n")
            f.write("# DO NOT EDIT THIS FILE\n")
            f.write("---\n")
            for nc in notify_config:
                f.write(f"- Skilltree: {nc['skilltree']}\n")
                f.write("  Labs:\n")
                for lab in nc["labs"]:
                    f.write(f"    - {lab}\n")
                f.write("  Courses:\n")
                for course in nc["courses"]:
                    f.write(f"    - {course}\n")
                f.write("  Projects:\n")
                for project in nc["projects"]:
                    f.write(f"    - {project}\n")
        print(f"[bold green]✔ Save notify config to notify_config.yaml[/bold green]")
