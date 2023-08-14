import click
from .commands.utils.version import CheckUpdate


from .commands.lab_create import CreateLab
from .commands.index_check import CheckIndexValidation
from .commands.index_update import UpdateIndexJSON
from .commands.skilltree_export import ExportSkills
from .commands.skilltree_notify import SkillTreeNotify


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """LabEx Command Line Interface"""
    pass


# =========================
# LAB COMMANDS GROUP
# =========================


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
    UpdateIndexJSON().title("./")


idx.add_command(title)


@click.command()
@click.option(
    "--schema",
    type=str,
    default="schema.json",
    help="schema file path",
    metavar="<path>",
)
@click.option(
    "--instance",
    type=str,
    help="index.json file path",
    metavar="<path>",
)
def check(schema, instance):
    """Check index.json based on schema.json

    - schema: schema.json file path
    - instance: index.json file path
    """
    if instance is None:
        CheckIndexValidation().validate_all_json(schema, "./")
    else:
        CheckIndexValidation().validate_json(schema, instance)


idx.add_command(check)

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
    help="Feishu App ID",
)
@click.option(
    "--appsecret",
    type=str,
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


if __name__ == "__main__":
    cli()
