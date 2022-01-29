""" Classes to manage database operations """

from os import path
from typing import Any, List
from dataclasses import dataclass
from PyQt6.QtCore import QFile, QTextStream, qWarning
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from adjutant.context.settings_context import SettingsContext
from adjutant.context.dataclasses import Tag


@dataclass
class QueryBinding:
    """Query Binding"""

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
            self.execute_sql_file("migrations/initial.sql")

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
        resources_path = path.abspath(
            path.join(path.dirname(__file__), "../../resources/")
        )
        sql_file = QFile(resources_path + "/" + filename)
        sql_file.open(QFile.OpenModeFlag.ReadOnly)

        for query in QTextStream(sql_file).readAll().split(";"):
            if not query.strip():
                # Ignore empty lines
                continue
            self.execute_sql_command(query)


def remove_all_tags_for_base(context: DatabaseContext, base_id: int):
    """Remove all the tags for a given base"""
    query = "DELETE from bases_tags WHERE bases_id = :base_id;"
    bindings = [QueryBinding(":base_id", base_id)]
    result = context.execute_sql_command(query, bindings)
    if not result:
        print("Failed to remove old tags")


def add_tag_to_base(context: DatabaseContext, base_id: int, tag_id: int):
    """ "Add a tag usage for a given tag/base combination"""
    query = "INSERT INTO bases_tags VALUES(NULL, :base_id, :tag_id)"
    bindings = [QueryBinding(":base_id", base_id), QueryBinding(":tag_id", tag_id)]
    result = context.execute_sql_command(query, bindings)
    if not result:
        print("Failed to associate tag to base")


def get_tags_for_base(context: DatabaseContext, base_id: int) -> List[Tag]:
    """Returns all tags for a given base ID"""
    query = """
        SELECT tags.id AS tag_id, tags.name AS tag_name 
        FROM tags 
        INNER JOIN bases_tags 
        ON bases_tags.tags_id = tags.id 
        WHERE bases_tags.bases_id = :base_id;
        """
    bindings = [QueryBinding(":base_id", base_id)]
    result: QSqlQuery = context.execute_sql_command(query, bindings)
    if not result:
        print("Failed to retrieve the tags from the database")
        return []

    tags = []
    while result.next():
        tag_id = result.value("tag_id")
        tag_name = result.value("tag_name")
        tags.append(Tag(tag_id, tag_name))
    return tags


def get_bases_for_tag(context: DatabaseContext, tag_id: int) -> List[int]:
    """Return a list of bases that have the given tag applied"""
    query = """
        SELECT bases.id as base_id
        FROM bases
        INNER JOIN bases_tags
        ON bases_tags.bases_id = bases.id
        WHERE bases_tags.tags_id = :tag_id;
    """
    bindings = [QueryBinding(":tag_id", tag_id)]
    result: QSqlQuery = context.execute_sql_command(query, bindings)
    if not result:
        return []
    bases = []
    while result.next():
        bases.append(result.value("base_id"))
    return bases


def get_tag_count(context: DatabaseContext, tag_id: int) -> int:
    """Returns a count of how many times the given tag is used"""
    query = """
        SELECT count(*) cnt
        FROM bases_tags
        WHERE tags_id = :tag_id;
    """
    bindings = [QueryBinding(":tag_id", tag_id)]
    result: QSqlQuery = context.execute_sql_command(query, bindings)
    if not result:
        return 0
    result.next()
    return result.value("cnt")


def remove_scheme_components(context: DatabaseContext, scheme_id: int) -> bool:
    """Remove all components for the given colour scheme"""
    query = """
        DELETE FROM scheme_components
        WHERE schemes_id = :schemes_id
    """
    bindings = [QueryBinding(":schemes_id", scheme_id)]
    result: QSqlQuery = context.execute_sql_command(query, bindings)
    return bool(result)
