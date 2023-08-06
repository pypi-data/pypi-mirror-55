import click
from kakeibox_controllers.controllers.expense.total import ExpenseTotal


@click.command()
@click.argument('filters')
def total_period(filters):
    action = ExpenseTotal()
    response = action.execute(filters)
    click.echo(response)
