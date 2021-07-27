""" Classes to manage database operations """


from typing import Any, List
from dataclasses import dataclass
from PyQt6.QtCore import QFile, QTextStream, qWarning
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from adjutant.context.settings_context import SettingsContext


@dataclass
class QueryBinding:
    placeholder: str
    value: Any


class DatabaseContext:
    """Manage connection to the database"""

    def __init__(self) -> None:
        self.database = QSqlDatabase.database()
        if not self.database.isValid():
            # Create the global database connection if one doesn't exist already
            self.database = QSqlDatabase.addDatabase("QSQLITE")

    def open_database(self, filename) -> None:
        """Open the database for operations"""
        if self.database.isOpen():
            self.database.close()

        self.database.setDatabaseName(filename)
        if not self.database.open():
            qWarning("Failed to open the database")
            return

    def version(self) -> int:
        """The version of the database"""
        result = self.execute_sql_command("SELECT version FROM settings", errors=False)
        if result is None:
            return 0
        result.first()
        version = result.value("version")
        return version

    def migrate(self, settings: SettingsContext) -> None:
        """Applies any outstanding migrations to the database"""
        if settings.database_version > self.version():
            self.execute_sql_file("resources/migrations/initial.sql")

    def execute_sql_command(
        self, command: str, bindings: List[QueryBinding] = None, errors: bool = True
    ) -> QSqlQuery:
        """Execute a SQL command"""
        bindings = bindings if bindings else []
        query = QSqlQuery(self.database)
        query.prepare(command)
        for binding in bindings:
            query.bindValue(binding.placeholder, binding.value)
        if not query.exec():
            if errors:
                qWarning(
                    "Failed to execute query. Error: "
                    + query.lastError().text()
                    + " Command: "
                    + command
                    + " Bindings: "
                    + str(bindings)
                )
            return None
        return query

    def execute_sql_file(self, filename: str) -> None:
        """Execute SQL statements in given file"""
        # qWarning(f"Executing {filename}")
        sql_file = QFile(filename)
        sql_file.open(QFile.OpenModeFlag.ReadOnly)

        for query in QTextStream(sql_file).readAll().split(";"):
            if not query.strip():
                # Ignore empty lines
                continue
            self.execute_sql_command(query)
