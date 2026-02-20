import pytest
import requests
from simple_http_checker.checker import check_urls

def test_check_urls_success(mocker):
    mock_requests_get = mocker.patch('simple_http_checker.checker.requests.get')
    mock_response = mocker.MagicMock()
    mock_response.ok = True
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mock_requests_get.return_value = mock_response

    urls = ["http://example.com"]
    result = check_urls(urls)

    mock_requests_get.assert_called_once_with(urls[0], timeout=5)
    assert result[urls[0]] == "200 OK"

def test_check_urls_error(mocker):
    mock_requests_get = mocker.patch('simple_http_checker.checker.requests.get')
    mock_response = mocker.MagicMock()
    mock_response.ok = False
    mock_response.status_code = 404
    mock_response.reason = "Not Found"
    mock_requests_get.return_value = mock_response

    urls = ["http://example.com/nonexistent"]
    result = check_urls(urls)

    mock_requests_get.assert_called_once_with(urls[0], timeout=5)
    assert result[urls[0]] == "Error: HTTP 404 Not Found"

@pytest.mark.parametrize(
        "exception, expected_status", 
        [
            (requests.exceptions.Timeout, "Error: Timeout"),
            (requests.exceptions.ConnectionError("Connection failed"), "Error: Connection failed"),
            (requests.exceptions.RequestException("General error"), "Error: General error")
        ]
)
def test_check_urls_exceptions(mocker, exception, expected_status):
    mock_requests_get = mocker.patch('simple_http_checker.checker.requests.get')
    mock_requests_get.side_effect = exception

    urls = ["http://problem.com"]
    result = check_urls(urls)

    mock_requests_get.assert_called_once_with(urls[0], timeout=5)
    assert result[urls[0]] == expected_status

def test_check_urls_with_timeout(mocker):
    mock_requests_get = mocker.patch('simple_http_checker.checker.requests.get')
    mock_response = mocker.MagicMock()
    mock_response.ok = True
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mock_requests_get.return_value = mock_response

    urls = ["http://example.com"]
    timeout = 10
    result = check_urls(urls, timeout=timeout)

    mock_requests_get.assert_called_once_with(urls[0], timeout=timeout)
    assert result[urls[0]] == "200 OK"

def test_check_urls_with_multiple_urls(mocker):
    mock_requests_get = mocker.patch('simple_http_checker.checker.requests.get')

    def side_effect(url, timeout):
        if url == "http://example.com":
            mock_response = mocker.MagicMock()
            mock_response.ok = True
            mock_response.status_code = 200
            mock_response.reason = "OK"
            return mock_response
        else:
            raise requests.exceptions.ConnectionError("Connection failed")

    mock_requests_get.side_effect = side_effect

    urls = ["http://example.com", "http://problem.com"]
    result = check_urls(urls)

    assert mock_requests_get.call_count == 2
    assert result["http://example.com"] == "200 OK"
    assert result["http://problem.com"] == "Error: Connection failed"