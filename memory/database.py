import sqlite3
conn = sqlite3.connect('memory/database.db')

#TODO date, other relevant infos (name of user, style, verbosity)

def init_db():
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
    conn.execute("INSERT INTO tasks(task, notes, status) VALUES (?, ?, ?)", (task, notes, status))
    conn.commit()

def get_tasks():
    tasks = []
    rows = conn.execute("SELECT * FROM tasks WHERE status = ?", (1,))
    for task in rows:
        tasks.append(task)
    return tasks

def update_task(id, status=0):
    conn.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, id))
    conn.commit()

def add_grocery(grocery, amount=1, notes="", status=1):
    conn.execute("INSERT INTO groceries(grocery, amount, notes, status) VALUES (?, ?, ?, ?)", (grocery, amount, notes, status))
    conn.commit()

def get_groceries():
    tasks = []
    rows = conn.execute("SELECT * FROM groceries WHERE status = ?", (1,))
    for task in rows:
        tasks.append(task)
    return tasks

def update_grocery(id, status=0):
    conn.execute("UPDATE groceries SET status = ? WHERE id = ?", (status, id))
    conn.commit()

def add_note(note, status=1):
    conn.execute("INSERT INTO notes(note, status) VALUES (?, ?)", (note, status))
    conn.commit()

def get_notes():
    tasks = []
    rows = conn.execute("SELECT * FROM notes WHERE status = ?", (1,))
    for task in rows:
        tasks.append(task)
    return tasks

def update_notes(id, status=0):
    conn.execute("UPDATE notes SET status = ? WHERE id = ?", (status, id))
    conn.commit()

def delete_done():
    conn.execute("DELETE FROM tasks WHERE status = ?", (0,))
    conn.execute("DELETE FROM groceries WHERE status = ?", (0,))
    conn.execute("DELETE FROM notes WHERE status = ?", (0,))
    conn.commit()

def delete_note(id):
    conn.execute("DELETE FROM notes WHERE id = ?", (id,))
    conn.commit()

def delete_grocery(id):
    conn.execute("DELETE FROM groceries WHERE id = ?", (id,))
    conn.commit()

def delete_task(id):
    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()

