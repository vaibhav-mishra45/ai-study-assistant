from utils import generate_menu, choose_option
from storageManager import (
    get_subject_by_name,
    get_topics,
    search_topics,
    search_notes
)
from rich import print
from rich.panel import Panel

def search_menu():
    panel_title = "Search"
    panel_subtitle = "Welcome to Search Menu"
    table_tile = "Search Menu"
    rows = ["Search Subject", "Search Topic", "Search Notes"]
    back_text = "Back"
    generate_menu(panel_title, panel_subtitle, table_tile, rows, back_text)

def search_subject(subject_name):
    subject = get_subject_by_name(subject_name)

    if not subject:
        print("[red]Subject not found.[/red]")
        return

    topics = get_topics(subject["id"])

    topic_names = "\n".join(
        f"• {topic['name']}"
        for topic in topics
    )

    subject_details = f"""Subject Found

Subject : {subject['name']}

TOPICS
{topic_names}
"""

    print(
        Panel.fit(
            subject_details,
            title="Subject Details",
            border_style="green"
        )
    )

def search_topic(topic_name):
    matches = search_topics(topic_name)

    if not matches:
        print(f"[red]Topic '{topic_name}' not found.[/red]")
        return

    match = matches[0]

    topic_details = f"""Topic Found

Topic   : {match["topic_name"]}

Subject : {match["subject_name"]}

Notes Available : {match["notes_available"]}
"""

    print(
        Panel.fit(
            topic_details,
            title="Topic Details",
            border_style="green"
        )
    )

def search_note(keyword):
    matches = search_notes(keyword)

    if not matches:
        print(
            f"[red]No notes found containing '{keyword}'.[/red]"
        )
        return

    found_details = f"""Search Results

{"\n\n".join(
    f"Subject : {match['subject_name']}\n"
    f"Topic   : {match['topic_name']}"
    for match in matches
)}
"""

    print(
        Panel.fit(
            found_details,
            title="Note Search Results",
            border_style="green"
        )
    )

def search():
    search_menu()
    while True:
        sub_option2 = choose_option(3)
        if sub_option2 == 0:
            break
        elif sub_option2 == 1:
            subject_name = input("Enter Subject Name: ").strip()
            if subject_name:
                search_subject(subject_name)
            else:
                print("[red] Invalid Input. [/red]")
        elif sub_option2 == 2:
            topic_name = input("Enter Topic Name: ").strip()
            if topic_name:
                search_topic(topic_name)
            else:
                print("[red] Invalid Input. [/red]")
        elif sub_option2 == 3:
            keyword = input("Enter Keyword: ").strip()
            if keyword:
                search_note(keyword)
            else:
                print("[red] Invalid Input. [/red]")