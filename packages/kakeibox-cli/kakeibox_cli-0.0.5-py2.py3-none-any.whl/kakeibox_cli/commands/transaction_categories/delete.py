import click
from kakeibox_controllers.controllers.transaction_category.delete \
    import TransactionCategoryDelete


@click.command()
@click.argument('transaction_category_code')
def delete(transaction_category_code):
    action = TransactionCategoryDelete()
    response = action.execute(transaction_category_code)
    click.echo(response)
