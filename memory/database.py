import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta

DB_PATH = 'memory/database.db'


def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY,
                name TEXT,
                birthdate TEXT
            )
        """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                start_time  NOT NULL,
                duration FLOAT,
                location TEXT,
                description TEXT,
                reoccurring INTEGER
            )
        """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS groceries (
                id INTEGER PRIMARY KEY,
                grocery TEXT,
                amount TEXT,
                notes TEXT,
                status INTEGER
            )
        """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                note TEXT,
                status INTEGER
            )      
        """
        )

        conn.execute(
            "INSERT OR IGNORE INTO user (id, name, birthdate) VALUES (1, '', '')"
        )


# --- user functions ---
def create_user():
    with get_db() as conn:
        conn.execute(
            'INSERT INTO user (id, name, birthdate) VALUES (?, ?, ?)',
            (1, '', ''),
        )


def update_user_name(name):
    with get_db() as conn:
        conn.execute('UPDATE user SET name = ? WHERE id = ?', (name, 1))


def update_user_birthdate(birthdate):
    with get_db() as conn:
        conn.execute(
            'UPDATE user SET birthdate = ? WHERE id = ?', (birthdate, 1)
        )


def get_user():
    with get_db() as conn:
        return conn.execute('SELECT * FROM user').fetchall()


# --- event functions ---
def update_reoccurring_events():
    with get_db() as conn:
        now = datetime.now().isoformat()
        events = conn.execute(
            'SELECT id, start_time FROM events WHERE reoccurring = 1 AND start_time < ?',
            (now,),
        ).fetchall()
        for event in events:
            new_start = (
                datetime.fromisoformat(event['start_time']) + timedelta(days=7)
            ).isoformat()
            conn.execute(
                'UPDATE events SET start_time = ? WHERE id = ?',
                (new_start, event['id']),
            )


def add_event(
    title, start_time, duration=1.0, location='', description='', reoccurring=0
):
    with get_db() as conn:
        conn.execute(
            'INSERT INTO events(title, start_time, duration, location, description, reoccurring) VALUES (?, ?, ?, ?, ?, ?)',
            (title, start_time, duration, location, description, reoccurring),
        )


def get_events_between(start, end):
    with get_db() as conn:
        return conn.execute(
            'SELECT * FROM events WHERE start_time BETWEEN ? AND ?',
            (start.isoformat(), end.isoformat()),
        ).fetchall()


def get_event_by_text(search: str):
    with get_db() as conn:
        return conn.execute(
            'SELECT * FROM events WHERE title LIKE ?', (f'%{search}%',)
        ).fetchall()


def get_event_by_id(id: int):
    with get_db() as conn:
        return conn.execute(
            'SELECT * FROM events WHERE id = ?', (id,)
        ).fetchall()


def delete_event_by_id(id: int):
    with get_db() as conn:
        conn.execute('DELETE FROM events WHERE id=?', (id,))


def get_all_events():
    with get_db() as conn:
        return conn.execute('SELECT * FROM events').fetchall()


# --- grocery functions ---
def add_grocery(grocery, amount='1', notes='', status=1):
    with get_db() as conn:
        conn.execute(
            'INSERT INTO groceries(grocery, amount, notes, status) VALUES (?, ?, ?, ?)',
            (grocery, amount, notes, status),
        )


def get_groceries():
    with get_db() as conn:
        return conn.execute(
            'SELECT * FROM groceries WHERE status = ?', (1,)
        ).fetchall()


def update_grocery(id, status=0):
    with get_db() as conn:
        conn.execute(
            'UPDATE groceries SET status = ? WHERE id = ?', (status, id)
        )


def delete_grocery(id):
    with get_db() as conn:
        conn.execute('DELETE FROM groceries WHERE id = ?', (id,))


# --- notes functions ---
def add_note(note, status=1):
    with get_db() as conn:
        conn.execute(
            'INSERT INTO notes(note, status) VALUES (?, ?)', (note, status)
        )


def get_notes():
    with get_db() as conn:
        return conn.execute(
            'SELECT * FROM notes WHERE status = ?', (1,)
        ).fetchall()


def update_notes(id, status=0):
    with get_db() as conn:
        conn.execute('UPDATE notes SET status = ? WHERE id = ?', (status, id))


def delete_note(id):
    with get_db() as conn:
        conn.execute('DELETE FROM notes WHERE id = ?', (id,))


# --- other functions ---
def delete_done():
    with get_db() as conn:
        conn.execute('DELETE FROM groceries WHERE status = ?', (0,))
        conn.execute('DELETE FROM notes WHERE status = ?', (0,))


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f'Database error: {e}')
        raise
    finally:
        conn.close()


init_db()
