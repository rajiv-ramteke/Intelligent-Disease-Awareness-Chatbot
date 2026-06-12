from flask import Blueprint, request, jsonify, Response, stream_with_context
from services.ai_service import get_chat_response_stream
import uuid

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

from flask_login import current_user
from database import get_db

@chat_bp.route('/message', methods=['POST'])
def chat_message():
    data = request.json
    message = data.get('message', '')
    session_id = data.get('session_id', str(uuid.uuid4()))
    language = data.get('language', 'en')

    if not message:
        return jsonify({"error": "Message is required"}), 400

    # Save user message to conversations memory
    try:
        db = get_db()
        db.execute(
            "INSERT INTO conversations (session_id, role, message) VALUES (?, ?, ?)",
            (session_id, 'user', message)
        )
        db.commit()
    except Exception as e:
        print(f"Memory error: {e}")
    finally:
        db.close()

    def generate():
        full_response = []
        try:
            for chunk in get_chat_response_stream(session_id, message, language):
                full_response.append(chunk)
                yield chunk
        finally:
            bot_resp = "".join(full_response)
            if bot_resp:
                db = get_db()
                try:
                    # Save bot response to conversations memory
                    db.execute(
                        "INSERT INTO conversations (session_id, role, message) VALUES (?, ?, ?)",
                        (session_id, 'assistant', bot_resp)
                    )
                    
                    # Save to logged-in user history
                    if current_user.is_authenticated:
                        db.execute(
                            "INSERT INTO chat_history (user_id, user_message, bot_response) VALUES (?, ?, ?)",
                            (current_user.id, message, bot_resp)
                        )
                    db.commit()
                except Exception as e:
                    print(f"Error saving chat history: {e}")
                finally:
                    db.close()

    return Response(stream_with_context(generate()), content_type='text/plain')

from deep_translator import GoogleTranslator

@chat_bp.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    text = data.get('text', '')
    target_lang = data.get('target', 'hi')
    
    if not text:
        return jsonify({"error": "Text is required"}), 400
        
    try:
        translated = GoogleTranslator(source='en', target=target_lang).translate(text)
        return jsonify({"translated": translated})
    except Exception as e:
        print(f"Translation error: {e}")
        return jsonify({"error": str(e)}), 500
