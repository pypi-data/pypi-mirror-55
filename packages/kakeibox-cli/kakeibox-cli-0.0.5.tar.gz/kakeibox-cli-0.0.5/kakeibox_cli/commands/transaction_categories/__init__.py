import click
from kakeibox_cli.commands.transaction_categories.list_all import list_all
from kakeibox_cli.commands.transaction_categories.new import new
from kakeibox_cli.commands.transaction_categories.delete import delete
from kakeibox_cli.commands.transaction_categories.update import update
from kakeibox_cli.commands.transaction_categories.get import get_by_code


@click.group()
def transaction_categories():
    pass


transaction_categories.add_command(list_all)
transaction_categories.add_command(get_by_code)
transaction_categories.add_command(new)
transaction_categories.add_command(update)
transaction_categories.add_command(delete)
