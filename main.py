import sys
from aiManager import choose_ai_feature
from studyManager import study_management
from progressManager import progress_tracking
from utils import choose_option, generate_menu
from rich import print

def main():
    while True:
        main_menu()
        option = choose_option(5)
        if option == 1:
            study_management()
        elif option == 2:
            choose_ai_feature()
        elif option == 3:
            progress_tracking()
        elif option == 4:
            print("[bold green]You selected Reports.[/bold green]")
        elif option == 5:
            print("[bold green]You selected Search.[/bold green]")
        elif option == 0:
            print("[bold red]Exiting the program. Goodbye![/bold red]")
            sys.exit()
   
def main_menu():
    panel_title="AI Study Assistant"
    panel_subtitle="Your Personal Learning Companion"
    table_title="Main Menu"
    rows=["Study Management", "AI Features", "Progress Tracking", "Reports", "Search"]
    back_text="Exit"
    generate_menu(panel_title, panel_subtitle, table_title, rows, back_text)

if __name__ == "__main__":
    main()