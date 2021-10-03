import sqlite3

sql1 = """
    CREATE TABLE IF NOT EXISTS User(
        email TEXT PRIMARY KEY,
        name TEXT,
        password TEXT NOT NULL,
        gender TEXT,
        dob TEXT,
        college TEXT
        
    );
"""

sql2 = """
    CREATE TABLE IF NOT EXISTS Mail(
        no INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        sender TEXT NOT NULL,
        receiver TEXT NOT NULL,
        subject TEXT,
        content TEXT,
        time TEXT,
        att TEXT,
        att_als TEXT,
        del_s BOOLEAN,
        del_r BOOLEAN
    );
"""


def execute_query(sql):
    with sqlite3.connect("mail.db") as conn:
        cur = conn.cursor()
        result = cur.execute(sql)
        conn.commit()
    return result


if __name__ == '__main__':
    execute_query(sql2)
