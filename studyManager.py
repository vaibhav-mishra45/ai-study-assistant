from storageManager import save_subject, del_subject, load_data, rename, print_subject
from storageManager import save_topic, print_topics, delete_topic, rename_topic
from storageManager import add_edit_note, delete_note, display_note

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
    note_content = input("Enter the note content: ").strip()
    add_edit_note(subject_name, topic_name, note_content)

def delete_note_():
    subject_name = input("Enter the subject name to delete a note from: ").capitalize().strip()
    topic_name = input("Enter the topic name: ").capitalize().strip()
    delete_note(subject_name, topic_name)

def display_note_():
    subject_name = input("Enter the subject name to display note from: ").capitalize().strip()
    topic_name = input("Enter the topic name: ").capitalize().strip()
    display_note(subject_name, topic_name)

def edit_note_():
    subject_name = input("Enter the subject name to edit a note in: ").capitalize().strip()
    topic_name = input("Enter the topic name: ").capitalize().strip()
    new_note_content = input("Enter the new note content: ").strip()
    add_edit_note(subject_name, topic_name, new_note_content)