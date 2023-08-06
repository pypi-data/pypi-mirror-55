import click
from kakeibox_controllers.controllers.income.new \
    import IncomeNew


@click.command()
@click.argument('income_data')
def new(income_data):
    action = IncomeNew()
    response = action.execute(income_data)
    click.echo(response)
