from datetime import datetime
import json
import os

print(""" _____         _   _____             _           
|_   _|___ ___| |_|_   _|___ ___ ___| |_ ___ ___ 
  | | | .'|_ -| '_| | | |  _| .'|  _| '_| -_|  _|
  |_| |__,|___|_,_| |_| |_| |__,|___|_,_|___|_|  """)

PATH = "tasks.json"
COMMANDS = [
    "add",
    "update",
    "delete",
    "mark-in-progress",
    "mark-done",
    "list",
]
LIST_COMMANDS = [ #TODO validate this stuff on calling the list command
    "done",
    "todo",
    "in-progress"
]

def check_if_json_exists() -> None:
    if os.path.isfile(PATH) and os.access(PATH, os.R_OK):
        pass
    else:
        with open(PATH, "w") as tasks_json:
            tasks_json.write(json.dumps({"tasks": []}))

def load_json() -> dict:
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
    return tasks

def save_json(tasks) -> None:
    with open("tasks.json", "w") as f:
        # noinspection PyTypeChecker
        json.dump(tasks, f, indent=4)

def create_task(task_description: str) -> None:
    tasks = load_json()

    task_id = len(tasks["tasks"]) + 1
    tasks["tasks"].append({
        "task_id": task_id,
        "description": task_description,
        "status": "todo",
        "created_at": datetime.now().isoformat(),
        "updated_at": None,
    })

    save_json(tasks)
    print(f"Task {task_id} created.")

def update_task(task_id: int, task_description: str) -> None:
    tasks = load_json()

    for task in tasks["tasks"]:
        if task_id == task["task_id"]:
            task["description"] = task_description
            task["updated_at"] = datetime.now().isoformat()

    save_json(tasks)
    print(f"Task {task_id} updated.")

if __name__ == "__main__":
    check_if_json_exists()

    while True:
        command = input("task-cli > ")
        command = command.split(" ")

        if command[0] not in COMMANDS:
            print("Command not recognised.")
            continue

        if command[0] == "add":
            command_description = " ".join(command).split('"')[1]
            create_task(command_description)

        if command[0] == "update":
            command_description = " ".join(command).split('"')[1]
            update_task(int(command[1]), command_description)

        if command[0] == "delete":
            #TODO delete task
            pass
