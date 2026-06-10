from flask import Flask, render_template, jsonify, redirect, url_for, flash
from config import Config
from database import init_db, get_db
import os

from flask_login import LoginManager, login_required, current_user
from models.user import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    # Ensure database is initialized
    init_db()

    # Register blueprints (routes)
    from routes.chat_routes import chat_bp
    from routes.location_routes import location_bp
    from routes.admin_routes import admin_bp
    from routes.emergency_routes import emergency_bp
    from routes.voice_routes import voice_bp
    from routes.auth_routes import auth_bp

    app.register_blueprint(chat_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(emergency_bp)
    app.register_blueprint(voice_bp)
    app.register_blueprint(auth_bp)

    @app.route('/')
    def index():
        return render_template('landing.html')

    @app.route('/chat')
    def chat_interface():
        return render_template('chat.html')

    @app.route('/history')
    @login_required
    def chat_history_page():
        db = get_db()
        history = db.execute(
            "SELECT * FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC", 
            (current_user.id,)
        ).fetchall()
        db.close()
        return render_template('history.html', history=history)

    @app.route('/history/delete', methods=['POST'])
    @login_required
    def delete_chat_history():
        db = get_db()
        db.execute("DELETE FROM chat_history WHERE user_id = ?", (current_user.id,))
        db.commit()
        db.close()
        flash("Chat history deleted successfully.")
        return redirect(url_for('chat_history_page'))

    @app.route('/health')
    def health_check():
        return jsonify({"status": "running"}), 200

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=8000)
