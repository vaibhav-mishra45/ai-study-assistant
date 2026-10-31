import sys
from aiManager import choose_ai_feature
from studyManager import study_management
from progressManager import progress_tracking
from reports import reports
from search import search
from storageManager import (
    verify_quiz_integrity,
    get_recent_quizzes,
    get_all_signed_quizzes
)
from utils import choose_option, generate_menu
from rich import print
from rich.table import Table
from rich.align import Align
from rich.console import Console

console = Console()

def main():
    while True:
        main_menu()
        option = choose_option(6)
        if option == 1:
            study_management()
        elif option == 2:
            choose_ai_feature()
        elif option == 3:
            progress_tracking()
        elif option == 4:
            reports()
        elif option == 5:
            search()
        elif option == 6:
            quiz_integrity()
        elif option == 0:
            print("[bold red]Exiting the program. Goodbye![/bold red]")
            sys.exit()
   
def main_menu():
    panel_title="AI Study Assistant"
    panel_subtitle="Your Personal Learning Companion"
    table_title="Main Menu"
    rows=["Study Management", "AI Features", "Progress Tracking", "Reports", "Search", "Quiz Integrity"]
    back_text="Exit"
    generate_menu(panel_title, panel_subtitle, table_title, rows, back_text)

def quiz_integrity():
    while True:
        generate_menu(
            "Quiz Integrity",
            "ECDSA Signature Verification",
            "Integrity Menu",
            ["Verify Recent Quizzes", "List All Tampered Quizzes"],
            "Back"
        )
        option = choose_option(2)
        if option == 0:
            break
        elif option == 1:
            verify_recent_quizzes()
        elif option == 2:
            list_tampered_quizzes()

def verify_recent_quizzes():
    quizzes = get_recent_quizzes(10)

    if not quizzes:
        print("[yellow]No completed quizzes found.[/yellow]")
        _pause()
        return

    table = Table(title="Recent Quiz Integrity")
    table.add_column("Quiz ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Topic ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Score", justify="center", style="cyan", no_wrap=True)
    table.add_column("Accuracy", justify="right", style="cyan", no_wrap=True)
    table.add_column("Completed", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center", no_wrap=True)

    for quiz in quizzes:
        result = verify_quiz_integrity(quiz["id"])
        status = result["status"]
        status_display = _format_status(status)
        score_display = f"{quiz['score']}/{quiz['total_questions']}"
        accuracy_display = f"{quiz['accuracy']}%"
        completed_display = quiz["completed_at"].strftime("%Y-%m-%d %H:%M")

        table.add_row(
            str(quiz["id"]),
            str(quiz["topic_id"]),
            score_display,
            accuracy_display,
            completed_display,
            status_display
        )

    console.print(Align.center(table))
    _pause()

def list_tampered_quizzes():
    quizzes = get_all_signed_quizzes()

    if not quizzes:
        print("[yellow]No signed quizzes found.[/yellow]")
        _pause()
        return

    tampered = []
    for quiz in quizzes:
        result = verify_quiz_integrity(quiz["id"])
        if result["status"] == "tampered":
            tampered.append(quiz)

    if not tampered:
        print("[bold green]No tampered quizzes found. All signed records are intact.[/bold green]")
        _pause()
        return

    table = Table(title="Tampered Quizzes")
    table.add_column("Quiz ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Topic ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Score", justify="center", style="cyan", no_wrap=True)
    table.add_column("Accuracy", justify="right", style="cyan", no_wrap=True)
    table.add_column("Completed", style="cyan", no_wrap=True)
    table.add_column("Status", justify="center", no_wrap=True)

    for quiz in tampered:
        score_display = f"{quiz['score']}/{quiz['total_questions']}"
        accuracy_display = f"{quiz['accuracy']}%"
        completed_display = quiz["completed_at"].strftime("%Y-%m-%d %H:%M")

        table.add_row(
            str(quiz["id"]),
            str(quiz["topic_id"]),
            score_display,
            accuracy_display,
            completed_display,
            "[bold red]TAMPERED ✗[/bold red]"
        )

    console.print(Align.center(table))
    _pause()

def _format_status(status):
    if status == "valid":
        return "[bold green]VALID ✓[/bold green]"
    elif status == "tampered":
        return "[bold red]TAMPERED ✗[/bold red]"
    elif status == "unsigned":
        return "[bold yellow]UNSIGNED[/bold yellow]"
    else:
        return "[dim]UNKNOWN[/dim]"

def _pause():
    while input("Press Enter to continue...") != "":
        print("[red]Please press only Enter.[/red]")

if __name__ == "__main__":
    main()