"""
This module supports running Open WebUI
"""
# Standard
import os
import pathlib
import threading

# Third Party
import uvicorn


class OpenWebUIWrapper:
    """Wrapper to run Open WebUI in a thread with graceful shutdown"""

    def __init__(self, host: str = "localhost", port: int = 8080):
        """Initialize with host and port

        NOTE: host defaults to 'localhost' to disallow external traffic
        """

        # Update the env to run without auth and to place the data in the user's
        # home directory. Note that this does not actually change the
        # environment, but it does change all places that the later code reads
        # from the env.
        data_dir = pathlib.Path.home() / ".open_webui"
        data_dir.mkdir(parents=True, exist_ok=True)
        os.environ.update({"WEBUI_AUTH": "False", "DATA_DIR": str(data_dir)})

        # Third Party
        # NOTE: The Open WebUI package installs a standalone module main.py in
        #   the base of site-packages based on how it's packaged. This is not
        #   ideal since it could conflict with any other package that does the
        #   same thing, but since this is an encapsulated environment, it's also
        #   not a problem.
        from main import app as open_webui_app

        self.server_config = uvicorn.Config(open_webui_app, host=host, port=port)
        self.server = uvicorn.Server(self.server_config)
        self.server_thread = threading.Thread(target=self.server.run)

    def start(self):
        self.server_thread.start()

    def stop(self):
        self.server.should_exit = True
        self.server_thread.join()
