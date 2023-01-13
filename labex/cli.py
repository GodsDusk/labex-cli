import click
from .commands.create import Create
from .commands.update import Update
from .commands.check import Check
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

# Check Group
@click.group(context_settings=CONTEXT_SETTINGS)
def check():
    """Check lab or challenge metadata
    """
    pass


cli.add_command(check)


@click.command()
@click.option(
    "--schema", type=str, required=True, help="schema file path", metavar="<path>",
)
@click.option(
    "--instance", type=str, help="index.json file path", metavar="<path>",
)
def json(schema, instance):
    """Check index.json based on schema.json

    - schema: schema.json file path
    - instance: index.json file path
    """
    if instance is None:
        Check().validate_all_json(schema, "./")
    else:
        Check().validate_json(schema, instance)


check.add_command(json)


if __name__ == "__main__":
    cli()
