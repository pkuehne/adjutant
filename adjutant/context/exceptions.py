""" Exceptions raised in adjutant"""


class NoSettingsFileFound(RuntimeError):
    """Raised when no settings file is found"""


class NoDatabaseFileFound(RuntimeError):
    """Raised when no database file is found"""


class DatabaseNeedsMigration(RuntimeError):
    """Raised when the database version is behind application"""


class DatabaseIsNewer(RuntimeError):
    """Raised when the database is ahead of the application"""


class SettingsFileCorrupt(RuntimeError):
    """Raised when the settings file is corrupted somehow"""
