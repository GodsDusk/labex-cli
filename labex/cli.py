import os
import click

from .commands.utils.version import CheckUpdate
from .commands.utils.auth import LabExLogin

from .commands.lab_create import CreateLab
from .commands.lab_unverified import LabForTesting

from .commands.lab_translate import Translator
from .commands.lab_split import MDSplitter

from .commands.index_check import CheckIndexValidation
from .commands.index_update_title import UpdateIndexTitle
from .commands.index_add_fee_type import SetFeeType
from .commands.index_add_contributors import AddContributors
from .commands.index_update_step_name import StandardName
from .commands.index_add_skills import AddSkills
from .commands.index_update_time import UpdateIndexTime

from .commands.skilltree_export import ExportSkills
from .commands.skilltree_notify import SkillTreeNotify
from .commands.skilltree_top_labs import TopLabs

from .commands.sync_pr_to_feishu import SyncPRToFeishu
from .commands.sync_labs_to_feishu import SyncLabsToFeishu
from .commands.sync_issues_to_feishu import SyncIssuesToFeishu
from .commands.sync_course_to_feishu import SyncCoursesToFeishu

from .commands.project_create import CreateProject


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """LabEx Command Line Interface"""
    pass


@click.command()
@click.option("--username", type=str, help="Username")
@click.option("--password", type=str, help="Password")
@click.option(
    "--check",
    type=bool,
    default=True,
    show_default=True,
    help="Check for version updates.",
)
def login(username, password, check):
    """LOG IN TO LABEX

    \b
    Support passing in the username and password as parameters. If they do not exist, prompt for login.
    """
    LabExLogin().login_account(un=username, pw=password, check=check)


cli.add_command(login)


# ==================
# LAB COMMANDS GROUP
# ==================


@click.group(context_settings=CONTEXT_SETTINGS)
def lab():
    """LAB COMMANDS GROUP"""
    pass


cli.add_command(lab)


@click.command()
@click.option(
    "--path",
    type=str,
    help="if not set, it will create a new lab in the current directory",
)
def create(path):
    """CREATE NEW LABS"""
    CheckUpdate().check_version()
    if path is None:
        CreateLab().init_base()
    if path.endswith(".ipynb"):
        CreateLab().init_notebook(path)


lab.add_command(create)


@click.command(no_args_is_help=True)
@click.option(
    "--repo",
    type=str,
    help="Repo Name like 'labex-labs/scenarios'",
)
@click.option(
    "--mode",
    type=click.Choice(["create", "close"]),
    default="create",
    show_default=True,
    help="Set mode to create or close",
)
def unverified(mode, repo):
    """CREATE UNVERIFIED LAB ISSUES"""
    if mode == "create":
        LabForTesting(repo).main()


lab.add_command(unverified)


@click.command(no_args_is_help=True)
@click.option(
    "--path",
    type=str,
    help="md/ipynb file path",
    metavar="<path>",
)
@click.option(
    "--gpt",
    default="gpt-35-turbo",
    show_default=True,
    type=click.Choice(["gpt-35-turbo", "gpt-35-turbo-16k", "gpt-4"]),
)
def translate(path, gpt):
    """TRANSLATE MD/IPYNB FILE"""
    translator = Translator(gpt_model=gpt)
    if os.path.isfile(path) and path.endswith(".md"):
        translator.translate_md(path)
    elif os.path.isfile(path) and path.endswith(".ipynb"):
        translator.translate_ipynb(path)
    elif os.path.isdir(path):
        translator.translate_lab(path)


lab.add_command(translate)


@click.command(no_args_is_help=True)
@click.option(
    "--path",
    type=str,
    help="Path to md file",
    metavar="<path>",
)
def split(path):
    """SPLITE MD FILE"""
    MDSplitter().new_lab(md_path=path)


lab.add_command(split)

# =========================
# INDEX JSON COMMANDS GROUP
# =========================


@click.group(context_settings=CONTEXT_SETTINGS)
def idx():
    """INDEX JSON COMMANDS GROUP"""
    pass


