import sqlite3 as sq
import os
from pathlib import Path

from icecream import ic

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = os.path.join(BASE_DIR, 'database/database.db')


def create_db():
    conn = sq.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE table IF NOT EXISTS schedule "
              "(specialist TEXT, service TEXT, time TEXT, client_id INTEGER, is_busy INTEGER, date TEXT, week_day TEXT, price INTEGER)")
    conn.commit()
    conn.close()


def add_new(specialist, service, time, client_id, is_busy, date, week_day):
    conn = sq.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO schedule (specialist, service, time, client_id, is_busy, date, week_day) VALUES "
              "(?, ?, ?, ?, ?, ?, ?)", (specialist, service, time, client_id, is_busy, date, week_day))
    conn.commit()
    conn.close()


# def get_specialists():
#     conn = sq.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute("SELECT specialist FROM schedule")
#     data = c.fetchall()
#     print(list(set(data)))
#     conn.close()
#     return list(set(data))

def get_specialists():
    conn = sq.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT specialist FROM schedule")
    data = list(set(c.fetchall()))
    conn.close()
    specialists = []
    for row in data:
        full_name = row[0].strip()
        parts = full_name.split()
        if len(parts) >= 2:
            first_name, last_name = parts[0], ' '.join(parts[1:])
        else:
            first_name, last_name = full_name, ""
        specialists.append((first_name, last_name))
    return specialists


# def get_services_by_specialist(name):
#     conn = sq.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute("SELECT service FROM schedule WHERE specialist=?", (name,))
#     data = c.fetchall()
#     print(list(set(data)))
#     conn.close()
#     srvs = ''
#     for i in list(set(data)):
#         srvs += i[0] + ', '
#     return srvs[:-2]

def get_services_by_specialist(full_name):
    conn = sq.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT service FROM schedule WHERE specialist=?", (full_name,))
    data = c.fetchall()
    conn.close()

    # Преобразуем список кортежей в список строк
    services = [item[0] for item in data]
    unique_services = list(set(services))  # Убираем дубликаты
    print("Услуги:", unique_services)
    return unique_services


def get_time_on_specialist(name, profession):
    conn = sq.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT time, date, week_day FROM schedule WHERE specialist=? AND service=? AND is_busy=?",
              (name, profession, "N"))
    data = c.fetchall()
    conn.close()
    return list(data)


def get_time_on_date(date, name):
    conn = sq.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT time FROM schedule WHERE specialist=? AND date=? AND is_busy=?",
              (name, date, "N"))
    data = set(c.fetchall())
    conn.close()
    return list(data)


def service_n_cost_on_specialist_n_time(name, time, date):
    conn = sq.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT price, service FROM schedule WHERE specialist=? AND time=? AND date=?", (name, time, date))
    data = c.fetchall()
    conn.close()
    return data


def get_bookings_from_user_id(user_id):
    conn = sq.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT specialist, service, date, time FROM schedule WHERE client_id=?", (user_id,))
    data = c.fetchall()
    conn.close()
    ic(data)
    return data


