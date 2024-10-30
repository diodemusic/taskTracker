from datetime import datetime
import json
import os
import commands
import sys

print(""" _____         _   _____             _           
|_   _|___ ___| |_|_   _|___ ___ ___| |_ ___ ___ 
  | | | .'|_ -| '_| | | |  _| .'|  _| '_| -_|  _|
  |_| |__,|___|_,_| |_| |_| |__,|___|_,_|___|_|
-------------------------------------------------\n""")

PATH = "tasks.json"

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

def save_json(tasks: dict) -> None:
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

def delete_task(task_id: int) -> None:
    tasks = load_json()

    tasks["tasks"].pop(task_id - 1)

    save_json(tasks)
    print(f"Task {task_id} deleted.")

def mark_task(action: str, task_id: int) -> None:
    tasks = load_json()

    for task in tasks["tasks"]:
        if task_id == task["task_id"]:
            if action == "mark-todo":
                task["status"] = "todo"
            elif action == "mark-in-progress":
                task["status"] = "in-progress"
            elif action == "mark-done":
                task["status"] = "done"

            task["updated_at"] = datetime.now().isoformat()

    save_json(tasks)
    print(f"Task {task_id} status updated to {action[5:]}")

def list_tasks(action: str) -> None:
    tasks = load_json()["tasks"]

    print("")
    if action == "":
        for task in tasks:
            for k, v in task.items():
                print(f"{k}: {v}")
            print("")
    else:
        for task in tasks:
            if task["status"] == action:
                for k, v in task.items():
                    print(f"{k}: {v}")
                print("")

if __name__ == "__main__":
    check_if_json_exists()

    while True:
        command = input("task-cli > ")
        command = command.split(" ")

        if command[0] not in commands.COMMANDS:
            print("Command not recognised.")
            continue

        elif command[0] == "add":
            command_description = " ".join(command).split('"')[1]
            create_task(command_description)

        elif command[0] == "update":
            command_description = " ".join(command).split('"')[1]
            update_task(int(command[1]), command_description)

        elif command[0] == "delete":
            delete_task(int(command[1]))

        elif command[0] == "mark-todo":
            mark_task(command[0], int(command[1]))
        elif command[0] == "mark-in-progress":
            mark_task(command[0], int(command[1]))
        elif command[0] == "mark-done":
            mark_task(command[0], int(command[1]))

        elif command[0] == "list":
            if len(command) == 1:
                list_tasks("")
            elif command[1] not in commands.LIST_COMMANDS:
                print("Command not recognised.")
                continue
            else:
                list_tasks(command[1])

        elif command[0] == "help":
            for user_command in commands.COMMANDS:
                print(user_command)
            for user_list_command in commands.LIST_COMMANDS:
                print(f"list {user_list_command}")

        elif command[0] == "quit":
            sys.exit()
