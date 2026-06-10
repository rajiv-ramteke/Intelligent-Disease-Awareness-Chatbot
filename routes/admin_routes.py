from flask import Blueprint, render_template, jsonify
from database import get_db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def dashboard():
    return render_template('admin.html')

@admin_bp.route('/stats')
def get_stats():
    db = get_db()
    
    # Get basic stats
    conversations_count = db.execute('SELECT COUNT(*) FROM conversations').fetchone()[0]
    emergencies_count = db.execute('SELECT COUNT(*) FROM emergency_logs').fetchone()[0]
    
    return jsonify({
        "total_conversations": conversations_count,
        "emergency_alerts": emergencies_count,
        "api_status": "running"
    })
