"""
This module supports capturing stdout and stderr from the main python process
"""

# Standard
from collections.abc import Callable
import io
import os
import sys
import threading


class OutputTeeBytesIO(io.BytesIO):
    """Overload of BytesIO to tee output to other streams"""

    def __init__(self, *streams):
        self.streams = list(streams)
        self.write_lock = threading.Lock()
        self._buffered_lines_content = b""
        super().__init__()

    def write(self, *args, **kwargs):
        with self.write_lock:
            here = self.tell()
            ret = super().write(*args, **kwargs)
            self.seek(here)
            content = self.read(ret)
            self._buffered_lines_content += content
        for stream in self.streams:
            stream.write(content)
        return ret

    def flush(self, *args, **kwargs):
        super().flush(*args, **kwargs)
        for stream in self.streams:
            stream.flush(*args, **kwargs)


class StreamLineBuffer:
    def __init__(self, line_callback):
        self._buffered_content = b""
        self._write_lock = threading.Lock()
        self.line_callback = line_callback

    def write(self, content):
        with self._write_lock:
            lines = (self._buffered_content + content).split(os.linesep.encode("utf-8"))
            ready_lines = lines[:-1]
            self._buffered_content = lines[-1]
        for line in ready_lines:
            self.line_callback(line.decode("utf-8"))

    def flush(self):
        pass


def capture_output(
    label: str, line_callback: Callable[[str], None]
) -> OutputTeeBytesIO:
    """Capture a single system output (stdout or stderr)"""
    tee = OutputTeeBytesIO(getattr(sys, label).buffer, StreamLineBuffer(line_callback))
    setattr(sys, label, io.TextIOWrapper(tee, encoding="utf-8"))
    return tee
