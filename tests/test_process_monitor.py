"""
Unit tests for ProcessMonitor
"""
# Standard
from unittest import mock

# Third Party
import pytest

# Local
from ollama_bar.process_monitor import ProcessMonitor


def test_process_monitor_stdout():
    """Test that ProcessMonitor can collect stdout iteratively"""
    cmd = "bash -c 'echo one; echo two'"
    pm = ProcessMonitor(cmd)
    collector = mock.MagicMock()
    pm.register_callback("stdout", collector)
    pm.start()
    pm._proc.wait()
    assert collector.call_count == 2
    assert [c.args for c in collector.call_args_list] == [("one",), ("two",)]
