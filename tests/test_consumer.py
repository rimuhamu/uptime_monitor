from unittest.mock import patch, MagicMock
from consumer.main import send_discord_alert
from consumer.consumer_db import save_to_db
from database import WebsiteStats

@patch('consumer.main.requests.post')
def test_send_discord_alert(mock_post):
    mock_post.return_value.status_code = 204

    data = {
        'url': 'https://example.com',
        'status_code': 500,
        'latency': 0.123,
        'error': 'Timeout',
        'timestamp': 1672531200
    }

    send_discord_alert(data)

    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    payload = kwargs['json']

    assert payload['username'] == 'Uptime Bot'
    assert len(payload['embeds']) == 1

    embed = payload['embeds'][0]
    assert "SERVER DOWN" in embed['title']
    assert embed['color'] == 15158332

    fields = {f['name']: f['value'] for f in embed['fields']}
    assert fields['Target URL'] == 'https://example.com'
    assert fields['Status Code'] == '500'
    assert fields['Error Message'] == 'Timeout'

@patch('consumer.consumer_db.SessionLocal')
def test_save_to_db(mock_session_cls, capsys):
    mock_session = MagicMock()
    mock_session_cls.return_value = mock_session

    data = {
        'url': 'https://example.com',
        'status_code': 200,
        'latency': 0.05
    }

    save_to_db(data)

    mock_session.add.assert_called_once()
    record = mock_session.add.call_args[0][0]

    assert isinstance(record, WebsiteStats)
    assert record.url == 'https://example.com'
    assert record.status_code == 200
    assert record.latency == 0.05

    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()

    captured = capsys.readouterr()
    assert "DB Saved: https://example.com" in captured.out


@patch('consumer.consumer_db.SessionLocal')
def test_save_to_db_error(mock_session_cls, capsys):
    mock_session = MagicMock()
    mock_session_cls.return_value = mock_session
    # Simulate a DB error
    mock_session.commit.side_effect = Exception("DB Connection Failed")

    data = {'url': 'http://fail.com', 'status_code': 200, 'latency': 0.0}

    save_to_db(data)

    mock_session.close.assert_called_once()

    captured = capsys.readouterr()
    assert "DB Error: DB Connection Failed" in captured.out