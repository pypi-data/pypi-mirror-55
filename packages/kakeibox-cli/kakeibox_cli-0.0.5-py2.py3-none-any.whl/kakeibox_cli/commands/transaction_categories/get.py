import click
from kakeibox_controllers.controllers.transaction_category.get \
    import TransactionCategoryGet


@click.command()
@click.argument('transaction_category_code')
def get_by_code(transaction_category_code):
    action = TransactionCategoryGet()
    response = action.execute(transaction_category_code)
    click.echo(response)
