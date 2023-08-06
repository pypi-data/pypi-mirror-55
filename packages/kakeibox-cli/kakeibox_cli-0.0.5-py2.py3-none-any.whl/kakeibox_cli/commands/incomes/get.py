import click
from kakeibox_controllers.controllers.income.get \
    import TransactionIncomeGet


@click.command()
@click.argument('income_uuid')
def get_by_uuid(income_uuid):
    action = TransactionIncomeGet()
    response = action.execute(income_uuid)
    click.echo(response)
