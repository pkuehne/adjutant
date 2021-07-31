""" Bases Model"""

from dataclasses import dataclass
from typing import List
from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel


@dataclass
class ManyToManyRelationship:
    """Defines a many-to-many relationship"""

    target_table: str
    target_field: int
    query: str = None


class BasesModel(QSqlTableModel):
    """Subclass QSqlTableModel"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.m2m_relationships: List[ManyToManyRelationship] = []

    def set_many_to_many_relationship(self, rel: ManyToManyRelationship):
        """Adds a new many-to-many relationship"""
        self.m2m_relationships.append(rel)
        if rel.query is not None:
            return
        sts = self.tableName()
        tts = rel.target_table
        its = f"{sts}_{tts}"
        rel.query = f"""
            SELECT {tts}.id AS {tts}_id, {tts}.name AS {tts}_name 
            FROM {tts} 
            INNER JOIN {its} 
            ON {its}.{tts}_id = {tts}.id 
            WHERE {its}.{sts}_id = :source_id;
        """

    # def select(self) -> bool:
    #     """Reload all data from the database"""
    #     return super().select()

    def columnCount(self, _: QModelIndex = None) -> int:  # pylint: disable=invalid-name
        """Override for the column count"""
        return super().columnCount() + len(self.m2m_relationships)

    def data(self, idx: QModelIndex, role: int):
        """Return many-to-many relationships as well"""
        if idx.column() < super().columnCount():
            return super().data(idx, role=role)

        if role not in [
            Qt.ItemDataRole.DisplayRole,
            Qt.ItemDataRole.EditRole,
            Qt.ItemDataRole.SizeHintRole,
            Qt.ItemDataRole.ToolTipRole,
        ]:
            return None

        rel = self.m2m_relationships[idx.column() - super().columnCount()]
        source_id = idx.siblingAtColumn(0).data()
        sql = QSqlQuery()
        sql.prepare(rel.query)
        sql.bindValue(":source_id", source_id)
        success = sql.exec()
        if not success:
            print(f"Failed to get values. Query: {rel.query}")
            return None
        ids = []
        values = []
        while sql.next():
            ids.append(sql.value(f"{rel.target_table}_id"))
            values.append(sql.value(f"{rel.target_table}_name"))
        return {
            Qt.ItemDataRole.DisplayRole: ",".join(values),
            Qt.ItemDataRole.EditRole: ids,
            Qt.ItemDataRole.SizeHintRole: len(",".join(values)),
            Qt.ItemDataRole.ToolTipRole: "\n".join(values),
        }.get(role, None)

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        """Flags for the items"""
        if index.column() < super().columnCount():
            return super().flags(index)
        return super().flags(index.siblingAtColumn(0))
