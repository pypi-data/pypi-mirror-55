import click
from kakeibox_controllers.controllers.transaction_subcategory.update \
    import TransactionSubcategoryUpdate


@click.command()
@click.argument('transaction_subcategory_code')
@click.argument('transaction_subcategory_data')
def update(transaction_subcategory_code, transaction_subcategory_data):
    action = TransactionSubcategoryUpdate()
    response = action.execute(transaction_subcategory_code,
                              transaction_subcategory_data)
    click.echo(response)
