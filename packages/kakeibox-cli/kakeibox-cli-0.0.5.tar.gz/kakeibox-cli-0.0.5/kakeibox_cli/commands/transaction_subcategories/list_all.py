import click
from kakeibox_controllers.controllers.transaction_subcategory.list \
    import TransactionSubcategoryList


@click.command()
def list_all():
    action = TransactionSubcategoryList()
    response = action.execute()
    click.echo(response)
