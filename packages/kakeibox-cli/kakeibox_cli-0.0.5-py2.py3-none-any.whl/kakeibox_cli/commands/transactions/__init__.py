import click
from kakeibox_cli.commands.transactions.list_all import list_all


@click.group()
def transactions():
    pass


transactions.add_command(list_all)
