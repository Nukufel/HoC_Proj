from langchain.tools import tool
import memory.database as db

@tool
def add_task_tool(text: str) -> str:
    db.add_task(text)
    return "Task added."

@tool
def list_tasks_tool() -> str:
    tasks = db.get_tasks()
    return "\n".join(tasks) if tasks else "No tasks."

@tool
def set_task_done_tool(id: int) -> str:
    db.update_task(id)
    return "Task is done."

@tool
def add_grocery_tool(text: str) -> str:
    db.add_grocery(text)
    return "Task added."

@tool
def list_groceries_tool() -> str:
    tasks = db.get_groceries()
    return "\n".join(tasks) if tasks else "No tasks."

@tool
def set_grocery_done_tool(id: int) -> str:
    db.update_grocery(id)
    return "Grocary is done."

@tool
def add_note_tool(text: str) -> str:
    db.add_note(text)
    return "Task added."

@tool
def list_notes_tool() -> str:
    tasks = db.get_notes()
    return "\n".join(tasks) if tasks else "No tasks."

@tool
def set_note_done_tool(id: int) -> str:
    db.update_notes(id)
    return "Note is done."

@tool
def delete_done_tool() -> str:
    db.delete_done()
    return "Deleted done elements."