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
    tasks = db.get_tasks()
    return "\n".join(tasks) if tasks else "No tasks."

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
    tasks = db.get_groceries()
    return "\n".join(tasks) if tasks else "No groceries."

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
    tasks = db.get_notes()
    return "\n".join(tasks) if tasks else "No tasks."

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
    """ Use this tool whenever the user asks about:
        - schedule
        - timetable
        - meetings
        - lectures
        - events
        - what happens on a specific day
        - what is planned

        ALWAYS use this tool instead of answering from memory."""

    docs = create_or_get_vector_store().similarity_search(question, k=4)

    context = "\n\n".join(d.page_content for d in docs)

    return f"Relevant schedule information:\n{context}"