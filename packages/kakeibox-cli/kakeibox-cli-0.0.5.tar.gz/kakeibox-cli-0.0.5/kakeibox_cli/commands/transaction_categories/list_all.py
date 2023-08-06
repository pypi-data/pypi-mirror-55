import click
from kakeibox_controllers.controllers.transaction_category.list \
    import TransactionCategoryList


@click.command()
def list_all():
    action = TransactionCategoryList()
    response = action.execute()
    click.echo(response)
