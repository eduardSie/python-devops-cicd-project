from click.testing import CliRunner
from simple_http_checker.cli import main

def test_cli_no_urls():
    runner = CliRunner()
    result = runner.invoke(main, [])
    assert result.exit_code == 0
    assert "" in result.output

def test_cli_with_urls(mocker):
    mock_check_urls = mocker.patch('simple_http_checker.cli.check_urls')
    mock_check_urls.return_value = {
        "http://example.com": "200 OK",
        "http://example.com/notfound": "Error: HTTP 404 Not Found"
    }

    runner = CliRunner()
    result = runner.invoke(main, ["http://example.com", "http://example.com/notfound"])
    
    assert result.exit_code == 0
    assert "http://example.com: 200 OK" in result.output
    assert "http://example.com/notfound: Error: HTTP 404 Not Found" in result.output

def test_cli_with_timeout(mocker):
    mock_check_urls = mocker.patch('simple_http_checker.cli.check_urls')
    mock_check_urls.return_value = {
        "http://example.com": "Error: Timeout"
    }

    runner = CliRunner()
    result = runner.invoke(main, ["http://example.com", "--timeout", "10"])
    
    assert result.exit_code == 1
    mock_check_urls.assert_called_once_with(["http://example.com"], timeout=10)
    assert "Timeout" in result.output