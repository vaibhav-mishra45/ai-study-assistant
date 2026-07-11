import json
from rich import print
from rich.table import Table
from utils import load_data, write_data

SUBJECT_FILE = 'data/subjects.json'





def find_subject(data, name):
    for subject in data.get('subjects', []):
        if subject.get('name').lower() == name.lower():
            return subject
    return None


def find_topic(subject, name):
    for topic in subject.get('topics', []):
        if topic.get('name').lower() == name.lower():
            return topic
    return None


def print_subject(data):
    table = Table(title="Subjects List", show_header=False)

    subjects = sorted(data.get('subjects', []), key=lambda s: s.get('name', '').lower())
    if not subjects:
        print("[red]No subjects found![/red]")
        return
    for subject in subjects:
        table.add_row(subject['name'])
    print(table)


def save_subject(name):
    data = load_data(SUBJECT_FILE)
    if find_subject(data, name):
        print("[red]Subject already exist![/red]")
        return
    new_subject = {"name": name, "topics": []}
    data['subjects'].append(new_subject)
    write_data(SUBJECT_FILE, data)


def del_subject(name):
    data = load_data(SUBJECT_FILE)
    if not find_subject(data, name):
        print(f"[red]Subject '{name}' not found![/red]")
        return
    data['subjects'] = [subject for subject in data.get('subjects', []) if subject.get('name').lower() != name.lower()]
    write_data(SUBJECT_FILE, data)


def rename(old_name, new_name):
    data = load_data(SUBJECT_FILE)
    subjects = data.get('subjects', [])
    # check old exists
    subject = find_subject(data, old_name)
    if not subject:
        print(f"[red]Subject '{old_name}' not found![/red]")
        return
    # check new doesn't already exist
    if any(s.get('name').lower() == new_name.lower() for s in subjects):
        print(f"[red]Subject '{new_name}' already exists![/red]")
        return
    # perform rename
    subject['name'] = new_name
    write_data(SUBJECT_FILE, data)
    print(f"[green]Renamed '{old_name}' to '{new_name}'[/green]")


def print_topics(subject_name):
    data = load_data(SUBJECT_FILE)
    subject = find_subject(data, subject_name)
    if not subject:
        print(f"[red]Subject '{subject_name}' not found![/red]")
        return
    topics = subject.get('topics', [])
    if not topics:
        print(f"[red]No topics found under subject '{subject_name}'[/red]")
        return
    table = Table(title=f"Topics under '{subject_name}'", show_header=False)
    for topic in topics:
        table.add_row(topic['name'])
    print(table)
    return


def save_topic(subject_name, topic_name):
    data = load_data(SUBJECT_FILE)
    subject = find_subject(data, subject_name)
    if not subject:
        print(f"[red]Subject '{subject_name}' not found![/red]")
        return
    if find_topic(subject, topic_name):
        print(f"[red]Topic '{topic_name}' already exists under subject '{subject_name}'![/red]")
        return
    new_topic = {"name": topic_name, "note": ""}
    subject['topics'].append(new_topic)
    write_data(SUBJECT_FILE, data)
    print(f"[green]Added topic '{topic_name}' under subject '{subject_name}'[/green]")
    return


def delete_topic(subject_name, topic_name):
    data = load_data(SUBJECT_FILE)
    subject = find_subject(data, subject_name)
    if not subject:
        print(f"[red]Subject '{subject_name}' not found![/red]")
        return
    if not find_topic(subject, topic_name):
        print(f"[red]Topic '{topic_name}' not found under subject '{subject_name}'![/red]")
        return
    subject['topics'] = [t for t in subject['topics'] if t.get('name').lower() != topic_name.lower()]
    write_data(SUBJECT_FILE, data)
    print(f"[green]Deleted topic '{topic_name}' from subject '{subject_name}'[/green]")
    return


def rename_topic(subject_name, old_topic_name, new_topic_name):
    data = load_data(SUBJECT_FILE)
    subject = find_subject(data, subject_name)
    if not subject:
        print(f"[red]Subject '{subject_name}' not found![/red]")
        return
    old_topic = find_topic(subject, old_topic_name)
    if not old_topic:
        print(f"[red]Topic '{old_topic_name}' not found under subject '{subject_name}'![/red]")
        return
    if find_topic(subject, new_topic_name):
        print(f"[red]Topic '{new_topic_name}' already exists under subject '{subject_name}'![/red]")
        return
    old_topic['name'] = new_topic_name
    write_data(SUBJECT_FILE, data)
    print(f"[green]Renamed topic '{old_topic_name}' to '{new_topic_name}' under subject '{subject_name}'[/green]")
    return


def add_edit_note(subject_name, topic_name, note_content):
    data = load_data(SUBJECT_FILE)
    subject = find_subject(data, subject_name)
    if not subject:
        print(f"[red]Subject '{subject_name}' not found![/red]")
        return
    topic = find_topic(subject, topic_name)
    if topic:
        topic['note'] = note_content
        write_data(SUBJECT_FILE, data)
        print(f"[green]Added/Updated note for topic '{topic_name}' under subject '{subject_name}'[/green]")
        return
    print(f"[red]Topic '{topic_name}' not found under subject '{subject_name}'![/red]")
    return


def delete_note(subject_name, topic_name):
    data = load_data(SUBJECT_FILE)
    subject = find_subject(data, subject_name)
    if not subject:
        print(f"[red]Subject '{subject_name}' not found![/red]")
        return
    topic = find_topic(subject, topic_name)
    if topic:
        topic['note'] = ""
        write_data(SUBJECT_FILE, data)
        print(f"[green]Deleted note for topic '{topic_name}' under subject '{subject_name}'[/green]")
        return
    print(f"[red]Topic '{topic_name}' not found under subject '{subject_name}'![/red]")
    return


def display_note(subject_name, topic_name):
    data = load_data(SUBJECT_FILE)
    subject = find_subject(data, subject_name)
    if not subject:
        print(f"[red]Subject '{subject_name}' not found![/red]")
        return
    topic = find_topic(subject, topic_name)
    if topic:
        note_content = topic.get('note', "")
        if note_content:
            print(f"[bold green]Note for topic '{topic_name}' under subject '{subject_name}':[/bold green]\n{note_content}")
        else:
            print(f"[red]No note found for topic '{topic_name}' under subject '{subject_name}'[/red]")
        return
    print(f"[red]Topic '{topic_name}' not found under subject '{subject_name}'![/red]")


