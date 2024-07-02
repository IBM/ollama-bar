"""
This module holds a rumps menu object that manages the display of an output
stream from a running ProcessMonitor.
"""

# Third Party
from AppKit import NSAppearance, NSMakeRect, NSMenuItem, NSTextField, NSUserDefaults
from rumps.rumps import NSApp
import rumps

# Local
from ollama_bar.process_monitor import ProcessMonitor


class CommandDisplayWindow:
    __doc__ = __doc__

    def __init__(
        self,
        stream_type: str = "stdout",
        process_monitor: ProcessMonitor | None = None,
        update_period: float = 0.5,
        max_lines: int = 20,
    ):
        self._stream_type = stream_type
        self._max_lines = max_lines
        self._lines = []

        # Set up the menu item with the text window
        self._text_container = NSTextField.alloc().initWithFrame_(
            NSMakeRect(0, 0, 100, 100)
        )
        if (
            NSUserDefaults.standardUserDefaults().stringForKey_("AppleInterfaceStyle")
            == "Dark"
        ):
            self._text_container.setAppearance_(
                NSAppearance.appearanceNamed_("NSAppearanceNameVibrantDark")
            )
        self._menuitem = NSMenuItem.alloc().init()
        self._menuitem.setTarget_(NSApp)
        self._menuitem.setView_(self._text_container)

        # Register the update callback
        if process_monitor is not None:
            process_monitor.register_callback(self._stream_type, self.add_line_callback)

        # Set up a timer to update the display
        rumps.timer(update_period)(self.update_output)

    def set_process(self, process_monitor: ProcessMonitor):
        self._lines = []
        process_monitor.register_callback(self._stream_type, self.add_line_callback)

    def add_line_callback(self, line: str):
        self._lines.append(line)
        if len(self._lines) > self._max_lines:
            self._lines.pop(0)

    def update_output(self, *_, **__):
        """Update the text window with the latest output."""
        display_out = "\n".join(self._lines)
        self._text_container.setStringValue_(display_out)
        self._text_container.sizeToFit()
