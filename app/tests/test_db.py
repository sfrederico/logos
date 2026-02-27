

import pytest
from unittest.mock import Mock, patch, MagicMock
from flask import Flask, g

from src.db import get_db


@pytest.fixture
def app():
    """Create a Flask app for testing."""
    app = Flask(__name__)
    return app


@pytest.fixture
def app_context(app):
    """Create an application context for testing."""
    with app.app_context():
        yield


def test_get_db_creates_new_connection(app_context):
    """Test that get_db creates a new connection when one doesn't exist."""
    
    # Mock psycopg2.connect
    with patch('src.db.psycopg2.connect') as mock_connect:
        mock_db = Mock()
        mock_connect.return_value = mock_db
        
        # Call get_db
        result = get_db()
        
        # Assert connect was called once
        assert mock_connect.call_count == 1
        
        # Assert the connection was stored in g
        assert g.db is mock_db
        
        # Assert the function returned the connection
        assert result is mock_db


def test_get_db_reuses_existing_connection(app_context):
    """Test that get_db returns existing connection from g."""
    
    # Mock an existing connection in g
    mock_existing_db = Mock()
    g.db = mock_existing_db
    
    # Mock psycopg2.connect
    with patch('src.db.psycopg2.connect') as mock_connect:
        # Call get_db
        result = get_db()
        
        # Assert connect was NOT called
        assert mock_connect.call_count == 0
        
        # Assert the existing connection was returned
        assert result is mock_existing_db


def test_get_db_uses_correct_settings(app_context):
    """Test that get_db uses the correct database settings."""
    
    # Mock psycopg2.connect
    with patch('src.db.psycopg2.connect') as mock_connect:
        with patch('src.db.Settings') as mock_settings:
            # Set up mock settings
            mock_settings.DB_NAME = 'test_db'
            mock_settings.DB_USER = 'test_user'
            mock_settings.DB_PASSWORD = 'test_password'
            mock_settings.DB_HOST = 'localhost'
            mock_settings.DB_PORT = 5432
            
            mock_db = Mock()
            mock_connect.return_value = mock_db
            
            # Call get_db
            get_db()
            
              
            mock_connect.assert_called_once_with(
                dbname='test_db',
                user='test_user',
                password='test_password',
                host='localhost',
                port=5432
            )# Assert connect was called with correct parameters