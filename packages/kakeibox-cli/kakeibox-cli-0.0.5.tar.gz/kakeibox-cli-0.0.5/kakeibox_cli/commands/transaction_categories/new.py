import click
from kakeibox_controllers.controllers.transaction_category.new \
    import TransactionCategoryNew


@click.command()
@click.argument('transaction_category_data')
def new(transaction_category_data):
    action = TransactionCategoryNew()
    response = action.execute(transaction_category_data)
    click.echo(response)
