import datetime

from langchain.tools import tool
import memory.database as db
from rag import create_or_get_vector_store


# --- event tools ---
@tool
def add_event_tool(title, start, end, location, description) -> str:
    """
    Add a calendar event using natural language.
    Example:
    'Meeting tomorrow at 10'
    """

    db.add_event(
        title=title,
        start_time=start,
        end_time=end,
        location=location,
        description=description,
    )

    return f"Event added: {title} at {start} to {end}"

@tool
def get_today_events_tool() -> str:
    """Get all events scheduled for today."""
    start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + datetime.timedelta(days=1)
    events = db.get_events_between(start, end)
    return events

@tool
def list_all_events_tool() -> str:
    """List all calendar events."""
    events = db.get_all_events()
    return events

@tool
def search_event_tool(text: str) -> str:
    """Search calendar events by description."""
    events = db.get_event_by_text(text)
    return events

@tool
def delete_event_by_id_tool(id: int) -> str:
    """Delete event using its id."""
    db.delete_event_by_id(id)
    return f"Event {id} deleted."


# --- user tools ---
@tool
def update_user_name_tool(name: str):
    """Update the user's name."""
    db.update_user_name(name)
    return "Name updated"

@tool
def update_user_birthdate_tool(name: str):
    """Update the user's birthdate."""
    db.update_user_name(name)
    return "Name updated"

@tool
def get_user_tool():
    """Get user info."""
    user = db.get_user()
    return user


# --- grocery tools ---
@tool
def add_grocery_tool(text: str) -> str:
    """Add a new grocery item to the user's groceries list."""
    db.add_grocery(text)
    return "Grocery added."

@tool
def list_groceries_tool() -> str:
    """Get all groceries from the user's grocery list."""
    rows = db.get_groceries()
    return rows

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

# --- note tools ---
@tool
def add_note_tool(text: str) -> str:
    """Add a new note to the user's notes."""
    db.add_note(text)
    return "Task added."

@tool
def list_notes_tool() -> str:
    """Get all the notes from the user’s notes."""
    rows = db.get_notes()
    return rows

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