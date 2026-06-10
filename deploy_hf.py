import os
from huggingface_hub import HfApi

TOKEN = os.environ.get('HF_TOKEN', '')
if not TOKEN:
    print("Error: HF_TOKEN environment variable not set.")
    exit(1)

try:
    api = HfApi(token=TOKEN)
    user_info = api.whoami()
    username = user_info["name"]
    space_id = f"{username}/healthbot-pro"
    
    print(f"Creating or fetching Space: {space_id}...")
    api.create_repo(repo_id=space_id, repo_type="space", space_sdk="docker", exist_ok=True)
    
    print("Uploading files to Hugging Face Spaces...")
    api.upload_folder(
        folder_path=".",
        repo_id=space_id,
        repo_type="space",
        ignore_patterns=[
            ".env",
            "__pycache__/*",
            "*.pyc",
            ".git/*",
            "venv/*",
            ".idea/*",
            ".vscode/*",
            "deploy_hf.py",
            "healthbot.db",
            "*.log"
        ]
    )
    
    print(f"\nDeployment triggered successfully!")
    print(f"View your app at: https://huggingface.co/spaces/{space_id}")
except Exception as e:
    print(f"Error during deployment: {str(e)}")
