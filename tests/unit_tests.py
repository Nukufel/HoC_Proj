import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import memory.database as db
from tools import (
    add_event_tool,
    get_events_tool,
    delete_event_by_id_tool,
    update_user_name_tool,
    update_user_birthdate_tool,
    get_user_tool,
    add_grocery_tool,
    list_groceries_tool,
    set_grocery_done_tool,
    remove_grocery_tool,
    add_note_tool,
    list_notes_tool,
    set_note_done_tool,
    remove_note_tool,
    delete_done_tool,
)


@pytest.fixture()
def fresh_db(tmp_path, monkeypatch):
    db_file = str(tmp_path / 'test.db')
    monkeypatch.setattr('memory.database.DB_PATH', db_file)
    import memory.database as _db
    _db.init_db()
    return db_file


#  Helpers

def add_event(title='Meeting', start='2026-06-10T10:00:00', reoccurring=0):
    add_event_tool.func(title=title, start=start, duration=1.0, location='', description='', reoccurring=reoccurring)

def add_grocery(text='Milk'):
    add_grocery_tool.func(text=text, amount='1')

def add_note(text='Buy flowers'):
    add_note_tool.func(text=text)


# Events

def test_add_and_get_event(fresh_db):
    add_event('Event1')
    assert 'Event1' in get_events_tool.func()

def test_delete_event(fresh_db):
    add_event('Doctor')
    event_id = db.get_all_events()[0]['id']
    delete_event_by_id_tool.func(id=event_id)
    assert db.get_all_events() == []

def test_add_reoccurring_event_sets_flag(fresh_db):
    add_event('School', reoccurring=1)
    assert db.get_all_events()[0]['reoccurring'] == 1

def test_get_events_empty(fresh_db):
    assert get_events_tool.func() == 'No information stored.'


# User Profile

def test_update_name(fresh_db):
    update_user_name_tool.func(name='Alice')
    assert 'Alice' in get_user_tool.func()

def test_update_name_overwrites(fresh_db):
    update_user_name_tool.func(name='Alice')
    update_user_name_tool.func(name='Bob')
    result = get_user_tool.func()
    assert 'Bob' in result and 'Alice' not in result

def test_update_birthdate(fresh_db):
    update_user_birthdate_tool.func(birthdate='1995-07-20')
    assert '1995-07-20' in get_user_tool.func()


# Groceries

def test_add_and_list_grocery(fresh_db):
    add_grocery('Eggs')
    assert 'Eggs' in list_groceries_tool.func()

def test_mark_grocery_done_hides_it(fresh_db):
    add_grocery('Milk')
    item_id = db.get_groceries()[0]['id']
    set_grocery_done_tool.func(id=item_id)
    assert list_groceries_tool.func() == 'No information stored.'

def test_remove_grocery(fresh_db):
    add_grocery('Bread')
    item_id = db.get_groceries()[0]['id']
    remove_grocery_tool.func(id=item_id)
    assert db.get_groceries() == []


# Notes

def test_add_and_list_note(fresh_db):
    add_note('Call dentist')
    assert 'Call dentist' in list_notes_tool.func()

def test_mark_note_done_hides_it(fresh_db):
    add_note('Task')
    note_id = db.get_notes()[0]['id']
    set_note_done_tool.func(id=note_id)
    assert list_notes_tool.func() == 'No information stored.'

def test_remove_note(fresh_db):
    add_note('Temporary')
    note_id = db.get_notes()[0]['id']
    remove_note_tool.func(id=note_id)
    assert db.get_notes() == []


# delete_done

def test_delete_done_clears_completed_items(fresh_db):
    add_grocery('Done grocery')
    add_note('Done note')
    set_grocery_done_tool.func(id=db.get_groceries()[0]['id'])
    set_note_done_tool.func(id=db.get_notes()[0]['id'])
    delete_done_tool.func()
    assert db.get_groceries() == [] and db.get_notes() == []

def test_delete_done_keeps_active_items(fresh_db):
    add_grocery('Keep')
    add_note('Keep note')
    delete_done_tool.func()
    assert len(db.get_groceries()) == 1
    assert len(db.get_notes()) == 1


# Reoccurring events

def test_past_reoccurring_event_advances_by_7_days(fresh_db):
    from datetime import datetime, timedelta
    past = (datetime.now() - timedelta(days=3)).isoformat()
    db.add_event('Weekly', past, reoccurring=1)
    db.update_reoccurring_events()
    expected = datetime.fromisoformat(past) + timedelta(days=7)
    result = datetime.fromisoformat(db.get_all_events()[0]['start_time'])
    assert abs((result - expected).total_seconds()) < 2

def test_non_reoccurring_past_event_not_advanced(fresh_db):
    from datetime import datetime, timedelta
    past = (datetime.now() - timedelta(days=3)).isoformat()
    db.add_event('One-off', past, reoccurring=0)
    db.update_reoccurring_events()
    assert db.get_all_events()[0]['start_time'] == past
