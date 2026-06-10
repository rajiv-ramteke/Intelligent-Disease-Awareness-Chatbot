import os
from openai import OpenAI
from config import Config
from chatbot.prompt_manager import get_system_prompt

def get_chat_response_stream(session_id, message, language='en'):
    # Initialize the client for NVIDIA API (OpenAI compatible)
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=Config.NVIDIA_API_KEY
    )
    
    system_prompt = get_system_prompt(language)
    
    messages = [{"role": "system", "content": system_prompt}]

    # Fetch conversation history from DB to give AI memory
    # We fetch the PREVIOUS messages (before the one we just inserted)
    try:
        from database import get_db
        db = get_db()
        # Get all messages for this session, ordered chronologically
        # But exclude the very last inserted row (the current user message we just saved)
        history = db.execute(
            """SELECT role, message FROM conversations 
               WHERE session_id = ? 
               AND id < (SELECT MAX(id) FROM conversations WHERE session_id = ?)
               ORDER BY id ASC LIMIT 20""",
            (session_id, session_id)
        ).fetchall()
        db.close()

        for row in history:
            messages.append({"role": row['role'], "content": row['message']})

    except Exception as e:
        print(f"Error fetching history: {e}")

    # Always append the current user message at the end (clean, no duplicates)
    messages.append({"role": "user", "content": message})


    try:
        completion = client.chat.completions.create(
            model="meta/llama-3.1-8b-instruct",
            messages=messages,
            temperature=0.8,
            top_p=0.95,
            max_tokens=2048,
            frequency_penalty=1.0,
            presence_penalty=0.6,
            stream=True
        )
        for chunk in completion:
            if hasattr(chunk, 'choices') and chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if hasattr(delta, 'content') and delta.content:
                    yield delta.content
    except Exception as e:
        print(f"Error calling AI API: {str(e)}", flush=True)
        yield f"API Error: {str(e)}"
