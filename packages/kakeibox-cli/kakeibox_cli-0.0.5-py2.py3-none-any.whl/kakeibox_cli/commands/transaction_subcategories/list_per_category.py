import click
from kakeibox_controllers.controllers.transaction_subcategory\
    .list_per_category import TransactionSubcategoryListPerCategory


@click.command()
@click.argument('transaction_category_code')
def list_per_category(transaction_category_code):
    action = TransactionSubcategoryListPerCategory()
    response = action.execute(transaction_category_code)
    click.echo(response)
