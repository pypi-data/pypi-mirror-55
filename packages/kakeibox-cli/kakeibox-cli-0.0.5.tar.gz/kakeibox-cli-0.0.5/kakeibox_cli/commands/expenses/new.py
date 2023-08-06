import click
from kakeibox_controllers.controllers.expense.new \
    import ExpenseNew


@click.command()
@click.argument('expense_data')
def new(expense_data):
    action = ExpenseNew()
    response = action.execute(expense_data)
    click.echo(response)