def make_booking(user_id, service, specialist, date, time):
    conn = sq.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        UPDATE schedule 
        SET is_busy = 'Y', client_id = ? 
        WHERE service = ? AND specialist = ? AND date = ? AND time = ?
    """, (user_id, service, specialist, date, time))
    conn.commit()
    conn.close()

def get_profile_pic(user_id):
    conn = sq.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT url FROM profile_pictures WHERE User_id=?", (user_id,))
    data = c.fetchone()
    conn.close()
    ic(data)
    return data[0]


# conn = sq.connect(DB_PATH)
# c = conn.cursor()
# c.execute("""
# INSERT INTO schedule (specialist, service, time, client_id, is_busy, date, week_day, price) VALUES
# -- 23.05.2025 (пятница)
# ('Иванов Иван', 'Монтаж системы отопления', '10:00', NULL, 'N', '23.05.2025', 'friday', 4200),
# ('Петров Петр', 'Ремонт водопровода', '10:00', NULL, 'N', '23.05.2025', 'friday', 3800),
# ('Сидоров Сидор', 'Замена электропроводки', '11:00', NULL, 'N', '23.05.2025', 'friday', 4500),
# ('Николаев Николай', 'Установка канализационных труб', '12:00', NULL, 'N', '23.05.2025', 'friday', 5000),
# ('Алексеев Алексей', 'Ремонт насоса', '13:00', NULL, 'N', '23.05.2025', 'friday', 3200),
# ('Иванов Иван', 'Обслуживание котла', '14:00', NULL, 'N', '23.05.2025', 'friday', 4000),
# ('Петров Петр', 'Установка счетчика воды', '15:00', NULL, 'N', '23.05.2025', 'friday', 2800),
#
# -- 24.05.2025 (суббота)
# ('Сидоров Сидор', 'Ремонт вентиляции', '9:00', NULL, 'N', '24.05.2025', 'saturday', 3700),
# ('Николаев Николай', 'Монтаж газовой трубы', '9:00', NULL, 'N', '24.05.2025', 'saturday', 4800),
# ('Алексеев Алексей', 'Замена радиатора', '10:00', NULL, 'N', '24.05.2025', 'saturday', 4100),
# ('Иванов Иван', 'Установка фильтра очистки', '11:00', NULL, 'N', '24.05.2025', 'saturday', 3300),
# ('Петров Петр', 'Ремонт септика', '12:00', NULL, 'N', '24.05.2025', 'saturday', 5500),
# ('Сидоров Сидор', 'Диагностика системы отопления', '13:00', NULL, 'N', '24.05.2025', 'saturday', 3000),
# ('Николаев Николай', 'Прокладка водопровода', '14:00', NULL, 'N', '24.05.2025', 'saturday', 6000),
#
# -- 25.05.2025 (воскресенье)
# ('Алексеев Алексей', 'Установка термостата', '8:00', NULL, 'N', '25.05.2025', 'sunday', 2900),
# ('Иванов Иван', 'Ремонт водонагревателя', '8:00', NULL, 'N', '25.05.2025', 'sunday', 3600),
# ('Петров Петр', 'Замена крана', '9:00', NULL, 'N', '25.05.2025', 'sunday', 2700),
# ('Сидоров Сидор', 'Монтаж дренажной системы', '10:00', NULL, 'N', '25.05.2025', 'sunday', 4300),
# ('Николаев Николай', 'Установка насосной станции', '11:00', NULL, 'N', '25.05.2025', 'sunday', 5200),
# ('Алексеев Алексей', 'Ремонт электрического щитка', '12:00', NULL, 'N', '25.05.2025', 'sunday', 4700),
# ('Иванов Иван', 'Чистка труб', '13:00', NULL, 'N', '25.05.2025', 'sunday', 3400),
#
# -- 26.05.2025 (понедельник)
# ('Петров Петр', 'Установка счетчика тепла', '10:00', NULL, 'N', '26.05.2025', 'monday', 3100),
# ('Сидоров Сидор', 'Ремонт канализации', '10:00', NULL, 'N', '26.05.2025', 'monday', 4900),
# ('Николаев Николай', 'Монтаж труб ПВХ', '11:00', NULL, 'N', '26.05.2025', 'monday', 4400),
# ('Алексеев Алексей', 'Установка обратного клапана', '12:00', NULL, 'N', '26.05.2025', 'monday', 3500),
# ('Иванов Иван', 'Техническое обслуживание котла', '13:00', NULL, 'N', '26.05.2025', 'monday', 3900),
# ('Петров Петр', 'Замена компрессора', '14:00', NULL, 'N', '26.05.2025', 'monday', 5300),
# ('Сидоров Сидор', 'Прочистка канализационных труб', '15:00', NULL, 'N', '26.05.2025', 'monday', 4600),
#
# -- 27.05.2025 (вторник)
# ('Николаев Николай', 'Установка редукционного клапана', '9:00', NULL, 'N', '27.05.2025', 'tuesday', 3200),
# ('Алексеев Алексей', 'Ремонт циркуляционного насоса', '9:00', NULL, 'N', '27.05.2025', 'tuesday', 4000),
# ('Иванов Иван', 'Монтаж системы полива', '10:00', NULL, 'N', '27.05.2025', 'tuesday', 5000),
# ('Петров Петр', 'Установка фильтра грубой очистки', '11:00', NULL, 'N', '27.05.2025', 'tuesday', 3300),
# ('Сидоров Сидор', 'Ремонт насосной станции', '12:00', NULL, 'N', '27.05.2025', 'tuesday', 4800),
# ('Николаев Николай', 'Замена мембраны расширительного бака', '13:00', NULL, 'N', '27.05.2025', 'tuesday', 3600),
# ('Алексеев Алексей', 'Установка гидроаккумулятора', '14:00', NULL, 'N', '27.05.2025', 'tuesday', 4500),
#
# -- 28.05.2025 (среда)
# ('Иванов Иван', 'Ремонт системы отопления', '8:00', NULL, 'N', '28.05.2025', 'wednesday', 4700),
# ('Петров Петр', 'Монтаж душевой кабины', '8:00', NULL, 'N', '28.05.2025', 'wednesday', 5500),
# ('Сидоров Сидор', 'Установка счетчика электроэнергии', '9:00', NULL, 'N', '28.05.2025', 'wednesday', 3400),
# ('Николаев Николай', 'Ремонт электродвигателя', '10:00', NULL, 'N', '28.05.2025', 'wednesday', 4200),
# ('Алексеев Алексей', 'Замена проводов освещения', '11:00', NULL, 'N', '28.05.2025', 'wednesday', 3800),
# ('Иванов Иван', 'Установка автоматического выключателя', '12:00', NULL, 'N', '28.05.2025', 'wednesday', 2900),
# ('Петров Петр', 'Ремонт водяного счетчика', '13:00', NULL, 'N', '28.05.2025', 'wednesday', 3700),
#
# -- 29.05.2025 (четверг)
# ('Сидоров Сидор', 'Монтаж системы фильтрации воды', '10:00', NULL, 'N', '29.05.2025', 'thursday', 4600),
# ('Николаев Николай', 'Установка предохранительного клапана', '10:00', NULL, 'N', '29.05.2025', 'thursday', 3500),
# ('Алексеев Алексей', 'Ремонт системы вентиляции', '11:00', NULL, 'N', '29.05.2025', 'thursday', 4300),
# ('Иванов Иван', 'Замена теплообменника', '12:00', NULL, 'N', '29.05.2025', 'thursday', 5200),
# ('Петров Петр', 'Монтаж системы подогрева пола', '13:00', NULL, 'N', '29.05.2025', 'thursday', 6000),
# ('Сидоров Сидор', 'Установка датчика температуры', '14:00', NULL, 'N', '29.05.2025', 'thursday', 3100),
# ('Николаев Николай', 'Ремонт насоса повышения давления', '15:00', NULL, 'N', '29.05.2025', 'thursday', 4900),
#
# -- 30.05.2025 (пятница)
# ('Алексеев Алексей', 'Установка системы контроля давления', '9:00', NULL, 'N', '30.05.2025', 'friday', 4100),
# ('Иванов Иван', 'Ремонт канализационного насоса', '9:00', NULL, 'N', '30.05.2025', 'friday', 5300),
# ('Петров Петр', 'Монтаж системы охлаждения', '10:00', NULL, 'N', '30.05.2025', 'friday', 5800),
# ('Сидоров Сидор', 'Установка счетчика газа', '11:00', NULL, 'N', '30.05.2025', 'friday', 3900),
# ('Николаев Николай', 'Замена электромагнитного клапана', '12:00', NULL, 'N', '30.05.2025', 'friday', 3600),
# ('Алексеев Алексей', 'Ремонт системы автоматики', '13:00', NULL, 'N', '30.05.2025', 'friday', 4400),
# ('Иванов Иван', 'Установка расширительного бака', '14:00', NULL, 'N', '30.05.2025', 'friday', 4200),
#
# -- 31.05.2025 (суббота)
# ('Петров Петр', 'Ремонт системы отопления дома', '8:00', NULL, 'N', '31.05.2025', 'saturday', 5100),
# ('Сидоров Сидор', 'Монтаж системы дренажа', '8:00', NULL, 'N', '31.05.2025', 'saturday', 4700),
# ('Николаев Николай', 'Установка системы фильтрации канализации', '9:00', NULL, 'N', '31.05.2025', 'saturday', 5400),
# ('Алексеев Алексей', 'Ремонт водопроводной сети', '10:00', NULL, 'N', '31.05.2025', 'saturday', 4800),
# ('Иванов Иван', 'Замена системы вентиляции', '11:00', NULL, 'N', '31.05.2025', 'saturday', 5600),
# ('Петров Петр', 'Установка системы подачи воды', '12:00', NULL, 'N', '31.05.2025', 'saturday', 5000),
# ('Сидоров Сидор', 'Ремонт электрической панели', '13:00', NULL, 'N', '31.05.2025', 'saturday', 4500),
#
# -- 01.06.2025 (воскресенье)
# ('Николаев Николай', 'Монтаж системы орошения', '9:00', NULL, 'N', '01.06.2025', 'sunday', 4300),
# ('Алексеев Алексей', 'Установка насоса для скважины', '9:00', NULL, 'N', '01.06.2025', 'sunday', 5700),
# ('Иванов Иван', 'Ремонт системы отопления коттеджа', '10:00', NULL, 'N', '01.06.2025', 'sunday', 6200),
# ('Петров Петр', 'Замена трубопровода горячей воды', '11:00', NULL, 'N', '01.06.2025', 'sunday', 4900),
# ('Сидоров Сидор', 'Установка системы контроля уровня воды', '12:00', NULL, 'N', '01.06.2025', 'sunday', 4600),
# ('Николаев Николай', 'Ремонт системы отвода сточных вод', '13:00', NULL, 'N', '01.06.2025', 'sunday', 5300),
# ('Алексеев Алексей', 'Монтаж системы подогрева труб', '14:00', NULL, 'N', '01.06.2025', 'sunday', 5000)
# """)
# conn.commit()
#
# conn = sq.connect(DB_PATH)
# c = conn.cursor()
# c.execute("INSERT INTO schedule (specialist, service, time, client_id, is_busy, date, week_day, price) VALUES ('Николаев Николай', 'Демонтаж труб ПВХ', '11:00', NULL, 'N', '26.05.2025', 'monday', 4400)")
# conn.commit()