cli.add_command(idx)


@click.command(no_args_is_help=True)
@click.option(
    "--instance",
    type=str,
    required=True,
    help="index.json file path",
    metavar="<path>",
)
def check(instance):
    """Check index.json based on schema.json

    - instance: index.json file path
    """
    if instance is None:
        CheckIndexValidation().validate_all_json("./")
    else:
        CheckIndexValidation().validate_json(instance)


idx.add_command(check)


@click.group(context_settings=CONTEXT_SETTINGS)
def update():
    """INDEX UPDATE COMMANDS GROUP"""
    pass


idx.add_command(update)


@click.command()
@click.option(
    "--path",
    type=str,
    default="./",
    show_default=True,
    help="Path",
    metavar="<path>",
)
def title(path):
    """Update lab title from md files
    - excute from lab directory
    """
    UpdateIndexTitle().title(path)


update.add_command(title)


@click.command()
@click.option(
    "--path",
    type=str,
    default="./",
    show_default=True,
    help="Path",
    metavar="<path>",
)
def time(path):
    """Update lab time in index.json"""
    UpdateIndexTime().update_time(path)


update.add_command(time)


@click.command(no_args_is_help=True)
@click.option(
    "--path",
    type=str,
    default="./",
    show_default=True,
    help="Path to Repo",
    metavar="<path>",
)
@click.option(
    "--mode",
    type=click.Choice(["check", "update"]),
    default="check",
    show_default=True,
    help="check first, then update",
)
def stepname(path, mode):
    """Standardize the name of the index.json file and the step file."""
    StandardName(path=path).main(mode=mode)


update.add_command(stepname)


@click.group(context_settings=CONTEXT_SETTINGS)
def add():
    """INDEX ADD COMMANDS GROUP"""
    pass


idx.add_command(add)


@click.command(no_args_is_help=True)
@click.option(
    "--ghtoken",
    type=str,
    required=True,
    help="Github Token",
)
@click.option(
    "--repo",
    type=str,
    required=True,
    help="Repo Name like 'labex-labs/scenarios'",
)
@click.option(
    "--path",
    type=str,
    default="./",
    show_default=True,
    help="Path to Repo",
    metavar="<path>",
)
def contributors(ghtoken, repo, path):
    """Add Repo Contributors to index.json"""
    AddContributors(ghtoken=ghtoken).add_contributors(path=path, repo=repo)


add.add_command(contributors)


@click.command(no_args_is_help=True)
@click.option(
    "--path",
    type=str,
    default="./",
    show_default=True,
    help="Path to index.json files",
    metavar="<path>",
)
@click.option(
    "--type",
    type=click.Choice(["pro", "free"]),
    default="pro",
    show_default=True,
    help="Set pro or free",
)
@click.option(
    "--mode",
    type=str,
    default="cli",
    show_default=True,
    help="cli mode or not",
)
def feetype(path, type, mode):
    """Set lab feetype
    - excute from lab directory
    """
    SetFeeType().set(path, type, mode)


add.add_command(feetype)


@click.command(no_args_is_help=True)
@click.option(
    "--path",
    type=str,
    default="./",
    show_default=True,
    help="Directory path",
    metavar="<path>",
)
@click.option(
    "--skilltree",
    type=click.Choice(list(AddSkills().languages.keys())),
    help="choose a skilltree",
)
def skills(path, skilltree):
    """Add skills to index.json"""
    AddSkills().add_skills(dir_path=path, skilltree=skilltree)


add.add_command(skills)


# =========================
# SKILL TREE COMMANDS GROUP
# =========================


@click.group(context_settings=CONTEXT_SETTINGS)
def skt():
    """SKILL TREE COMMANDS GROUP"""
    pass


cli.add_command(skt)


@click.command(no_args_is_help=True)
@click.option(
    "--appid",
    type=str,
    required=True,
    help="Feishu App ID",
)
@click.option(
    "--appsecret",
    type=str,
    required=True,
    help="Feishu App Secret",
)
def export(appid, appsecret):
    """Export lab skills to csv"""
    ExportSkills(app_id=appid, app_secret=appsecret).export_skills()


