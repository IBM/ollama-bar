# Standard
import os
import pathlib
import sys

# Third Party
import rumps

# Local
from ollama_bar.command_display_window import CommandDisplayWindow
from ollama_bar.process_monitor import ProcessMonitor


class OllamaBarApp(rumps.App):
    """App to run ollama in the macos menu bar"""

    def __init__(self):
        super().__init__(
            name="ollama-bar",
            title="",
            icon=self._resource("ollama.png"),
        )
        # Add start/stop menu
        self._on_icon = self._resource("on.svg")
        self._off_icon = self._resource("off.svg")
        self._menu.add(
            rumps.MenuItem(
                "Start", icon=self._off_icon, callback=self._start_stop_ollama
            )
        )
        self._menu.add(None)

        # Add the output displays
        self._ollama_cmd = "ollama serve"
        self._setup_process_menu_items(self._menu)
        self._menu.add(None)

        # Add the options for Open WebUI
        self._open_webui_cmd = (
            "{} -c 'import open_webui; open_webui.serve(host=\"localhost\")'".format(
                sys.executable
            )
        )
        self._open_webui_menu = rumps.MenuItem("Open WebUI")
        self._open_webui_menu.add(
            rumps.MenuItem(
                "Start", icon=self._off_icon, callback=self._start_stop_webui
            )
        )
        self._setup_process_menu_items(self._open_webui_menu, "open_webui")
        self._menu.add(self._open_webui_menu)
        self._menu.add(None)

        # Placeholder for the running processes
        self._ollama_server_proc = None
        self._open_webui_proc = None

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

    def _start_stop_ollama(self, sender: rumps.MenuItem | None):
        self._ollama_server_proc = self._start_stop(
            self._ollama_cmd,
            self._ollama_server_proc,
            self._stdout_window,
            self._stderr_window,
            sender,
        )

    def _start_stop_webui(self, sender: rumps.MenuItem | None):
        data_dir = pathlib.Path.home() / ".open_webui"
        data_dir.mkdir(parents=True, exist_ok=True)
        env = os.environ.copy()
        env.update({"WEBUI_AUTH": "false", "DATA_DIR": data_dir})
        self._open_webui_proc = self._start_stop(
            self._open_webui_cmd,
            self._open_webui_proc,
            self._open_webui_stdout_window,
            self._open_webui_stderr_window,
            sender,
            env=env,
        )

    def _start_stop(
        self,
        command: str,
        proc: ProcessMonitor | None,
        stdout_window: CommandDisplayWindow,
        stderr_window: CommandDisplayWindow,
        sender: rumps.MenuItem | None,
        **kwargs,
    ) -> ProcessMonitor | None:
        if proc is None:
            if sender is not None:
                sender.title = "Stop"
                sender.icon = self._on_icon
            proc = ProcessMonitor(command, **kwargs)
            stdout_window.set_process(proc)
            stderr_window.set_process(proc)
            proc.start()
        else:
            if sender is not None:
                sender.title = "Start"
                sender.icon = self._off_icon
            proc.stop()
            proc = None
        return proc

    def _enable_disable_webui(self, sender: rumps.MenuItem | None) -> None:
        """Enable/disable the open WebUI based on the button click"""

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
