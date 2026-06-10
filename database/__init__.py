import sqlite3
import os

DATABASE = 'database/healthbot.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    if not os.path.exists('database'):
        os.makedirs('database')
    db = get_db()
    with open('database/schema.sql', 'r') as f:
        db.executescript(f.read())
    db.commit()
    db.close()
    print("Database initialized.")

if __name__ == '__main__':
    init_db()
