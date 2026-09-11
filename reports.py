from utils import generate_menu, choose_option
from storageManager import (
    get_study_report_data,
    get_quiz_report_data
)
from rich.table import Table
from rich.panel import Panel
from rich import print


def progress_tracking_menu():
    panel_title = "Reports"
    panel_subtitle = "Get your Reports"
    table_tile = "Reports Menu"
    rows = ["Study Report", "Quiz Report", "Overall Summary"]
    back_text = "Back"
    generate_menu(panel_title, panel_subtitle, table_tile, rows, back_text)

def study_statistics():
    sessions = get_study_report_data()

    if not sessions:
        return None

    study_sessions = len(sessions)

    study_time = 0
    subject_count = {}
    topic_count = {}

    for session in sessions:
        study_time += session["duration_minutes"]

        subject = session["subject_name"]
        topic = session["topic_name"]

        subject_count[subject] = subject_count.get(subject, 0) + 1
        topic_count[topic] = topic_count.get(topic, 0) + 1

    return {
        "study_sessions": study_sessions,
        "study_time": study_time,
        "avg_study_duration": round(
            study_time / study_sessions,
            2
        ),
        "most_subject": max(
            subject_count,
            key=subject_count.get
        ),
        "most_topic": max(
            topic_count,
            key=topic_count.get
        )
    }

def quiz_statistics():
    quizzes = get_quiz_report_data()

    if not quizzes:
        return None

    total_quizzes = len(quizzes)

    accuracy_total = 0
    score_total = 0
    topic_count = {}

    for quiz in quizzes:
        accuracy_total += float(quiz["accuracy"])
        score_total += quiz["score"]

        topic = quiz["topic_name"]
        topic_count[topic] = topic_count.get(topic, 0) + 1

    return {
        "total_quizzes": total_quizzes,
        "average_accuracy": round(
            accuracy_total / total_quizzes,
            2
        ),
        "average_score": round(
            score_total / total_quizzes,
            2
        ),
        "highest_score": max(
            quiz["score"] for quiz in quizzes
        ),
        "lowest_score": min(
            quiz["score"] for quiz in quizzes
        ),
        "most_topic": max(
            topic_count,
            key=topic_count.get
        )
    }

def study_report():
    stats = study_statistics()

    if not stats:
        print("[red]No study history found.[/red]")
        return
    table = Table(title="Study Report")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    table.add_row("Total Study Sessions", str(stats["study_sessions"]))
    table.add_row("Total Study Time", f'{stats["study_time"]} min')
    table.add_row("Average Study Duration", f'{stats["avg_study_duration"]} min')
    table.add_row("Most Studied Subject", stats["most_subject"])
    table.add_row("Most Studied Topic", stats["most_topic"])

    print(Panel.fit(table, title="Reports", border_style="green"))

def quiz_report():
    stats = quiz_statistics()

    if not stats:
        print("[red]No quiz history found.[/red]")
        return

    table = Table(title="Quiz Report")
    table.add_column("Metric", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    table.add_row("Total Quizzes", str(stats["total_quizzes"]))
    table.add_row("Average Accuracy", f'{stats["average_accuracy"]}%')
    table.add_row("Highest Score", f'{stats["highest_score"]}/5')
    table.add_row("Lowest Score", f'{stats["lowest_score"]}/5')
    table.add_row("Average Score", f'{stats["average_score"]}/5')
    table.add_row("Most Quizzed Topic", stats["most_topic"])

    print(Panel.fit(table, title="Reports", border_style="green"))

def overall_summary():
    study_stats = study_statistics()
    quiz_stats = quiz_statistics()

    if not study_stats and not quiz_stats:
        print("[red]No data available.[/red]")
        return

    summary = f"""OVERALL SUMMARY

Study Sessions      : {study_stats["study_sessions"] if study_stats else 0}

Study Time          : {study_stats["study_time"] if study_stats else 0} min

Quizzes Attempted   : {quiz_stats["total_quizzes"] if quiz_stats else 0}

Average Accuracy    : {quiz_stats["average_accuracy"] if quiz_stats else 0}%

Most Studied Subject: {study_stats["most_subject"] if study_stats else "N/A"}

Most Quizzed Topic  : {quiz_stats["most_topic"] if quiz_stats else "N/A"}

Keep up the good work!
"""

    print(Panel.fit(summary, title="Overall Summary", border_style="green"))

def reports():
    progress_tracking_menu()
    while True:
        sub_option2 = choose_option(3)
        if sub_option2 == 0:
            break
        elif sub_option2 == 1:
            study_report()
        elif sub_option2 == 2:
            quiz_report()
        elif sub_option2 == 3:
            overall_summary()
        