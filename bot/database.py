import sqlite3
import logging
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = os.path.join(BASE_DIR, 'database/database.db')

logger = logging.getLogger(__name__)

def create_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                specialist TEXT NOT NULL,
                service TEXT NOT NULL,
                time TEXT NOT NULL,
                client_id TEXT,
                is_busy TEXT NOT NULL,
                date TEXT NOT NULL,
                week_day TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Ошибка при создании базы данных: {str(e)}")
        raise

def add_new(specialist, service, time, client_id, is_busy, date, week_day, price):
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO schedule (specialist, service, time, client_id, is_busy, date, week_day, price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (specialist, service, time, client_id, is_busy, date, week_day, price))
        conn.commit()
        conn.close()
    except Exception as e:
        conn.close()
        logger.error(f"Ошибка при добавлении записи: {str(e)}")
        raise

def get_user_appointments(user_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT specialist, service, time, date
            FROM schedule
            WHERE client_id = ?
            ORDER BY date DESC, time ASC
        ''', (str(user_id),))
        appointments = cursor.fetchall()
        conn.close()
        
        return [
            {
                'specialist': app[0],
                'service': app[1],
                'time': app[2],
                'date': app[3]
            }
            for app in appointments
        ]
    except Exception as e:
        logger.error(f"Ошибка при получении записей пользователя: {str(e)}")
        raise

def save_user_picture_and_nickname(user_id, pic_url, nickname):
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute('''
                SELECT * FROM profile_pictures WHERE User_id=?
            ''',
                       (user_id)
                       )
        data = cursor.fetchall()
        if len(data) == 1:
            cursor.execute('''
                            UPDATE url, nickname IN profile_pictures WHERE User_id=?
                            VALUES (?, ?)
                        ''', (user_id, pic_url, nickname))
            conn.commit()
            conn.close()
            return
        elif len(data) > 1:
            cursor.execute('''
                            DELETE FROM profile_pictures WHERE User_id=?
                        ''',
                           (user_id)
                           )
            conn.commit()

        cursor.execute('''
                INSERT INTO profile_pictures (User_id, url, nickname)
                VALUES (?, ?, ?)
            ''', (user_id, pic_url, nickname))
        conn.commit()
        conn.close()
    except Exception as e:
        conn.close()
        logger.error(f"Ошибка при записи профиля пользователя: {str(e)}")
        raise