skt.add_command(export)


@click.command()
def notify():
    """Notify SkillTree"""
    SkillTreeNotify().labs_from_skilltrees()


skt.add_command(notify)


@click.command(no_args_is_help=True)
@click.option(
    "--appid",
    type=str,
    required=True,
    help="Feishu App ID",
)
@click.option(
    "--appsecret",
    type=str,
    required=True,
    help="Feishu App Secret",
)
@click.option(
    "--num",
    type=int,
    required=True,
    help="Number of pro labs to be updated",
)
def toplabs(appid, appsecret, num):
    """Update SkillTree Top Labs"""
    TopLabs(appid, appsecret).main(pro_labs=num)


skt.add_command(toplabs)

# ===========================
# SYNC SCRIPTS COMMANDS GROUP
# ===========================


@click.group(context_settings=CONTEXT_SETTINGS)
def syc():
    """SYNC SCRIPTS COMMANDS GROUP"""
    pass


cli.add_command(syc)


@click.group(context_settings=CONTEXT_SETTINGS)
def feishu():
    """FEISHU SYNC COMMANDS GROUP"""
    pass


syc.add_command(feishu)


@click.command(no_args_is_help=True)
@click.option(
    "--appid",
    type=str,
    required=True,
    help="Feishu App ID",
)
@click.option(
    "--appsecret",
    type=str,
    required=True,
    help="Feishu App Secret",
)
@click.option(
    "--ghtoken",
    type=str,
    required=True,
    help="Github Token",
)
@click.option(
    "--repo",
    type=str,
    required=True,
    help="Github Repo Name",
)
def pr(appid, appsecret, ghtoken, repo):
    """Sync Repo PR to Feishu"""
    SyncPRToFeishu(app_id=appid, app_secret=appsecret, ghtoken=ghtoken).sync_pr(
        repo_name=repo
    )


feishu.add_command(pr)


@click.command(no_args_is_help=True)
@click.option(
    "--appid",
    type=str,
    required=True,
    help="Feishu App ID",
)
@click.option(
    "--appsecret",
    type=str,
    required=True,
    help="Feishu App Secret",
)
@click.option(
    "--repo",
    type=str,
    required=True,
    help="Github Repo Name",
)
@click.option(
    "--skip",
    type=bool,
    default=False,
    show_default=True,
    help="Skip the labs that have been synced. This option is prioritized over --full.",
)
@click.option(
    "--full",
    type=bool,
    default=False,
    show_default=True,
    help="Synchronize all labs without checking for changes in record fields.",
)
@click.option(
    "--path",
    type=str,
    default="./",
    show_default=True,
    help="Directory path",
)
def lab(appid, appsecret, repo, skip, full, path):
    """Sync Repo labs to Feishu"""
    SyncLabsToFeishu(app_id=appid, app_secret=appsecret, repo=repo).sync_labs(
        skip=skip, full=full, dirpath=path
    )


feishu.add_command(lab)


@click.command(no_args_is_help=True)
@click.option(
    "--appid",
    type=str,
    required=True,
    help="Feishu App ID",
)
@click.option(
    "--appsecret",
    type=str,
    required=True,
    help="Feishu App Secret",
)
@click.option(
    "--ghtoken",
    type=str,
    required=True,
    help="Github Token",
)
@click.option(
    "--repo",
    type=str,
    required=True,
    help="Github Repo Name",
)
def issue(appid, appsecret, ghtoken, repo):
    """Sync Repo Issues to Feishu"""
    SyncIssuesToFeishu(app_id=appid, app_secret=appsecret, ghtoken=ghtoken).sync_issues(
        repo_name=repo
    )


feishu.add_command(issue)


