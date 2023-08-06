import click
from kakeibox_controllers.controllers.transaction_subcategory.delete \
    import TransactionSubcategoryDelete


@click.command()
@click.argument('transaction_category_code')
def delete(transaction_category_code):
    action = TransactionSubcategoryDelete()
    response = action.execute(transaction_category_code)
    click.echo(response)
