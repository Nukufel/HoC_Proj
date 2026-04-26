import sqlite3

DB_PATH = "memory/database.db"

def get_connection():
    return sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )

#TODO date, other relevant infos (name of user, style, verbosity)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            task TEXT,
            notes TEXT,
            status INTEGER
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS groceries (
            id INTEGER PRIMARY KEY,
            grocery TEXT,
            amount INTEGER,
            notes TEXT,
            status INTEGER
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY,
            note TEXT,
            status INTEGER
        )      
    """)
    conn.commit()

def add_task(task, notes="", status=1):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO tasks(task, notes, status) VALUES (?, ?, ?)", (task, notes, status))
    conn.commit()

def get_tasks():
    conn = sqlite3.connect(DB_PATH)
    items = []
    rows = conn.execute("SELECT * FROM tasks WHERE status = ?", (1,))
    for row in rows:
        items.append(row)
    return items

def update_task(id, status=0):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, id))
    conn.commit()

def add_grocery(grocery, amount=1, notes="", status=1):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO groceries(grocery, amount, notes, status) VALUES (?, ?, ?, ?)", (grocery, amount, notes, status))
    conn.commit()

def get_groceries():
    conn = sqlite3.connect(DB_PATH)
    items = []
    rows = conn.execute("SELECT * FROM groceries WHERE status = ?", (1,))
    for row in rows:
        items.append(row)
    return items

def update_grocery(id, status=0):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE groceries SET status = ? WHERE id = ?", (status, id))
    conn.commit()

def add_note(note, status=1):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO notes(note, status) VALUES (?, ?)", (note, status))
    conn.commit()

def get_notes():
    conn = sqlite3.connect(DB_PATH)
    items = []
    rows = conn.execute("SELECT * FROM notes WHERE status = ?", (1,))
    for row in rows:
        items.append(row)
    return items

def update_notes(id, status=0):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE notes SET status = ? WHERE id = ?", (status, id))
    conn.commit()

def delete_done():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM tasks WHERE status = ?", (0,))
    conn.execute("DELETE FROM groceries WHERE status = ?", (0,))
    conn.execute("DELETE FROM notes WHERE status = ?", (0,))
    conn.commit()

def delete_note(id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM notes WHERE id = ?", (id,))
    conn.commit()

def delete_grocery(id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM groceries WHERE id = ?", (id,))
    conn.commit()

def delete_task(id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()

init_db()