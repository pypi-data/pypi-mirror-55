import click
from kakeibox_controllers.controllers.transaction_subcategory.get \
    import TransactionSubcategoryGet


@click.command()
@click.argument('transaction_subcategory_code')
def get_by_code(transaction_subcategory_code, ):
    action = TransactionSubcategoryGet()
    response = action.execute(transaction_subcategory_code)
    click.echo(response)
