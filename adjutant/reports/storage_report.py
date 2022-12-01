""" PDF report for Storages"""

import logging
import html
from typing import List, Dict
from PyQt6.QtSql import QSqlRecord
from adjutant.reports.base_report import BaseReport, InputValues
from adjutant.context import Context


class StorageReport(BaseReport):
    """Report for storage locations """

    def __init__(self, context: Context, inputs: InputValues) -> None:
        super().__init__(context, inputs)

        self.title = "Storage Report"
        self.model = self.context.models.storages_model
        self.storages: List[QSqlRecord] = []
        self.bases: Dict[str, List[str]] = {}

    def prepare(self):
        """Prepare the report"""
        for row in range(self.model.rowCount()):
            self.storages.append(self.model.record(row))
        self.storages.sort(key=lambda r: r.field("name").value())

        for row in range(self.context.models.bases_model.rowCount()):
            record = self.context.models.bases_model.record(row)
            storage_id = record.field("storages_id").value() or ""
            name = record.field("name").value() or ""
            if storage_id not in self.bases:
                self.bases[storage_id] = []
            self.bases[storage_id].append(html.escape(name))

    def get_storage_contents(self, storage_id: str) -> str:
        """Retrieve all bases for the given storage"""
        logging.info("Called with %s", storage_id)
        if storage_id not in self.bases:
            logging.error(
                "Storage report has no storage: %s.\nAvailable keys: %s",
                storage_id,
                self.bases.keys(),
            )
            return ""
        content = "<ul>"
        for base in self.bases[storage_id]:
            content += f"<li>{html.escape(base)}</li>"
        content += "</ul>"
        return content

    def body(self) -> str:
        """Create the body of the report"""
        body = ""
        for storage in self.storages:
            name = storage.field("name").value()
            storage_id = storage.field("id").value()
            if storage_id == "":
                continue
            body += f"<h1>{html.escape(name)}</h1>"
            body += self.get_storage_contents(storage_id)
        body += "<h1>No Storage</h1>"
        body += self.get_storage_contents("")

        return body
