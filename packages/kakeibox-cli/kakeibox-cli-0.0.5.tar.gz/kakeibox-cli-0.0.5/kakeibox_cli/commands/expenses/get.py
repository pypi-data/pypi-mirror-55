import click
from kakeibox_controllers.controllers.expense.get \
    import TransactionExpenseGet


@click.command()
@click.argument('expense_uuid')
def get_by_uuid(expense_uuid):
    action = TransactionExpenseGet()
    response = action.execute(expense_uuid)
    click.echo(response)
