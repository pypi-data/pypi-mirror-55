import click
from kakeibox_controllers.controllers.income.delete \
    import IncomeDelete


@click.command()
@click.argument('income_uuid')
def delete(income_uuid):
    action = IncomeDelete()
    response = action.execute(income_uuid)
    click.echo(response)
