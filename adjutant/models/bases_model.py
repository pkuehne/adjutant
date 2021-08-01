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
    select_query: str = None
    delete_query: str = None
    insert_query: str = None


@dataclass(eq=True, frozen=True)
class Tag:
    """Tag"""

    tag_id: int
    tag_name: str


class BasesModel(QSqlTableModel):
    """Subclass QSqlTableModel"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.m2m_relationships: List[ManyToManyRelationship] = []

    def set_many_to_many_relationship(self, rel: ManyToManyRelationship):
        """Adds a new many-to-many relationship"""
        self.m2m_relationships.append(rel)
        sts = self.tableName()
        tts = rel.target_table
        its = f"{sts}_{tts}"
        rel.select_query = f"""
            SELECT {tts}.id AS {tts}_id, {tts}.name AS {tts}_name 
            FROM {tts} 
            INNER JOIN {its} 
            ON {its}.{tts}_id = {tts}.id 
            WHERE {its}.{sts}_id = :source_id;
        """
        rel.delete_query = f"""
            DELETE FROM {its} WHERE {sts}_id = :source_id
        """
        rel.insert_query = f"""
            INSERT INTO {its} VALUES(NULL, :source_id, :target_id)
        """

    # def select(self) -> bool:
    #     """Reload all data from the database"""
    #     return super().select()

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        """Flags for the items"""
        if index.column() < super().columnCount():
            return super().flags(index)
        return super().flags(index.siblingAtColumn(0))

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
        sql.prepare(rel.select_query)
        sql.bindValue(":source_id", source_id)
        success = sql.exec()
        if not success:
            print(f"Failed to get values. Query: {rel.select_query}")
            return None
        tags = []
        values = []
        while sql.next():
            result_id = sql.value(f"{rel.target_table}_id")
            result_value = sql.value(f"{rel.target_table}_name")
            tags.append(Tag(result_id, result_value))
            values.append(result_value)
        return {
            Qt.ItemDataRole.DisplayRole: ",".join(values),
            Qt.ItemDataRole.EditRole: tags,
            Qt.ItemDataRole.SizeHintRole: len(",".join(values)),
            Qt.ItemDataRole.ToolTipRole: "\n".join(values),
        }.get(role, None)

    # pylint: disable=invalid-name
    def setData(
        self, index: QModelIndex, value, role: int = Qt.ItemDataRole.EditRole
    ) -> bool:
        """Update the data in the model"""
        if index.column() == 0:  # Ensure that id is always null
            return super().setData(index, None, role=role)
        if index.column() < super().columnCount():
            return super().setData(index, value, role=role)
        if role != Qt.ItemDataRole.EditRole:
            return False

        rel = self.m2m_relationships[index.column() - super().columnCount()]
        source_id = index.siblingAtColumn(0).data()
        sql = QSqlQuery()
        sql.prepare(rel.delete_query)
        sql.bindValue(":source_id", source_id)
        success = sql.exec()
        if not success:
            print(
                f"Failed to remove previous values. Query: {rel.delete_query} {source_id}"
            )
            return False

        tags: List[Tag] = value
        for tag in tags:
            sql.prepare(rel.insert_query)
            sql.bindValue(":source_id", source_id)
            sql.bindValue(":target_id", tag.tag_id)
            success = sql.exec()
            if not success:
                print(
                    f"Failed to insert value. Query: {rel.insert_query} {source_id}, {tag}"
                )
                return False
        return True

    def columnCount(self, _: QModelIndex = None) -> int:
        """Override for the column count"""
        return super().columnCount() + len(self.m2m_relationships)
