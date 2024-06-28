# Standard
import os
import signal
import subprocess

# Third Party
import rumps

# import tempfile


class OllamaBarApp(rumps.App):
    """App to run ollama in the macos menu bar"""

    def __init__(self):
        super().__init__(
            name="ollama-bar",
            title="",
            icon=self._resource("ollama.png"),
        )
        self._ollama_server_proc = None
        # self._ollama_server_stdout = None
        # self._ollama_server_stderr = None

        self._on_icon = self._resource("on.svg")
        self._off_icon = self._resource("off.svg")
        self._menu.add(
            rumps.MenuItem("Start", icon=self._off_icon, callback=self._start_stop)
        )

    def __del__(self):
        self._start_stop()

    ##########
    ## Impl ##
    ##########

    _RESOURCE_ROOT = os.path.join(os.path.dirname(__file__), "resources")

    def _start_stop(self, sender: rumps.MenuItem | None) -> None:
        if self._ollama_server_proc is None:
            if sender is not None:
                sender.title = "Stop"
                sender.icon = self._on_icon
            # self._ollama_server_stdout = tempfile.TemporaryFile()
            # self._ollama_server_stderr = tempfile.TemporaryFile()
            self._ollama_server_proc = subprocess.Popen(
                [
                    "ollama",
                    "serve",
                ],  # stdout=self._ollama_server_stdout, stderr=self._ollama_server_stderr,
            )
        else:
            if sender is not None:
                sender.title = "Stop"
                sender.icon = self._off_icon
            self._ollama_server_proc.send_signal(signal.SIGINT)
            self._ollama_server_proc.wait()
            del self._ollama_server_stdout
            del self._ollama_server_stderr
            self._ollama_server_proc = None
            # self._ollama_server_stdout = None
            # self._ollama_server_stderr = None

    @classmethod
    def _resource(cls, name: str) -> str:
        return os.path.join(cls._RESOURCE_ROOT, name)


def main():
    OllamaBarApp().run()


if __name__ == "__main__":
    main()
