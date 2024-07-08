"""
Unit tests to cover CommandDisplayWindow
"""
# Standard
from unittest import mock

# Local
from ollama_bar.command_display_window import CommandDisplayWindow
import ollama_bar.command_display_window as command_display_window


class MockProcessMonitor:
    def __init__(self):
        self.stdout_callbacks = []
        self.stderr_callbacks = []

    def trigger_stdout_callbacks(self, lines: list[str]):
        for callback in self.stdout_callbacks:
            callback(lines)

    def trigger_stderr_callbacks(self, lines: list[str]):
        for callback in self.stderr_callbacks:
            callback(lines)

    def register_callback(self, stream_type, callback):
        if stream_type == "stdout":
            self.stdout_callbacks.append(callback)
        elif stream_type == "stderr":
            self.stderr_callbacks.append(callback)


def test_command_display_window_stream_callbacks():
    """Test that the CommandDisplayWindow correctly registers and triggers
    callbacks for stdout and stderr streams.
    """
    mock_process_monitor = MockProcessMonitor()
    stdout_window = CommandDisplayWindow("stdout")
    stderr_window = CommandDisplayWindow("stderr")
    stdout_window.set_process(mock_process_monitor)
    stderr_window.set_process(mock_process_monitor)

    # Trigger a callback with some "stdout" lines
    stdout_lines = ["line1", "line2"]
    for line in stdout_lines:
        mock_process_monitor.trigger_stdout_callbacks(line)
    assert stdout_window._lines == stdout_lines
    assert not stderr_window._lines

    # Trigger a callback with some "stderr" lines
    stderr_lines = ["line3", "line4"]
    for line in stderr_lines:
        mock_process_monitor.trigger_stderr_callbacks(line)
    assert stdout_window._lines == stdout_lines
    assert stderr_window._lines == stderr_lines


def test_command_display_window_update_output():
    """Make sure that the text container gets updated correctly."""
    mock_process_monitor = MockProcessMonitor()
    window = CommandDisplayWindow()
    window.set_process(mock_process_monitor)
    stdout_lines = ["line1", "line2"]
    for line in stdout_lines:
        mock_process_monitor.trigger_stdout_callbacks(line)

    # Make sure the string value is not already set
    assert window._text_container.stringValue() == ""

    # Do the update and make sure it worked
    window.update_output()
    assert window._text_container.stringValue() == "\n".join(stdout_lines)


def test_command_display_window_max_lines():
    """Make sure the correct number of lines are kept."""
    max_lines = 2
    mock_process_monitor = MockProcessMonitor()
    window = CommandDisplayWindow(max_lines=max_lines)
    window.set_process(mock_process_monitor)
    stdout_lines = ["line1", "line2", "line3"]
    for line in stdout_lines:
        mock_process_monitor.trigger_stdout_callbacks(line)
    assert window._lines == stdout_lines[-max_lines:]


def test_command_display_window_dark_mode():
    """Make sure the dark mode is applied correctly.

    NOTE: This needs to do a lot of mocking to pass correctly both locally and
        on CI. The test simply validates that in dark mode, the setAppearance_
        method is called on the self._text_container object, but can't do more
        to validate that the call is actually correct.
    """
    with (
        mock.patch.object(
            command_display_window, "NSUserDefaults"
        ) as NSUserDefaults_patch,
        mock.patch.object(command_display_window, "NSTextField") as NSTextField_patch,
        mock.patch.object(command_display_window, "NSMenuItem"),
    ):
        text_container_mock = mock.MagicMock()
        NSTextField_patch.alloc().initWithFrame_.return_value = text_container_mock
        NSUserDefaults_patch.standardUserDefaults().stringForKey_.return_value = "Dark"
        mock_process_monitor = MockProcessMonitor()
        window = CommandDisplayWindow()
        window.set_process(mock_process_monitor)
        text_container_mock.setAppearance_.assert_called_once()
