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
    
    # Normally we'd fetch conversation history from DB here using session_id
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ]

    try:
        completion = client.chat.completions.create(
            model="meta/llama-3.1-8b-instruct",
            messages=messages,
            temperature=0.5,
            top_p=1,
            max_tokens=1024,
            stream=True
        )
        for chunk in completion:
            if hasattr(chunk, 'choices') and chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if hasattr(delta, 'content') and delta.content:
                    yield delta.content
    except Exception as e:
        print(f"Error calling AI API: {e}")
        yield "I'm sorry, I'm having trouble connecting to my AI core right now. Please try again later."
