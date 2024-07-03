"""
This module holds a small wrapper around monitoring the output of a subprocess.
It allows callbacks to be notified when a new line of output is available on
stdout or stderr.
"""

# Standard
from collections.abc import Callable
from io import TextIOWrapper
import shlex
import signal
import subprocess
import threading


class ProcessMonitor:
    __doc__ = __doc__

    _LINE_CALLBACK = Callable[[str], None]

    def __init__(
        self,
        command: str,
        stdout_callbacks: list[_LINE_CALLBACK] | None = None,
        stderr_callbacks: list[_LINE_CALLBACK] | None = None,
    ):
        self._command = command
        self._stdout_callbacks = stdout_callbacks or []
        self._stderr_callbacks = stderr_callbacks or []
        self._proc = None
        self._stdout_stream = None
        self._stderr_stream = None

    def __del__(self):
        self.stop()

    def register_callback(self, stream_type: str, callback: _LINE_CALLBACK):
        (
            self._stdout_callbacks
            if stream_type == "stdout"
            else self._stderr_callbacks
        ).append(callback)

    def start(self):
        """Start the process monitor and connect the callbacks"""

        # Start the process
        self._proc = subprocess.Popen(
            shlex.split(self._command),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Set up the stdout/stderr stream readers
        self._stdout_stream = TextIOWrapper(self._proc.stdout)
        self._stderr_stream = TextIOWrapper(self._proc.stderr)
        self._stdout_thread = threading.Thread(
            target=self._fill_stream_lines, args=("stdout",)
        )
        self._stderr_thread = threading.Thread(
            target=self._fill_stream_lines, args=("stderr",)
        )
        self._stdout_thread.start()
        self._stderr_thread.start()

    def stop(self):
        if self._proc is not None:
            self._proc.send_signal(signal.SIGINT)
            self._proc.wait(timeout=5)
            self._proc.terminate()
            self._stdout_stream.close()
            self._stderr_stream.close()

    def _fill_stream_lines(self, stream_type: str):
        stream = self._stdout_stream if stream_type == "stdout" else self._stderr_stream
        callbacks = (
            self._stdout_callbacks
            if stream_type == "stdout"
            else self._stderr_callbacks
        )
        while True:
            line = stream.readline()
            if not line:
                break
            line = line.rstrip("\n")
            for callback in callbacks:
                callback(line)
