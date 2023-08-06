import click
from kakeibox_controllers.controllers.expense.update \
    import ExpenseUpdate


@click.command()
@click.argument('expense_uuid')
@click.argument('expense_data')
def update(expense_uuid, expense_data):
    action = ExpenseUpdate()
    response = action.execute(expense_uuid, expense_data)
    click.echo(response)
