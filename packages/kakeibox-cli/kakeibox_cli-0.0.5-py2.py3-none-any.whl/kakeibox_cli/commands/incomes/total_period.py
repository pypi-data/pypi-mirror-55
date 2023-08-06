import click
from kakeibox_controllers.controllers.income.total import IncomeTotal


@click.command()
@click.argument('filters')
def total_period(filters):
    action = IncomeTotal()
    response = action.execute(filters)
    click.echo(response)
