import click
from kakeibox_cli.commands.expenses.get import get_by_uuid
from kakeibox_cli.commands.expenses.new import new
from kakeibox_cli.commands.expenses.delete import delete
from kakeibox_cli.commands.expenses.update import update
from kakeibox_cli.commands.expenses.total_period import total_period


@click.group()
def expenses():
    pass


expenses.add_command(get_by_uuid)
expenses.add_command(new)
expenses.add_command(delete)
expenses.add_command(update)
expenses.add_command(total_period)
