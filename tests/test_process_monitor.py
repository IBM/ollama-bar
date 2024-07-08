"""
Unit tests for ProcessMonitor
"""
# Standard
from unittest import mock

# Third Party
import pytest

# Local
from ollama_bar.process_monitor import ProcessMonitor


@pytest.mark.parametrize("stream_name", ["stdout", "stderr"])
def test_process_monitor_stdout(stream_name):
    """Test that ProcessMonitor can collect stdout iteratively"""
    redirect = "" if stream_name == "stdout" else "1>&2"
    cmd = f"bash -c 'echo one {redirect}; echo two {redirect}'"
    pm = ProcessMonitor(cmd)
    collector = mock.MagicMock()
    pm.register_callback(stream_name, collector)
    pm.start()
    pm._proc.wait()
    assert collector.call_count == 2
    assert [c.args for c in collector.call_args_list] == [("one",), ("two",)]
