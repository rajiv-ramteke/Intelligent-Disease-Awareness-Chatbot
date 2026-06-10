from flask_login import UserMixin
from database import get_db

class User(UserMixin):
    def __init__(self, id, name, email, password_hash):
        self.id = str(id)
        self.name = name
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        db = get_db()
        user_row = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        db.close()
        if not user_row:
            return None
        return User(user_row['id'], user_row['name'], user_row['email'], user_row['password_hash'])

    @staticmethod
    def get_by_email(email):
        db = get_db()
        user_row = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        db.close()
        if not user_row:
            return None
        return User(user_row['id'], user_row['name'], user_row['email'], user_row['password_hash'])

    @staticmethod
    def create(name, email, password_hash):
        db = get_db()
        cursor = db.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash)
        )
        db.commit()
        user_id = cursor.lastrowid
        db.close()
        return User(user_id, name, email, password_hash)
