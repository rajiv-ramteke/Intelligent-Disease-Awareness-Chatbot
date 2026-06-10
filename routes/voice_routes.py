from flask import Blueprint, jsonify

voice_bp = Blueprint('voice', __name__, url_prefix='/api/voice')

# Note: Actual voice processing (STT/TTS) is handled on the client side 
# via Browser Web Speech API as per requirements. 
# This route is a placeholder for potential backend voice processing/config.

@voice_bp.route('/config', methods=['GET'])
def get_voice_config():
    return jsonify({
        "stt_enabled": True,
        "tts_enabled": True,
        "supported_languages": ["en-US", "hi-IN", "mr-IN"]
    })
