from storageManager import save_subject, del_subject, load_subjects, rename, print_data

def add_subject():
    name = input("Enter the subject name: ").capitalize().strip()
    save_subject(name)

def delete_subject():
    name = input("Enter the subject name to delete: ").capitalize().strip()
    del_subject(name)

def display_subjects():
    data = load_subjects()
    print_data(data)


def rename_subject():
    old_name = input("Enter the subject name to rename: ").capitalize().strip()
    new_name = input("Enter the new subject name: ").capitalize().strip()
    rename(old_name, new_name)