@click.command(no_args_is_help=True)
@click.option(
    "--appid",
    type=str,
    required=True,
    help="Feishu App ID",
)
@click.option(
    "--appsecret",
    type=str,
    required=True,
    help="Feishu App Secret",
)
@click.option(
    "--repo",
    type=str,
    required=True,
    help="Github Repo Name",
)
@click.option(
    "--skip",
    type=bool,
    default=False,
    show_default=True,
    help="Skip the courses that have been synced. This option is prioritized over --full.",
)
@click.option(
    "--full",
    type=bool,
    default=False,
    show_default=True,
    help="Synchronize all courses without checking for changes in record fields.",
)
@click.option(
    "--path",
    type=str,
    default="./",
    show_default=True,
    help="Directory path",
)
def course(appid, appsecret, repo, skip, full, path):
    """Sync Repo courses to Feishu"""
    SyncCoursesToFeishu(app_id=appid, app_secret=appsecret, repo=repo).sync_courses(
        skip=skip, full=full, dirpath=path
    )


feishu.add_command(course)

# ======================
# PROJECT COMMANDS GROUP
# ======================


@click.group(context_settings=CONTEXT_SETTINGS)
def pro():
    """PROJECT COMMANDS GROUP"""
    pass


cli.add_command(pro)


@click.group(context_settings=CONTEXT_SETTINGS)
def create():
    """CREATE COMMANDS GROUP"""
    pass


pro.add_command(create)


@click.command(no_args_is_help=True)
@click.option(
    "--name",
    type=str,
    required=True,
    help="project name",
)
@click.option(
    "--desc",
    type=str,
    required=True,
    help="project description, end with a period.",
)
@click.option(
    "--path",
    type=str,
    default=".",
    show_default=True,
    help="path to save the project.",
)
@click.option(
    "--gpt",
    default="gpt-35-turbo",
    show_default=True,
    type=click.Choice(["gpt-35-turbo", "gpt-35-turbo-16k", "gpt-4"]),
)
@click.option(
    "--techstack",
    type=str,
    help="it will use in prompt 'develop a project using xxx'",
)
@click.option(
    "--mode",
    default="fc",
    show_default=True,
    type=click.Choice(["fc", "md"]),
    help="how to generate the project using gpt, fc: function call, md: markdown.",
)
def s1(name, desc, path, gpt, techstack, mode):
    """STEP1: CREATE CODE OF A PROJECT"""
    CreateProject(gpt_model=gpt).create_project_code(
        path=path,
        project_name=name,
        project_description=desc,
        techstack=techstack,
        mode=mode,
    )


create.add_command(s1)


@click.command(no_args_is_help=True)
@click.option(
    "--path",
    type=str,
    help="path of the project",
)
@click.option(
    "--gpt",
    default="gpt-35-turbo",
    show_default=True,
    type=click.Choice(["gpt-35-turbo", "gpt-35-turbo-16k", "gpt-4"]),
)
def s2(path, gpt):
    """STEP2: CREATE PROJECT MARKDOWN BASED ON CODE"""
    CreateProject(gpt_model=gpt).create_project_md(path=path)


create.add_command(s2)


@click.command(no_args_is_help=True)
@click.option(
    "--path",
    type=str,
    help="path of the project",
)
def s3(path):
    """STEP3: CREATE PROJECT LAB BASED ON MARKDOWN"""
    CreateProject().create_project_lab(path=path)


create.add_command(s3)


@click.command(no_args_is_help=True)
@click.option(
    "--path",
    type=str,
    help="path of the project",
)
def s4(path):
    """STEP4: CREATE COURSE CONFIG BASED ON LAB"""
    CreateProject().create_course_json(path=path)


create.add_command(s4)


@click.command(no_args_is_help=True)
@click.option(
    "--path",
    type=str,
    help="path of the project",
)
@click.option(
    "--gpt",
    default="gpt-35-turbo",
    show_default=True,
    type=click.Choice(["gpt-35-turbo", "gpt-35-turbo-16k", "gpt-4"]),
)
def s5(path, gpt):
    """STEP4: CREATE COURSE INTRUDUCTION BASED ON LAB"""
    CreateProject(gpt_model=gpt).create_course_intro(path=path)


create.add_command(s5)

if __name__ == "__main__":
    cli()
