""" Application Settings in Context """

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict
import yaml

from adjutant.context.exceptions import NoSettingsFileFound, SettingsFileCorrupt
from adjutant.context.version import V_MAJOR, V_MINOR, V_PATCH, V_STAGE

SETTINGS_FILE = Path(".") / "adjutant.yaml"


@dataclass
class SettingsContext:
    """Quick access to applicaiton settings"""

    version_string: str = ""
    font_size: int = 9

    def load(self) -> None:
        """Load from settings file"""
        settings: Dict[str, Any] = {}
        try:
            with SETTINGS_FILE.open("r") as stream:
                try:
                    settings = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    logging.error(exc)
                    raise SettingsFileCorrupt(
                        "The settings file is corrupted. Please take a copy and delete it."
                    ) from exc
        except IOError as exc:
            # File does not exist
            logging.info("Settings file '%s' not found", SETTINGS_FILE)
            raise NoSettingsFileFound from exc

        self.font_size = settings.get("font_size", self.font_size)
        self.version_string = f"{V_MAJOR}.{V_MINOR}.{V_PATCH}-{V_STAGE}"

    def save(self) -> None:
        """Save the settings to file"""
        settings: Dict[str, Any] = {}
        settings["font_size"] = self.font_size

        with SETTINGS_FILE.open("w") as outfile:
            yaml.dump(settings, outfile)
