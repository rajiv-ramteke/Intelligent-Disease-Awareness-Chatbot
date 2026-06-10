#!/bin/bash
# Startup script for deployment

echo "Starting HealthBot Pro..."

# Initialize database if needed (add any DB migration logic here)
python -c "from database.schema import init_db; init_db()"

# Start gunicorn
gunicorn --config deployment/gunicorn.conf.py app:app
