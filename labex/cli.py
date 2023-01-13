import click
from .commands.create import Create
from .commands.update import Update
from .commands.utils.version import CheckUpdate


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@click.command()
def create():
    """Create a new lab or challenge
    """
    CheckUpdate().check_version()
    Create().init_base()


cli.add_command(create)

# Update Group
@click.group(context_settings=CONTEXT_SETTINGS)
def update():
    """Update lab or challenge metadata
    """
    pass


cli.add_command(update)


@click.command()
def title():
    """Update lab title from md files
    - excute from lab directory
    """
    Update().title("./")


update.add_command(title)


if __name__ == "__main__":
    cli()
