import click
from kakeibox_cli.commands.incomes.get import get_by_uuid
from kakeibox_cli.commands.incomes.new import new
from kakeibox_cli.commands.incomes.delete import delete
from kakeibox_cli.commands.incomes.update import update
from kakeibox_cli.commands.incomes.total_period import total_period


@click.group()
def incomes():
    pass


incomes.add_command(get_by_uuid)
incomes.add_command(new)
incomes.add_command(delete)
incomes.add_command(update)
incomes.add_command(total_period)
