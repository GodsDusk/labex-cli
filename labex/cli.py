import os
import click
from rich import markdown, print
from .commands.create import Create


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@click.command()
def create():
    """Create a new lab or challenge
    """
    Create().init_base()


cli.add_command(create)


if __name__ == "__main__":
    cli()
