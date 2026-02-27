import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, patch, mock_open, MagicMock
from flask import Flask

from src.app import create_app, app as flask_app, home, health, error, db, BRAZIL_TZ


@pytest.fixture
def app():
    """Create a test Flask application."""
    with patch('src.app.init_db'):
        flask_app.config['TESTING'] = True
        yield flask_app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


def test_create_app_returns_flask_instance():
    """Test that create_app returns a Flask instance."""
    with patch('src.app.init_db'):
        app = create_app()
        assert isinstance(app, Flask)


def test_create_app_sets_uptime():
    """Test that create_app sets APP_UPTIME in config."""
    with patch('src.app.init_db'):
        before_create = datetime.now(tz=BRAZIL_TZ)
        app = create_app()
        after_create = datetime.now(tz=BRAZIL_TZ)
        
        assert 'APP_UPTIME' in app.config
        assert isinstance(app.config['APP_UPTIME'], datetime)
        assert before_create <= app.config['APP_UPTIME'] <= after_create


def test_create_app_initializes_db():
    """Test that create_app calls init_db."""
    with patch('src.app.init_db') as mock_init_db:
        app = create_app()
        mock_init_db.assert_called_once_with(app)


def test_create_app_configures_proxy_fix():
    """Test that create_app configures ProxyFix middleware."""
    with patch('src.app.init_db'):
        app = create_app()
        # Check if ProxyFix is applied
        assert hasattr(app, 'wsgi_app')
        assert app.wsgi_app.__class__.__name__ == 'ProxyFix'


def test_home_returns_200(client):
    """Test that the home route returns 200 status code."""
    mock_readme_content = "# Test README\n\nThis is a test."
    
    mock_file = mock_open(read_data=mock_readme_content)
    with patch('pathlib.Path.open', mock_file):
        response = client.get('/')
        assert response.status_code == 200


def test_home_reads_readme_file(client):
    """Test that home route reads the README.md file."""
    mock_readme_content = "# Test README"
    
    mock_file = mock_open(read_data=mock_readme_content)
    with patch('pathlib.Path.open', mock_file):
        response = client.get('/')
        # Verify that the file was opened
        mock_file.assert_called_once()


def test_home_converts_markdown_to_html(client):
    """Test that home route converts markdown content to HTML."""
    mock_readme_content = "# Test Header\n\nParagraph text."
    
    mock_file = mock_open(read_data=mock_readme_content)
    with patch('pathlib.Path.open', mock_file):
        response = client.get('/')
        data = response.get_data(as_text=True)
        # Check that markdown was converted (header should be in HTML format)
        assert '<h1>Test Header</h1>' in data


def test_home_renders_template(client):
    """Test that home route uses the home.html template."""
    mock_readme_content = "# Test"
    
    mock_file = mock_open(read_data=mock_readme_content)
    with patch('pathlib.Path.open', mock_file):
        with patch('src.app.render_template') as mock_render:
            mock_render.return_value = "rendered content"
            response = client.get('/')
            # Verify render_template was called with correct template
            mock_render.assert_called_once()
            args = mock_render.call_args[0]
            assert args[0] == 'home.html'
            # Verify html parameter is passed
            assert 'html' in mock_render.call_args[1]


def test_home_with_fenced_code_blocks(client):
    """Test that home route handles fenced code blocks in markdown."""
    mock_readme_content = "# Test\n\n```python\nprint('hello')\n```"
    
    mock_file = mock_open(read_data=mock_readme_content)
    with patch('pathlib.Path.open', mock_file):
        response = client.get('/')
        assert response.status_code == 200
        data = response.get_data(as_text=True)
        # Check that content is present (code block should be processed)
        assert 'Test' in data


def test_health_returns_200(client):
    """Test that the health route returns 200 status code."""
    response = client.get('/health')
    assert response.status_code == 200


def test_health_returns_json_with_required_fields(client):
    """Test that health route returns JSON with all required fields."""
    response = client.get('/health')
    data = response.get_json()
    
    assert 'status' in data
    assert 'database' in data
    assert 'uptime' in data
    assert 'timestamp' in data


def test_health_status_is_healthy(client):
    """Test that health route returns 'healthy' status."""
    response = client.get('/health')
    data = response.get_json()
    
    assert data['status'] == 'healthy'


def test_health_database_status_is_true(client):
    """Test that health route returns database status as True."""
    response = client.get('/health')
    data = response.get_json()
    
    assert data['database'] is True


def test_health_timestamp_is_iso_format(client):
    """Test that health route returns timestamp in ISO format."""
    response = client.get('/health')
    data = response.get_json()
    
    # Try to parse the timestamp as ISO format
    timestamp_str = data['timestamp']
    parsed_timestamp = datetime.fromisoformat(timestamp_str)
    
    # Verify it's a valid datetime
    assert isinstance(parsed_timestamp, datetime)
    # Verify timezone is present
    assert parsed_timestamp.tzinfo is not None


def test_health_uptime_format(client):
    """Test that health route returns uptime in correct format."""
    response = client.get('/health')
    data = response.get_json()
    
    uptime = data['uptime']
    # Uptime should be in format: "Xd Xh Xm Xs"
    assert 'd' in uptime
    assert 'h' in uptime
    assert 'm' in uptime
    assert 's' in uptime


def test_health_uptime_calculation(client, app):
    """Test that health route calculates uptime correctly."""
    # Mock the uptime to a known value
    mock_uptime = datetime.now(tz=BRAZIL_TZ) - timedelta(days=1, hours=2, minutes=3, seconds=4)
    app.config['APP_UPTIME'] = mock_uptime
    
    response = client.get('/health')
    data = response.get_json()
    
    uptime_str = data['uptime']
    # Should contain 1 day
    assert '1d' in uptime_str


def test_health_uses_brazil_timezone(client):
    """Test that health route uses Brazil timezone for timestamp."""
    with patch('src.app.datetime') as mock_datetime:
        mock_now = datetime(2026, 2, 27, 10, 30, 0, tzinfo=BRAZIL_TZ)
        mock_datetime.now.return_value = mock_now
        mock_datetime.fromisoformat = datetime.fromisoformat
        
        response = client.get('/health')
        
        # Verify datetime.now was called with BRAZIL_TZ
        mock_datetime.now.assert_called_with(tz=BRAZIL_TZ)


def test_error_returns_500(client):
    """Test that the error route returns 500 status code."""
    response = client.get('/error')
    assert response.status_code == 500


def test_error_returns_json(client):
    """Test that error route returns JSON response."""
    response = client.get('/error')
    data = response.get_json()
    
    assert data is not None
    assert isinstance(data, dict)


def test_error_returns_required_fields(client):
    """Test that error route returns required fields."""
    response = client.get('/error')
    data = response.get_json()
    
    assert 'status' in data
    assert 'message' in data


def test_error_status_is_error(client):
    """Test that error route returns status as 'error'."""
    response = client.get('/error')
    data = response.get_json()
    
    assert data['status'] == 'error'


def test_error_message_content(client):
    """Test that error route returns correct error message."""
    response = client.get('/error')
    data = response.get_json()
    
    assert data['message'] == 'An error occurred'

