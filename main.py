from rich.console import Console
from rich.align import Align
from rich.table import Table
from rich import print
from rich.panel import Panel
import sys
def main():
    menu()
    option = choose_option()
    if option == 1:
        print("[bold green]You selected Study Management.[/bold green]")
    elif option == 2:
        print("[bold green]You selected AI Features.[/bold green]")
    elif option == 3:
        print("[bold green]You selected Progress Tracking.[/bold green]")   
    elif option == 4:
        print("[bold green]You selected Reports.[/bold green]")
    elif option == 5:
        print("[bold green]You selected Search.[/bold green]")
    elif option == 0:
        sys.exit("[bold red]Exiting the program. Goodbye![/bold red]")

def menu():
    console = Console()
    print((Panel(Align.center("AI Study Assistant"), subtitle="Your Personal Learning Companion", style="bold green")))

    table = Table(title="Main Menu")

    table.add_column("Option", justify="right", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")

    table.add_row("1", "Study Management")
    table.add_row("2", "AI Features")
    table.add_row("3", "Progress Tracking")
    table.add_row("4", "Reports")
    table.add_row("5", "Search")
    table.add_row("0", "Exit")

    table = Align.center(table)
    console.print(table)

def choose_option():
    while True:
        try:
            option = int(input("Enter your choice (0-5): "))
            if option in range(6):
                return option
            else:
                print("[red]Invalid choice. Please enter a number between 0 and 5.[/red]")
        except ValueError:
            print("[red]Invalid input. Please enter a number between 0 and 5.[/red]")

if __name__ == "__main__":
    main()