"""
Unit tests for the OpenWebUIWrapper

NOTE: These tests only cover portions of the wrapper that are not covered by the
    main app tests
"""
# Standard
import time

# Third Party
from tls_test_tools import open_port
import requests

# Local
from ollama_bar.webui import OpenWebUIWrapper


def test_webui_start_stop():
    """Make sure that the Open WebUI server starts and stops correctly"""
    port = open_port()
    wrapper = OpenWebUIWrapper(port=port)
    assert not wrapper.server.started

    started = False
    try:

        # Start the wrapper
        wrapper.start()

        # Make sure it comes up
        start_time = time.time()
        max_startup_time = 3
        while time.time() - start_time < max_startup_time:
            time.sleep(0.01)
            if (
                wrapper.server.started
                and requests.get(f"http://localhost:{port}/health").ok
            ):
                started = True
                break

    finally:
        wrapper.stop()
        assert not wrapper.server_thread.is_alive()

    # Make sure it did start up successfully
    assert started
