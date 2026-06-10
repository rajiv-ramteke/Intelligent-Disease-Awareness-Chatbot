from flask import Blueprint, request, jsonify
from database import get_db

emergency_bp = Blueprint('emergency', __name__, url_prefix='/api/emergency')

@emergency_bp.route('/log', methods=['POST'])
def log_emergency():
    data = request.json
    session_id = data.get('session_id', 'unknown')
    trigger_words = data.get('trigger_words', '')
    user_message = data.get('message', '')

    db = get_db()
    db.execute(
        'INSERT INTO emergency_logs (session_id, trigger_words, user_message) VALUES (?, ?, ?)',
        (session_id, trigger_words, user_message)
    )
    db.commit()

    return jsonify({"status": "logged", "message": "Emergency logged securely."})
