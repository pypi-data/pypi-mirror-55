#!/home/jon/.virtualenvs/kakeibox-cli/bin/python
import click
from kakeibox_cli.commands.transaction_categories import transaction_categories
from kakeibox_cli.commands.transaction_subcategories import \
    transaction_subcategories
from kakeibox_cli.commands.transactions import transactions
from kakeibox_cli.commands.savings import savings
from kakeibox_cli.commands.incomes import incomes
from kakeibox_cli.commands.expenses import expenses


@click.group()
def kakeibox():
    pass


kakeibox.add_command(transaction_categories)
kakeibox.add_command(transaction_subcategories)
kakeibox.add_command(transactions)
kakeibox.add_command(savings)
kakeibox.add_command(incomes)
kakeibox.add_command(expenses)


if __name__ == "__main__":
    kakeibox()
