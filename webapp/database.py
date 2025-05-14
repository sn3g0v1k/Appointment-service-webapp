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

def get_specialists():
    conn = sq.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT specialist FROM schedule")
    data = c.fetchall()
    print(list(set(data)))
    conn.close()
    return list(set(data))

def get_services_by_specialist(name):
    conn = sq.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT service FROM schedule WHERE specialist=?", (name,))
    data = c.fetchall()
    print(list(set(data)))
    conn.close()
    srvs = ''
    for i in list(set(data)):
        srvs += i[0] + ', '
    return srvs[:-2]

def get_time_on_specialist(name, profession):
    conn = sq.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT time, date, week_day FROM schedule WHERE specialist=? AND service=? AND is_busy=?", (name, profession, "N"))
    data = c.fetchall()
    conn.close()
    return list(data)

def get_time_on_date(date, name):
    conn = sq.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT time FROM schedule WHERE specialist=? AND date=?",
              (name, date))
    data = c.fetchall()
    conn.close()
    return list(data)

def service_n_cost_on_specialist_n_time(name, time, date):
    conn = sq.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT price FROM schedule WHERE specialist=? AND time=? AND date=?", (name, time, date))
    data = c.fetchall()
    conn.close()
    return data