from utils import generate_menu, choose_option, load_data
from storageManager import find_subject
from rich import print
from rich.panel import Panel

SUBJECT_FILE = 'data/subjects.json'

def search_menu():
    panel_title = "Search"
    panel_subtitle = "Welcome to Search Menu"
    table_tile = "Search Menu"
    rows = ["Search Subject", "Search Topic", "Search Notes"]
    back_text = "Back"
    generate_menu(panel_title, panel_subtitle, table_tile, rows, back_text)

def search_subject(subject_name):
    data = load_data(SUBJECT_FILE)
    subject = find_subject(data, subject_name)
    if not subject:
        print("[red]Subject not found.[/red]")
        return
    topics = "\n".join(f"• {topic['name']}" for topic in subject["topics"])
    subject_details = f'''Subject Found

Subject : {subject['name']}

TOPICS
{topics}
    '''

    print(Panel.fit(subject_details, title="Subject Details", border_style="green"))

def search_topic(topic_name):
    data = load_data(SUBJECT_FILE)
    subjects = data.get("subjects", [])

    for subject in subjects:
        topics = subject.get("topics", [])

        for topic in topics:
            if topic["name"].lower() == topic_name.lower():

                note = "Yes" if topic["note"] else "No"

                topic_details = f"""Topic Found

Topic   : {topic["name"]}

Subject : {subject["name"]}

Notes Available : {note}
"""

                print(Panel.fit(topic_details,
                                title="Topic Details",
                                border_style="green"))
                return

    print(f"[red]Topic '{topic_name}' not found.[/red]")

def search_note(keyword):
    data = load_data(SUBJECT_FILE)
    subjects = data.get("subjects", [])
    matches = []
    for subject in subjects:
        topics = subject.get("topics", [])
        for topic in topics:
            note_text = topic.get('note', '') or ''
            if keyword.lower() in note_text.lower():
                matches.append(
                    f"Subject : {subject['name']}\n"
                    f"Topic   : {topic['name']}"
                )

    if not matches:
        print(f"[red]No notes found containing '{keyword}'.[/red]")
        return

    found_details = f'''Search Results
    
{"\n\n".join(matches)}'''

    print(Panel.fit(found_details, title="Note Search Results", border_style="green"))

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