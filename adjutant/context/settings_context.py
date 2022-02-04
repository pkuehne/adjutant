""" Application Settings in Context """


class SettingsContext:
    """Quick access to applicaiton settings"""

    def __init__(self) -> None:
        self.version_string = ""
        self.version_number = ""
        self.version_major = 0
        self.version_minor = 0
        self.version_patch = 0
        self.version_stage = ""
        # self.database_version = 0

    def set_version(self, version_string: str) -> None:
        """parse version string into major/minor/patch"""
        self.version_string = version_string
        parts = self.version_string.split("-")
        self.version_number = parts[0]
        if len(parts) > 1:
            self.version_stage = parts[1]

        (major, minor, patch) = self.version_number.split(".")
        self.version_major = int(major)
        self.version_minor = int(minor)
        self.version_patch = int(patch)
