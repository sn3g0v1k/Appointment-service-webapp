import sqlite3 as sq
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = os.path.join(BASE_DIR, 'database/database.db')


def create_db():
    conn = sq.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE table IF NOT EXISTS schedule "
              "(specialist TEXT, service TEXT, time TEXT, client_id INTEGER, is_busy INTEGER, date TEXT, week_day TEXT)")
    conn.commit()
    conn.close()


def add_new(specialist, service, time, client_id, is_busy, date, week_day):
    conn = sq.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO schedule (specialist, service, time, client_id, is_busy, date, week_day) VALUES "
              "(?, ?, ?, ?, ?, ?, ?)", (specialist, service, time, client_id, is_busy, date, week_day))
    conn.commit()
    conn.close()