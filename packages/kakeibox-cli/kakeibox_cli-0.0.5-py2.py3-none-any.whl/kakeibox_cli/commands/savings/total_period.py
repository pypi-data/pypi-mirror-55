import click
from kakeibox_controllers.controllers.saving.total import SavingTotal


@click.command()
@click.argument('filters')
def total_period(filters):
    action = SavingTotal()
    response = action.execute(filters)
    click.echo(response)
