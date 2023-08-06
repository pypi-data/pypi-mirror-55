import click
from kakeibox_controllers.controllers.transaction_category.update \
    import TransactionCategoryUpdate


@click.command()
@click.argument('transaction_category_code')
@click.argument('transaction_category_data')
def update(transaction_category_code, transaction_category_data):
    action = TransactionCategoryUpdate()
    response = action.execute(transaction_category_code,
                              transaction_category_data)
    click.echo(response)
