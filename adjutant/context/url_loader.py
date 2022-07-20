"""Convenience class to load arbitrary url"""

import logging
import urllib.request
from urllib.error import URLError
from PyQt6.QtCore import QThread, pyqtSignal


class UrlLoader(QThread):
    """Loads a URL asynchronously"""

    content_loaded = pyqtSignal(str)

    def __init__(self, parent, url: str) -> None:
        super().__init__(parent)
        self.url = url

    def run(self) -> None:
        """Execute the url loading"""
        logging.debug("Retrieving %s", self.url)
        try:
            with urllib.request.urlopen(self.url) as html:
                logging.debug("Url loaded, sending content")
                self.content_loaded.emit(html.read().decode("utf-8"))
        except URLError as exc:
            logging.error("Failed to load %s: %s", self.url, exc.reason)
