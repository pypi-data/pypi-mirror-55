import click
from kakeibox_cli.commands.savings.total_period import total_period


@click.group()
def savings():
    pass


savings.add_command(total_period)
