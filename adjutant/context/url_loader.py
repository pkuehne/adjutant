"""Convenience class to load arbitrary url"""

import logging
from threading import Thread
from typing import List
import urllib.request
from urllib.error import URLError
import yaml
from yaml.scanner import ScannerError
from yaml.parser import ParserError
from PyQt6.QtCore import QThread, pyqtSignal


def parse_yaml(content: str) -> dict:
    """Parses the content as yaml and returns it"""
    yaml_data = {}
    try:
        yaml_data = yaml.safe_load(content)
    except (ScannerError, ParserError) as exc:
        logging.error(
            "Failed to parse data:\n%s\n%s",
            exc.problem,
            exc.problem_mark,
        )
    return yaml_data


class UrlLoader(QThread):
    """Loads a URL asynchronously\n
    Usage:
        thread = UrlLoader(self, "https://google.com/")
        thread.content_loaded.connect(lambda content: print(content))
        thread.finished.connect(thread.deleteLater)
        thread.start()
    """

    content_loaded = pyqtSignal(str)
    workers: List[Thread] = []

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

    @classmethod
    def load_url(cls, url: str, callback):
        """Loads the specified URL"""
        thread = UrlLoader(None, url)
        thread.content_loaded.connect(callback)
        thread.finished.connect(thread.deleteLater)
        thread.start()
        cls.workers.append(thread)

    @classmethod
    def load_yaml_from_url(cls, url: str, callback):
        """Loads yaml from the URL"""
        cls.load_url(url, lambda yaml_data: callback(parse_yaml(yaml_data)))
