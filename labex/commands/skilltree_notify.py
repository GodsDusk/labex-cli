import json
import random
from rich import print
import pandas as pd
from .utils.api import UserData, AdminData


class SkillTreeNotify:
    def __init__(self) -> None:
        self.__user_data = UserData()
        self.__admin_data = AdminData()
        self.page_size = 50
        self.min_labs = 5

    def __get_skilltree(self) -> list:
        """Get all skilltree

        Returns:
            list: list of skilltree
        """
        paths = self.__user_data.get_all_path()["paths"]
        print(f"[bold green]→[/bold green] Found {len(paths)} existed paths")
        skill_trees = []
        for path in paths:
            skill_trees.append(
                {
                    "alias": path["alias"],
                    "labs_count": path["labs_count"] + path["challenges_count"],
                }
            )
        return skill_trees

    def __random_labs(self, path_alias: str, page: int) -> list:
        """Get random labs

        Args:
            page (int): page number

        Returns:
            list: list of labs
        """
        params = f"?pagination.current={page}&pagination.size={self.page_size}"
        labs = self.__user_data.get_path_labs(path_alias, params)["labs"]
        return labs

    def __get_existed_labs(self) -> list:
        """Get existed labs

        Returns:
            list: list of existed labs
        """
        all_notify = self.__admin_data.get_skilltree_notify()
        configs = all_notify["configs"]
        notify_ids = [c["id"] for c in configs]
        existed_labs = []
        for nid in notify_ids:
            config_raw = self.__admin_data.get_skilltree_notify_by_id(nid)["config"]
            skill_tree_config = json.loads(config_raw)
            for sk in skill_tree_config:
                sk_labs = sk["labs"]
                existed_labs.extend(sk_labs)
        print(
            f"[bold green]→[/bold green] Found {len(existed_labs)} existed labs in {len(notify_ids)} existed notify configs"
        )
        return list(set(existed_labs))

    def labs_from_skilltrees(self) -> list:
        existed_labs = self.__get_existed_labs()
        skill_trees = self.__get_skilltree()
        notify_config = []
        labs_for_testing = []
        for st in skill_trees:
            st_alias = st["alias"]
            st_labs_count = st["labs_count"]
            st_config = {"skilltree": st_alias, "labs": []}
            print(
                f"[bold green]→[/bold green] Found {st_labs_count} labs in {st_alias}"
            )
            get_random_labs = True
            while get_random_labs:
                # Get random page
                page_count = st_labs_count // self.page_size + 1
                random_page = random.randint(1, page_count)
                # Get random labs
                labs = self.__random_labs(st_alias, random_page)
                print(
                    f"[bold green]✓[/bold green] Get {len(labs)} labs in page {random_page} of {st_alias}"
                )
                labs_id = [l["id"] for l in labs]
                # Remove existed labs
                labs_without_existed = list(set(labs_id) - set(existed_labs))
                # Check labs count
                if len(labs_without_existed) >= self.min_labs:
                    keep_random_min_labs = random.sample(
                        labs_without_existed, self.min_labs
                    )
                    print(
                        f"[bold green]✓[/bold green] Pick {len(keep_random_min_labs)} randoms labs in {st_alias}"
                    )
                    st_config["labs"] = keep_random_min_labs
                    get_random_labs = False
                else:
                    print(
                        f"[bold yellow]⚠[/bold yellow] Pick {len(labs_without_existed)} randoms labs in {st_alias}, Try again..."
                    )
                    continue
            notify_config.append(st_config)
            # add original labs for testing
            for lab_id in st_config["labs"]:
                lab_raw = [l for l in labs if l["id"] == lab_id][0]
                labs_for_testing.append(
                    {
                        "id": lab_raw["id"],
                        "name": lab_raw["name"],
                        "difficulty": lab_raw["difficulty"],
                        "path": lab_raw["path"],
                        "skilltree": st_alias,
                        "url": f"https://labex.io/skilltrees/{st_alias}/labs/{lab_raw['id']}",
                    }
                )

        # save to file
        with open("notify_config.json", "w") as f:
            json.dump(notify_config, f, indent=4)
            print(
                f"[bold green]✓[/bold green] Save notify config to notify_config.json"
            )
        df = pd.DataFrame(labs_for_testing)
        print(df)
        df.to_csv("labs_for_testing.csv", index=False)
        print(
            f"[bold green]✓[/bold green] Save labs for testing to labs_for_testing.csv"
        )
