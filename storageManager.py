import json
from rich import print
from rich.table import Table

subject_file = 'data/subjects.json'
data = {
    "subjects": []
    }

def load_subjects():
    with open(subject_file, 'r') as f:
        data = json.load(f)
        return data
        
def print_data(data):
    if data is None:
        print("[red]No subjects found!![/red]")
    table = Table(title="Subjects List", show_header=False)

    subjects = sorted(data.get('subjects', []), key=lambda s: s.get('name', '').lower())
    for subject in subjects:
        table.add_row(subject['name'])
    print(table)

def save_subject(name):
    with open(subject_file, 'r+') as f:
        data = json.load(f)
        for subject in data["subjects"]:
            if name.lower() == subject["name"].lower():
                print("[red]Subject already exist![/red]")
                return
        new_subject = {"name": name}
        data['subjects'].append(new_subject)
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)

def del_subject(name):
    with open(subject_file, 'r+') as f:
        data = json.load(f)
        if not any(subject.get('name').lower() == name.lower() for subject in data.get('subjects', [])):
            print(f"[red]Subject '{name}' not found![/red]")
            return
        data['subjects'] = [subject for subject in data.get('subjects', []) if subject.get('name').lower() != name.lower()]
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)

def rename(old_name, new_name):
    with open(subject_file, 'r+') as f:
        data = json.load(f)
        subjects = data.get('subjects', [])
        # check old exists
        if not any(s.get('name').lower() == old_name.lower() for s in subjects):
            print(f"[red]Subject '{old_name}' not found![/red]")
            return
        # check new doesn't already exist
        if any(s.get('name').lower() == new_name.lower() for s in subjects):
            print(f"[red]Subject '{new_name}' already exists![/red]")
            return
        # perform rename
        for s in subjects:
            if s.get('name').lower() == old_name.lower():
                s['name'] = new_name
                break
        data['subjects'] = subjects
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)
        print(f"[green]Renamed '{old_name}' to '{new_name}'[/green]")


