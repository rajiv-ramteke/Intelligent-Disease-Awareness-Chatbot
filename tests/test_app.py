import pytest
import os
import sqlite3
from app import create_app
from database import init_db

@pytest.fixture
def client():
    # Setup
    os.environ['DATABASE_URI'] = 'sqlite:///:memory:' # Use in-memory DB for tests
    app = create_app()
    app.config['TESTING'] = True
    
    # Initialize DB specifically for test environment if needed
    db = sqlite3.connect(':memory:')
    db.row_factory = sqlite3.Row
    with open('database/schema.sql', 'r') as f:
        db.executescript(f.read())
        
    with app.test_client() as client:
        yield client
        
    # Teardown
    db.close()

def test_health_check(client):
    rv = client.get('/health')
    assert rv.status_code == 200
    assert b'running' in rv.data

def test_chat_message_missing_data(client):
    rv = client.post('/api/chat/message', json={})
    assert rv.status_code == 400
    assert b'Message is required' in rv.data

def test_admin_dashboard(client):
    rv = client.get('/admin/')
    assert rv.status_code == 200
    assert b'Admin Dashboard' in rv.data
