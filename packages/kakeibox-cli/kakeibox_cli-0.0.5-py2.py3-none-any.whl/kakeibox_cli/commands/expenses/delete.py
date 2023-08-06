import click
from kakeibox_controllers.controllers.expense.delete \
    import ExpenseDelete


@click.command()
@click.argument('expense_uuid')
def delete(expense_uuid):
    action = ExpenseDelete()
    response = action.execute(expense_uuid)
    click.echo(response)
