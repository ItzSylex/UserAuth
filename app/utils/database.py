import sqlite3

DATABASE = 'app/auth.db'


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY,
               username TEXT UNIQUE,
               email TEXT UNIQUE,
               password TEXT NOT NULL
           )'''
    )
    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    return conn
