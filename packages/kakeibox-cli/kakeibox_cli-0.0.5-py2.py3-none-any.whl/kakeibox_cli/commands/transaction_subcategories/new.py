import click
from kakeibox_controllers.controllers.transaction_subcategory.new \
    import TransactionSubcategoryNew


@click.command()
@click.argument('transaction_subcategory_data')
def new(transaction_subcategory_data):
    action = TransactionSubcategoryNew()
    response = action.execute(transaction_subcategory_data)
    click.echo(response)
