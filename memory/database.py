import sqlite3

DB_PATH = "memory/database.db"

def get_connection():
    return sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )

def init_db():
    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            name TEXT,
            birthdate TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT,
            location TEXT,
            description TEXT,
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

    conn.execute("INSERT INTO user (id, name, birthdate, note) VALUES (?, ?, ?, ?)", (1, "", "", ""))
    conn.commit()
    conn.close()


# --- user functions ---
def update_user_name(name):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE user SET name = ? WHERE id = ?", (name, 1))
    conn.commit()
    conn.close()

def update_user_birthdate(birthdate):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE user SET birthdate = ? WHERE id = ?", (birthdate, 1))
    conn.commit()
    conn.close()


# --- evnet functions ---
def add_event(title, start_time, end_time = "", location = "", description = "", status = 1):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO events(title, start_time, end_time, location, description, status) VALUES (?, ?, ?, ?, ?, ?)",(title, start_time, end_time, location, description, status),)
    conn.commit()
    conn.close()

def get_events_between(start, end):
    conn = sqlite3.connect(DB_PATH)
    out = conn.execute("SELECT * FROM events WHERE start_time BETWEEN ? AND ?",(start.isoformat(), end.isoformat()),)
    conn.close()
    return out

def get_event_by_text(search: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("SELECT * FROM events WHERE title LIKE ?",(search,))
    conn.commit()
    conn.close()

def delete_event_by_text(search: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM events WHERE title LIKE ?",(f"%{search}%",))
    conn.commit()
    conn.close()

def delete_event_by_id(id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM events WHERE id=?",(id,))
    conn.commit()
    conn.close()

def get_all_events():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT * FROM events")
    names = conn.execute("PRAGMA table_info(events)").fetchall()
    conn.close()
    return zip(names, rows)


# --- grocery functions ---
def add_grocery(grocery, amount=1, notes="", status=1):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO groceries(grocery, amount, notes, status) VALUES (?, ?, ?, ?)", (grocery, amount, notes, status))
    conn.commit()
    conn.close()

def get_groceries():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT * FROM groceries WHERE status = ?", (1,))
    names = conn.execute("PRAGMA table_info(groceries)")
    conn.close()
    return zip(names, rows)

def update_grocery(id, status=0):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE groceries SET status = ? WHERE id = ?", (status, id))
    conn.commit()
    conn.close()

def delete_grocery(id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM groceries WHERE id = ?", (id,))
    conn.commit()
    conn.close()


# --- notes functions ---
def add_note(note, status=1):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO notes(note, status) VALUES (?, ?)", (note, status))
    conn.commit()
    conn.close()

def get_notes():
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT * FROM notes WHERE status = ?", (1,))
    names = conn.execute("PRAGMA table_info(notes)").fetchall()
    conn.close()
    return zip(names, rows)

def update_notes(id, status=0):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE notes SET status = ? WHERE id = ?", (status, id))
    conn.commit()
    conn.close()

def delete_note(id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM notes WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# --- other functions ---
def delete_done():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM tasks WHERE status = ?", (0,))
    conn.execute("DELETE FROM groceries WHERE status = ?", (0,))
    conn.execute("DELETE FROM notes WHERE status = ?", (0,))
    conn.commit()
    conn.close()






init_db()