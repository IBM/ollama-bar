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
    app._run_webui = False
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


@pytest.mark.parametrize("do_start", [True, False])
def test_ollama_bar_stop_on_delete(subprocess_popen_mock, do_start):
    """Test that the app stops when it's deleted IFF it was started"""
    app = OllamaBarApp()
    app._run_webui = False
    if do_start:
        app._start_stop(None)
    with mock.patch.object(app, "_start_stop") as start_stop:
        app.__del__()
        start_stop.called == do_start


def test_ollama_bar_toggle_webui(subprocess_popen_mock):
    """Test that toggling open webui on/off correctly recreates the wrapper and
    toggles the icons
    """
    app = OllamaBarApp()
    with (
        mock.patch("ollama_bar.webui.OpenWebUIWrapper.start") as webui_start_mock,
        mock.patch("ollama_bar.webui.OpenWebUIWrapper.stop") as webui_stop_mock,
    ):
        app._start_stop(None)
        webui_start_mock.assert_called_once()
        webui_stop_mock.assert_not_called()

        # Toggle the webui while the app is running. Make sure it gets stopped
        menu_mock = mock.MagicMock()
        app._toggle_webui(menu_mock)
        webui_stop_mock.assert_called_once()
        assert menu_mock.icon is app._off_icon

        # Toggle it back on and make sure start was re-called
        app._toggle_webui(menu_mock)
        assert len(webui_start_mock.mock_calls) == 2
        assert menu_mock.icon is app._on_icon

        # Turn off the main toggle and make sure the webui gets stopped
        app._start_stop(None)
        assert len(webui_stop_mock.mock_calls) == 2
