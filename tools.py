from langchain.tools import tool
import memory.database as db
from rag import create_or_get_vector_store

@tool
def add_task_tool(text: str) -> str:
    """Add a new task to the user's task list."""
    db.add_task(text)
    return "Task added."

@tool
def list_tasks_tool() -> str:
    """Get all tasks from the user's task list."""
    rows = db.get_tasks()
    text = ""
    for row in rows:
        text += f"{row[1]}{add_note(row[2])}\n"
    return text if rows else "No tasks."

@tool
def set_task_done_tool(id: int) -> str:
    """Set the stat of a specific task to 'done'."""
    db.update_task(id)
    return "Task is done."

@tool
def remove_task_tool(id: int) -> str:
    """Remove the task with the given id."""
    db.delete_task(id)
    return "Task deleted."

@tool
def add_grocery_tool(text: str) -> str:
    """Add a new grocery item to the user's groceries list."""
    db.add_grocery(text)
    return "Grocery added."

@tool
def list_groceries_tool() -> str:
    """Get all groceries from the user's grocery list."""
    rows = db.get_groceries()
    text = ""
    for row in rows:
        text += f"{row[2]} {row[1]}{add_note(row[3])}\n"
    return text if rows else "No groceries."

@tool
def set_grocery_done_tool(id: int) -> str:
    """Set the stat of a specific grocery item to 'done'."""
    db.update_grocery(id)
    return "Grocary is done."

@tool
def remove_grocery_tool(id: int) -> str:
    """Remove the grocery with the given id."""
    db.delete_grocery(id)
    return "Grocery deleted."

@tool
def add_note_tool(text: str) -> str:
    """Add a new note to the user's notes."""
    db.add_note(text)
    return "Task added."

@tool
def list_notes_tool() -> str:
    """Get all the notes from the user’s notes."""
    rows = db.get_notes()
    text = ""
    for row in rows:
        text += f"{row[1]}\n"
    return text if rows else "No notes."

@tool
def set_note_done_tool(id: int) -> str:
    """Set the stat of a specific note to 'done'."""
    db.update_notes(id)
    return "Note is done."

@tool
def remove_note_tool(id: int) -> str:
    """Remove the note with the given id."""
    db.delete_grocery(id)
    return "Note deleted."

@tool
def delete_done_tool() -> str:
    """Removes all items that have been done."""
    db.delete_done()
    return "Deleted done elements."

#TODO make rag  for docs and schedule image or calender api
@tool
def search_schedule_tool(question: str) -> str:
    """Use this tool if the user asks about documents""" #TODO better description

    docs = create_or_get_vector_store().similarity_search(question, k=4)

    context = "\n\n".join(d.page_content for d in docs)

    return f"Relevant schedule information:\n{context}"

def add_note(note: str) -> str:
   if note == "":
       return ""
   return f"; Note: {note}"