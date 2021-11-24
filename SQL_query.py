from os import name
import sqlite3


def create_table(DB_name: str, table: str) -> dict:
    conn = sqlite3.connect(DB_name)
    cursor = conn.cursor()
    cursor.execute(f"""CREATE TABLE {table} (id INTEGER, name TEXT)""")
    conn.commit()
    print(f'{DB_name} - Создана таблица {table}')
    cursor.execute(f"""PRAGMA table_info({table})""")
    return cursor.fetchall()

def drop_table(DB_name: str, table: str) -> None:
    conn = sqlite3.connect(DB_name)
    cursor = conn.cursor()
    cursor.execute(f"""DROP TABLE {table}""")
    conn.commit()
    print(f'{DB_name} - удалена таблица {table}')

def select_all(DB_name: str, table: str) -> tuple:
    conn = sqlite3.connect(DB_name)
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM {table}""")
    return cursor.fetchall()

def select_all_where_simple(DB_name: str, table: str, cond: str) -> tuple:
    conn = sqlite3.connect(DB_name)
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM {table} WHERE {cond}""")
    return cursor.fetchall()

def insert_one_row(DB_name: str, table: str, **fields) -> None:
    conn = sqlite3.connect(DB_name)
    cursor = conn.cursor()
    field = ",".join(fields.keys())
    query = (f'INSERT INTO {table}({field}) VALUES')

    if len(fields) >= 2:
        query += '(?'
        query += ',?'*(len(fields)-1)+')'
    else:
        query += '(?)'

    cursor.execute(query, list(fields.values()))
    conn.commit()
    cursor.execute(f'SELECT * FROM {table} WHERE id=(SELECT max(id) FROM {table})')
    print(f'Запись добавлена в {table}')
    return cursor.fetchone()

def delete_rows(DB_name: str, table: str, cond: str):
    conn = sqlite3.connect(DB_name)
    cursor = conn.cursor()
    cursor.execute(f"""SELECT COUNT(*) FROM {table} WHERE {cond}""")
    count_rem_row = cursor.fetchone()[0]
    cursor.execute(f"""DELETE FROM {table} WHERE {cond}""")
    conn.commit()
    conn.close()
    print(f'{DB_name} - удалено {count_rem_row} записей по условию {cond}')

def update_row(DB_name: str, table: str, cond: str, **fields):
    conn = sqlite3.connect(DB_name)
    cursor = conn.cursor()
    query = f"""UPDATE {table} SET """
    for i in fields:
        query += str(i) + "=?, "
    query = query[:-2] + f' WHERE {cond}'
    cursor.execute(query, list(fields.values()))
    conn.commit()
    conn.close()
    print(query)

def count_rows(DB_name: str, table: str, cond: str="id>0") -> int:
    conn = sqlite3.connect(DB_name)
    cursor = conn.cursor()
    cursor.execute(f"""SELECT COUNT(*) FROM {table} WHERE {cond}""")
    res = cursor.fetchone()[0]
    conn.close()
    return res

print(select_all('DATABASE.db', 'Сategories'))
print(count_rows('DATABASE.db', 'Сategories', 'id=7'))
