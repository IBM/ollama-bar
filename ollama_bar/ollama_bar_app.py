# Standard
import os

# Third Party
import rumps

# Local
from ollama_bar.command_display_window import CommandDisplayWindow
from ollama_bar.output_capture import capture_output
from ollama_bar.process_monitor import ProcessMonitor
from ollama_bar.webui import OpenWebUIWrapper


class OllamaBarApp(rumps.App):
    """App to run ollama in the macos menu bar"""

    def __init__(self):
        super().__init__(
            name="ollama-bar",
            title="",
            icon=self._resource("ollama.png"),
        )
        self._run_webui = True

        # Add start/stop menu
        self._on_icon = self._resource("on.svg")
        self._off_icon = self._resource("off.svg")
        self._menu.add(
            rumps.MenuItem("Start", icon=self._off_icon, callback=self._start_stop)
        )
        self._menu.add(None)

        # Add the output displays
        self._ollama_cmd = "ollama serve"
        self._setup_process_menu_items(self._menu)
        self._menu.add(None)

        # Pipe all stdout and stderr from the main python process to the output
        # window along with the output of the ollama subprocess
        self._stdout_cap = capture_output(
            "stdout", self._stdout_window.add_line_callback
        )
        self._stderr_cap = capture_output(
            "stderr", self._stderr_window.add_line_callback
        )

        # Add a toggle to enable/disable Open WebUI
        self._menu.add(
            rumps.MenuItem(
                "Open WebUI", icon=self._on_icon, callback=self._toggle_webui
            )
        )

        # Placeholder for the running processes/threads
        self._ollama_server_proc = None
        self._open_webui_wrapper = None

    def __del__(self):
        if self.running:
            self._start_stop(None)

    @property
    def running(self) -> bool:
        return self._ollama_server_proc is not None

    ##########
    ## Impl ##
    ##########

    _RESOURCE_ROOT = os.path.join(os.path.dirname(__file__), "resources")

    def _start_stop(self, sender: rumps.MenuItem | None, **kwargs):
        if self._ollama_server_proc is None:
            if sender is not None:
                sender.title = "Stop"
                sender.icon = self._on_icon
            self._ollama_server_proc = ProcessMonitor(self._ollama_cmd, **kwargs)
            self._stdout_window.set_process(self._ollama_server_proc)
            self._stderr_window.set_process(self._ollama_server_proc)
            self._ollama_server_proc.start()
            if self._run_webui:
                self._open_webui_wrapper = OpenWebUIWrapper()
                self._open_webui_wrapper.start()
        else:
            if sender is not None:
                sender.title = "Start"
                sender.icon = self._off_icon
            self._ollama_server_proc.stop()
            self._ollama_server_proc = None
            if self._open_webui_wrapper is not None:
                self._open_webui_wrapper.stop()

    def _toggle_webui(self, sender: rumps.MenuItem):
        if self._run_webui:
            self._run_webui = False
            sender.icon = self._off_icon
            if self._open_webui_wrapper is not None:
                self._open_webui_wrapper.stop()
                self._open_webui_wrapper = None
        else:
            self._run_webui = True
            sender.icon = self._on_icon
            if self._ollama_server_proc is not None:
                self._open_webui_wrapper = OpenWebUIWrapper()
                self._open_webui_wrapper.start()

    def _setup_process_menu_items(self, parent: rumps.MenuItem, label: str = ""):
        """Helper to encapsulate adding menu items to manage stdout/stderr for
        a process
        """
        stdout_window = CommandDisplayWindow("stdout")
        stdout_menu = rumps.MenuItem("stdout")
        stdout_menu.add(stdout_window)
        stderr_window = CommandDisplayWindow("stderr")
        stderr_menu = rumps.MenuItem("stderr")
        stderr_menu.add(stderr_window)

        label_pfx = "_" if not label else f"_{label}_"
        setattr(self, f"{label_pfx}stdout_window", stdout_window)
        setattr(self, f"{label_pfx}stderr_window", stderr_window)
        parent.add(stdout_menu)
        parent.add(stderr_menu)

    @classmethod
    def _resource(cls, name: str) -> str:
        return os.path.join(cls._RESOURCE_ROOT, name)
