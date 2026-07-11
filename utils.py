from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.console import Console
from rich import print
import json

console = Console()

def generate_menu(panel_title, panel_subtitle, table_title, rows, back_text):
    print((Panel(Align.center(panel_title), subtitle=panel_subtitle, style="bold green")))
    table = Table(title=table_title)
    table.add_column("Option", justify="right", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    for i, row in enumerate(rows, start=1):
        table.add_row(str(i), row)
    table.add_row("0", back_text)
    table = Align.center(table)
    console.print(table)

def choose_option(n):
    while True:
        try:
            option = int(input(f"Enter your choice (0-{n}): "))
            if option in range(n + 1):
                return option
            else:
                print(f"[red]Invalid choice. Please enter a number between 0 and {n}.[/red]")
        except ValueError:
            print(f"[red]Invalid input. Please enter a number between 0 and {n}.[/red]")

def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        return data


def write_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)