import pytest
from datetime import timedelta

import requests

from producer import get_website_status
from unittest.mock import patch, Mock

@patch('requests.get')
@pytest.mark.parametrize("url, status_code, latency",[
    ("https://google.com", 200, 0.5),
    ("https://httpstat.us/404", 404, 0.1),
    ("https://mysite.com/down", 503, 0.0)
])
def test_website_status_logic(mock_get, url, status_code, latency):
    mock_response = Mock()
    mock_response.status_code = status_code
    mock_response.elapsed= timedelta(seconds=latency)
    mock_get.return_value = mock_response

    result = get_website_status(url)

    assert result['url'] == url
    assert result['status_code'] == status_code
    assert result['latency'] == latency

@patch('requests.get')
def test_website_connection_error(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError("ConnectionError")

    result = get_website_status("https://broken-link.com")

    assert result['url'] == "https://broken-link.com"
    assert result['status_code'] == 0
    assert "ConnectionError" in result['error']