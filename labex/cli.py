import click
from .commands.utils.version import CheckUpdate
from .commands.utils.auth import LabExLogin

from .commands.lab_create import CreateLab
from .commands.lab_unverified import LabForTesting

from .commands.index_check import CheckIndexValidation
from .commands.index_update_title import UpdateIndexTitle
from .commands.index_set_fee_type import SetFeeType
from .commands.index_add_contributors import AddContributors

from .commands.skilltree_export import ExportSkills
from .commands.skilltree_notify import SkillTreeNotify


from .commands.sync_pr_to_feishu import SyncPRToFeishu
from .commands.sync_labs_to_feishu import SyncLabsToFeishu
from .commands.sync_issues_to_feishu import SyncIssuesToFeishu


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
    help="Check for version updates, default is True.",
)
def login(username, password, check):
    """Log in to your LabEx account.

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
def create():
    """CREATE NEW LABS"""
    CheckUpdate().check_version()
    CreateLab().init_base()


lab.add_command(create)


@click.command()
@click.option(
    "--mode",
    type=click.Choice(["createissue", "closehidden"]),
    default="createissue",
    help="Set mode to createissue or closehidden",
)
def unverified(mode):
    """CREATE UNVERIFIED LAB ISSUES"""
    if mode == "createissue":
        LabForTesting().main()
    elif mode == "closehidden":
        LabForTesting().close_hidden_labs()


lab.add_command(unverified)

# =========================
# INDEX JSON COMMANDS GROUP
# =========================


@click.group(context_settings=CONTEXT_SETTINGS)
def idx():
    """INDEX JSON COMMANDS GROUP"""
    pass


cli.add_command(idx)


@click.command()
def title():
    """Update lab title from md files
    - excute from lab directory
    """
    UpdateIndexTitle().title("./")


idx.add_command(title)


@click.command()
@click.option(
    "--path",
    type=str,
    default="./",
    help="Path to index.json files",
    metavar="<path>",
)
@click.option(
    "--type",
    type=click.Choice(["pro", "free"]),
    default="pro",
    help="Set pro or free",
)
def feetype(path, type):
    """Set lab feetype
    - excute from lab directory
    """
    SetFeeType().set(path, type)


idx.add_command(feetype)


@click.command()
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


@click.command()
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
    help="Path to Repo",
    metavar="<path>",
)
def contributors(ghtoken, repo, path):
    """Add Repo Contributors to index.json"""
    AddContributors(ghtoken=ghtoken).add_contributors(path=path, repo=repo)


idx.add_command(contributors)


# =========================
# SKILL TREE COMMANDS GROUP
# =========================


@click.group(context_settings=CONTEXT_SETTINGS)
def skt():
    """SKILL TREE COMMANDS GROUP"""
    pass


cli.add_command(skt)


@click.command()
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

# ===========================
# SYNC SCRIPTS COMMANDS GROUP
# ===========================


@click.group(context_settings=CONTEXT_SETTINGS)
def sync():
    """SYNC SCRIPTS COMMANDS GROUP"""
    pass


cli.add_command(sync)


@click.command()
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
def prtofeishu(appid, appsecret, ghtoken, repo):
    """Sync Repo PR to Feishu"""
    SyncPRToFeishu(app_id=appid, app_secret=appsecret, ghtoken=ghtoken).sync_pr(
        repo_name=repo
    )


sync.add_command(prtofeishu)


@click.command()
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
    help="Skip the labs that have been synced, default is False.",
)
def labtofeishu(appid, appsecret, repo, skip):
    """Sync Repo labs to Feishu"""
    SyncLabsToFeishu(app_id=appid, app_secret=appsecret, repo=repo).sync_labs(skip=skip)


sync.add_command(labtofeishu)


@click.command()
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
def issuetofeishu(appid, appsecret, ghtoken, repo):
    """Sync Repo Issues to Feishu"""
    SyncIssuesToFeishu(app_id=appid, app_secret=appsecret, ghtoken=ghtoken).sync_issues(
        repo_name=repo
    )


sync.add_command(issuetofeishu)

if __name__ == "__main__":
    cli()
