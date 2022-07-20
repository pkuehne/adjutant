""" Classes to manage database operations """

import logging
import uuid
from pathlib import Path
from typing import Any, List
from dataclasses import dataclass
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from adjutant.context.dataclasses import Tag
from adjutant.context.database_migrations import LATEST_DATABASE_VERSION, VERSION_1
from adjutant.context.exceptions import (
    DatabaseIsNewer,
    DatabaseNeedsMigration,
    NoDatabaseFileFound,
)

DATABASE_FILE = Path(".") / "adjutant.db"


def generate_uuid() -> str:
    """Generates a 36 char hex string that should be unique"""
    return str(uuid.uuid4())


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

    def open_database(self) -> None:
        """Open the database for operations"""
        if self.database.isOpen():
            self.database.close()

        self.database.setDatabaseName(str(DATABASE_FILE))
        if not self.database.open():
            logging.error("Failed to open database: %s", DATABASE_FILE)
            raise RuntimeError("Failed to open the database")
        if self.version() == 0:
            logging.info("Database version is 0")
            raise NoDatabaseFileFound()
        if LATEST_DATABASE_VERSION < self.version():
            # Newer database than application
            raise DatabaseIsNewer(
                f"Incompatible database version: {self.version()}! "
                + f"Adjutant can only handle: {LATEST_DATABASE_VERSION}."
            )
        if LATEST_DATABASE_VERSION > self.version():
            logging.info(
                "Database needs migration from %s to %s",
                self.version(),
                LATEST_DATABASE_VERSION,
            )
            raise DatabaseNeedsMigration()

        # Versions match

    def version(self) -> int:
        """The version of the database"""
        result = self.execute_sql_command("SELECT version FROM settings", errors=False)
        if result is None:
            return 0
        result.first()
        version = result.value("version")
        return version

    def migrate(self) -> None:
        """Applies any outstanding migrations to the database"""
        logging.info("Starting database migration")
        if self.version() < 1:
            # Migrate from version 0 to 1
            self.execute_sql_string(VERSION_1)
            self.execute_sql_command("INSERT into settings(version) VALUES(0);")
            for table in ["storages", "statuses", "step_operations", "colour_schemes"]:
                self.execute_sql_command(
                    f"INSERT INTO {table}(id, name) VALUES ('', '<None>');"
                )

        # Database migrated to latest version
        self.execute_sql_command(
            f"UPDATE settings SET version = {LATEST_DATABASE_VERSION}"
        )
        logging.info("Database migration complete")

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
                logging.warning(
                    "Failed to execute query. Error: %s Command: %s Bindings %s",
                    query.lastError().text(),
                    command,
                    str(bindings),
                )
            return None
        return query

    def execute_sql_string(self, commands: str) -> None:
        """Execute a list of commands separated by semi-colons"""
        for query in commands.split(";"):
            if not query.strip():
                # ignore empty lines
                continue
            self.execute_sql_command(query)


def remove_all_tags_for_base(context: DatabaseContext, base_id: int):
    """Remove all the tags for a given base"""
    query = "DELETE from bases_tags WHERE bases_id = :base_id;"
    bindings = [QueryBinding(":base_id", base_id)]
    result = context.execute_sql_command(query, bindings)
    if not result:
        logging.error("Failed to remove old tags for %s", base_id)


def add_tag_to_base(context: DatabaseContext, base_id: int, tag_id: int):
    """ "Add a tag usage for a given tag/base combination"""
    query = "INSERT INTO bases_tags VALUES(NULL, :base_id, :tag_id)"
    bindings = [QueryBinding(":base_id", base_id), QueryBinding(":tag_id", tag_id)]
    result = context.execute_sql_command(query, bindings)
    if not result:
        logging.error("Failed to associate tag %s to base %s", tag_id, base_id)


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
        logging.error(
            "Failed to retrieve the tags from the database for base: %s", base_id
        )
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
