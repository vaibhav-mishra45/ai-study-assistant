from rich.console import Console
from rich.align import Align
from rich.table import Table
from rich import print
from rich.panel import Panel
import sys
from studyManager import add_subject, delete_subject, display_subjects  , rename_subject

console = Console()
def main():
    while True:
        main_menu()
        option = choose_option(5)
        if option == 1:
            study_management()
            
        elif option == 2:
            print("[bold green]You selected AI Features.[/bold green]")
        elif option == 3:
            print("[bold green]You selected Progress Tracking.[/bold green]")   
        elif option == 4:
            print("[bold green]You selected Reports.[/bold green]")
        elif option == 5:
            print("[bold green]You selected Search.[/bold green]")
        elif option == 0:
            print("[bold red]Exiting the program. Goodbye![/bold red]")
            sys.exit()
   
        
        

def main_menu():
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


def study_management_menu():
    print((Panel(Align.center("Study Management"), subtitle="Welcome to Study Management Module", style="bold green")))
    table = Table(title="Sub Menu")
    table.add_column("Option", justify="right", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")

    table.add_row("1", "Subject Management")
    table.add_row("2", "Topic Management")
    table.add_row("3", "Notes Management")
    table.add_row("0", "Back")
        
    table = Align.center(table)
    console.print(table)

def subject_management_menu():
    print((Panel(Align.center("Subject Management"), subtitle="Welcome to Subject Management Module", style="bold green")))
    table = Table(title="Sub Menu")
    table.add_column("Option", justify="right", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    table.add_row("1", "Add Subject")
    table.add_row("2", "Delete Subject")
    table.add_row("3", "Display Subjects")
    table.add_row("4", "Rename Subject")
    table.add_row("0", "Back")

    table = Align.center(table)
    console.print(table)

def subject_management():
    subject_management_menu()
    while True:
        sub_option2 = choose_option(4)
        if sub_option2 == 0:
            break
        elif sub_option2 == 1:
            add_subject()
        elif sub_option2 == 2:
            delete_subject()
        elif sub_option2 == 3:
            display_subjects()
        elif sub_option2 == 4:
            rename_subject()

def study_management():
    while True:
        study_management_menu()
        sub_option = choose_option(3)
        if sub_option == 0:
            break
        elif sub_option == 1:
            subject_management()
        elif sub_option == 2:
            print("[bold green]You selected Topic Management.[/bold green]")
        elif sub_option == 3:
            print("[bold green]You selected Notes Management.[/bold green]")
                
if __name__ == "__main__":
    main()