import click
from kakeibox_cli.commands.transaction_subcategories.list_all import list_all
from kakeibox_cli.commands.transaction_subcategories.new import new
from kakeibox_cli.commands.transaction_subcategories.update import update
from kakeibox_cli.commands.transaction_subcategories.delete import delete
from kakeibox_cli.commands.transaction_subcategories.list_per_category \
    import list_per_category
from kakeibox_cli.commands.transaction_subcategories.get import get_by_code


@click.group()
def transaction_subcategories():
    pass


transaction_subcategories.add_command(list_all)
transaction_subcategories.add_command(get_by_code)
transaction_subcategories.add_command(list_per_category)
transaction_subcategories.add_command(new)
transaction_subcategories.add_command(update)
transaction_subcategories.add_command(delete)
