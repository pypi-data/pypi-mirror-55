import click
from kakeibox_controllers.controllers.income.update \
    import IncomeUpdate


@click.command()
@click.argument('income_uuid')
@click.argument('income_data')
def update(income_uuid, income_data):
    action = IncomeUpdate()
    response = action.execute(income_uuid, income_data)
    click.echo(response)
