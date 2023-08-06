import click
from kakeibox_controllers.controllers.transaction.list import TransactionList


@click.command()
@click.argument('filters')
def list_all(filters):
    action = TransactionList()
    response = action.execute(filters)
    click.echo(response)
