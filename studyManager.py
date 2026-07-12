from storageManager import save_subject, del_subject, load_data, rename, print_subject
from storageManager import save_topic, print_topics, delete_topic, rename_topic
from storageManager import add_edit_note, delete_note, display_note
from utils import generate_menu, choose_option

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
    back_text = "Back"
    rows = ["Add Topic","Delete Topic","Display Topics","Rename Topic"]
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

def add_subject():
    name = input("Enter the subject name: ").capitalize().strip()
    save_subject(name)

def delete_subject():
    name = input("Enter the subject name to delete: ").capitalize().strip()
    del_subject(name)

def display_subjects():
    data = load_data()
    print_subject(data)

def rename_subject():
    old_name = input("Enter the subject name to rename: ").capitalize().strip()
    new_name = input("Enter the new subject name: ").capitalize().strip()
    rename(old_name, new_name)

def add_topic():
    subject_name = input("Enter the subject name to add a topic to: ").capitalize().strip()
    topic_name = input("Enter the topic name: ").capitalize().strip()
    save_topic(subject_name, topic_name)

def del_topic():
    subject_name = input("Enter the subject name to delete a topic from: ").capitalize().strip()
    topic_name = input("Enter the topic name to delete: ").capitalize().strip()
    delete_topic(subject_name, topic_name)

def rename_t():
    subject_name = input("Enter the subject name to rename a topic in: ").capitalize().strip()
    old_topic_name = input("Enter the current topic name: ").capitalize().strip()
    new_topic_name = input("Enter the new topic name: ").capitalize().strip()
    rename_topic(subject_name, old_topic_name, new_topic_name)

def display_topics():
    subject_name = input("Enter the subject name to display topics from: ").capitalize().strip()
    print_topics(subject_name)

def add_edit_note_():
    subject_name = input("Enter the subject name to add/edit a note for: ").capitalize().strip()
    topic_name = input("Enter the topic name: ").capitalize().strip()
    print("Enter your note (type END on a new line to finish):")
    lines = []

    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    note_content = "\n".join(lines)
    add_edit_note(subject_name, topic_name, note_content)

def delete_note_():
    subject_name = input("Enter the subject name to delete a note from: ").capitalize().strip()
    topic_name = input("Enter the topic name: ").capitalize().strip()
    delete_note(subject_name, topic_name)

def display_note_():
    subject_name = input("Enter the subject name to display note from: ").capitalize().strip()
    topic_name = input("Enter the topic name: ").capitalize().strip()
    display_note(subject_name, topic_name)
