from rich.console import Console
import sys
from aiManager import choose_ai_feature
from studyManager import add_subject, delete_subject, display_subjects, display_topics , rename_subject
from studyManager import add_topic, del_topic, rename_t
from studyManager import add_edit_note_, delete_note_, display_note_
from utils import choose_option
from utils import generate_menu

console = Console()
def main():
    while True:
        main_menu()
        option = choose_option(5)
        if option == 1:
            study_management()
        elif option == 2:
            choose_ai_feature()
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
    panel_title="AI Study Assistant"
    panel_subtitle="Your Personal Learning Companion"
    table_title="Main Menu"
    rows=["Study Management", "AI Features", "Progress Tracking", "Reports", "Search"]
    back_text="Exit"
    generate_menu(panel_title, panel_subtitle, table_title, rows, back_text)

def study_management_menu():
    panel_title="Study Management"
    panel_subtitle="Welcome to Study Management Module"
    table_title="Sub Menu"
    rows=["Subject Management", "Topic Management", "Notes Management"]
    back_text="Back"
    generate_menu(panel_title, panel_subtitle, table_title, rows, back_text)

def subject_management_menu():
    panel_title = "Subject Management"
    panel_subtitle = "Welcome to Subject Management Module"
    table_title = "Sub Menu"
    rows = ["Add Subject", "Delete Subject", "Display Subjects", "Rename Subject"]
    back_text = "Back"
    generate_menu(panel_title, panel_subtitle, table_title, rows, back_text)

def topic_management_menu():
    panel_title = "Topic Management"
    panel_subtitle = "Welcome to Topic Management Module"
    table_title = "Sub Menu"
    rows = ["Add/Edit Note", "Delete Note", "View Note"]
    back_text = "Back"
    generate_menu(panel_title, panel_subtitle, table_title, rows, back_text)

def notes_management_menu():
    panel_title = "Notes Management"
    panel_subtitle = "Welcome to Notes Management Module"
    table_title = "Sub Menu"
    rows = ["Add/Edit Note", "Delete Note", "View Note"]
    back_text = "Back"
    generate_menu(panel_title, panel_subtitle, table_title, rows, back_text)




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
            topic_management()
        elif sub_option == 3:
            notes_management()

def topic_management():
    topic_management_menu()
    while True:
        sub_option2 = choose_option(4)
        if sub_option2 == 0:
            break
        elif sub_option2 == 1:
            add_topic()
        elif sub_option2 == 2:
            del_topic()
        elif sub_option2 == 3:
            display_topics()
        elif sub_option2 == 4:
            rename_t()

def notes_management():
    notes_management_menu()
    while True:
        sub_option2 = choose_option(3)
        if sub_option2 == 0:
            break
        elif sub_option2 == 1:
            add_edit_note_()
        elif sub_option2 == 2:
            delete_note_()
        elif sub_option2 == 3:
            display_note_()

if __name__ == "__main__":
    main()