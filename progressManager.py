from utils import generate_menu, choose_option
from storageManager import find_subject, find_topic
from utils import load_data, write_data
from datetime import datetime
from rich import print
from rich.panel import Panel

SUBJECT_FILE = 'data/subjects.json'
STUDY_HISTORY_FILE = 'data/study_history.json'

def progress_tracking_menu():
    panel_title = "Progress Tracking"
    panel_subtitle = "Welcome to Progress Tracking"
    table_tile = "Progress Tracking Menu"
    rows = ["Start Study Session"]
    back_text = "Back"
    generate_menu(panel_title, panel_subtitle, table_tile, rows, back_text)

def get_info():
    subject_name = input("Enter Subject Name: ").strip().title()
    topic_name = input("Enter Topic Name: ").strip().title()

    data = load_data(SUBJECT_FILE)
    subject = find_subject(data, subject_name)
    if not subject:
        print(f"[red]Subject '{subject_name}' not found![/red]")
        return
    if not find_topic(subject, topic_name):
        print(f"[red]Topic '{topic_name}' not found under subject '{subject_name}'![/red]")
        return
    return subject_name, topic_name

def study_data(subject, topic, date, start, end, duration_minutes):
    data = load_data(STUDY_HISTORY_FILE)
    study_detail = {"subject":subject, "topic": topic, "date":date, "start": start,
                    "end": end, "duration_minutes": duration_minutes}
    data['sessions'].append(study_detail)
    write_data(STUDY_HISTORY_FILE, data)

def start_study_session():
    info = get_info()
    if not info:
        return
    subject_name, topic_name = info
    start_time = datetime.now()
    print("[green]Study session started.[/green]")
    while input("Press Enter when you finish studying.") != "":
        print("[red]Please press only Enter.[/red]")
    end_time = datetime.now()
    duration = end_time - start_time
    duration_minutes = round(duration.total_seconds() / 60)
    if duration_minutes == 0:
        print("[yellow]Study session was too short and was not saved.[/yellow]")
        return
    date = start_time.strftime("%Y-%m-%d")
    start = start_time.strftime("%H:%M:%S")
    end = end_time.strftime("%H:%M:%S")
    study_data(subject_name, topic_name, date, start, end, duration_minutes)
    session_summary = f'''STUDY SESSION COMPLETED

Subject : {subject_name}
Topic   : {topic_name}

Start   : {start}
End     : {end}

Duration: {duration_minutes} minutes

Session saved successfully.
'''
    print((Panel(session_summary, title="Session Summary", style="bold green")))

def progress_tracking():
    progress_tracking_menu()
    while True:
        sub_option2 = choose_option(2)
        if sub_option2 == 0:
            break
        elif sub_option2 == 1:
            start_study_session()
        



