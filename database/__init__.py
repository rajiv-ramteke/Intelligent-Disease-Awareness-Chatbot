import sqlite3
import os

# Use /data directory on Hugging Face Spaces (persistent storage)
# Fallback to local database/ directory for local development
if os.path.exists('/data'):
    DATABASE = '/data/healthbot.db'
    SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')
else:
    DATABASE = os.path.join(os.path.dirname(__file__), 'healthbot.db')
    SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db_dir = os.path.dirname(DATABASE)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    db = get_db()
    with open(SCHEMA_PATH, 'r') as f:
        db.executescript(f.read())
    db.commit()
    db.close()
    print(f"Database initialized at: {DATABASE}")

if __name__ == '__main__':
    init_db()
