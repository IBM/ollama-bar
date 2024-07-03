"""
Unit tests for the OllamaBarApp
"""
# Standard
from unittest import mock

# Third Party
import pytest

# Local
from ollama_bar.ollama_bar_app import OllamaBarApp


@pytest.fixture
def subprocess_popen_mock():
    with mock.patch("subprocess.Popen") as subprocess_popen:
        yield subprocess_popen


def test_ollama_bar_app_start_stop(subprocess_popen_mock):
    """Test that the app initializes stopped, and can toggle through start/stop"""
    app = OllamaBarApp()
    assert not app.running

    # Start the app and make sure it's running
    sender_mock = mock.MagicMock()
    app._start_stop(sender_mock)
    assert app.running
    assert sender_mock.title == "Stop"
    assert sender_mock.icon == app._on_icon

    # Stop the app and make sure it's not running
    app._start_stop(sender_mock)
    assert not app.running
    assert sender_mock.title == "Start"
    assert sender_mock.icon == app._off_icon
