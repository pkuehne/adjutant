""" Bases Model"""

from typing import Dict, List
from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtSql import QSqlQuery, QSqlTableModel
from adjutant.context.dataclasses import (
    OneToManyRelationship,
    ManyToManyRelationship,
    Tag,
)
from adjutant.context.database_context import (
    DatabaseContext,
    add_tag_to_base,
    get_tags_for_base,
    remove_all_tags_for_base,
)


class RelationalModel(QSqlTableModel):
    """Subclass QSqlTableModel"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.m2m_relationships: List[ManyToManyRelationship] = []
        self.o2m_relationships: Dict[int, OneToManyRelationship] = {}
        self.boolean_fields = []
        self.db_context = DatabaseContext()

    def set_many_to_many_relationship(self, rel: ManyToManyRelationship):
        """Adds a new many-to-many relationship"""
        self.m2m_relationships.append(rel)

    def set_one_to_many_relationship(self, field: int, rel: OneToManyRelationship):
        """Adds a relationship for a given field"""
        self.o2m_relationships[field] = rel

    # def select(self) -> bool:
    #     """Reload all data from the database"""
    #     return super().select()

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        """Flags for the items"""
        if index.column() < super().columnCount():
            return super().flags(index)
        return super().flags(index.siblingAtColumn(0))

    def _data_m2m(self, idx: QModelIndex, role: int):
        """many to many relationship data() call handling"""
        if role not in [
            Qt.ItemDataRole.DisplayRole,
            Qt.ItemDataRole.EditRole,
            Qt.ItemDataRole.SizeHintRole,
            Qt.ItemDataRole.ToolTipRole,
        ]:
            return None

        source_id = idx.siblingAtColumn(0).data()
        values = get_tags_for_base(self.db_context, source_id)
        names = [value.tag_name for value in values]
        return {
            Qt.ItemDataRole.DisplayRole: ",".join(names),
            Qt.ItemDataRole.EditRole: values,
            Qt.ItemDataRole.SizeHintRole: len(",".join(names)),
            Qt.ItemDataRole.ToolTipRole: "\n".join(names),
        }.get(role, None)

    def _data_o2m(self, idx: QModelIndex, role: int):
        """One to many relationship data() call handling"""
        foreign_key = super().data(idx, role)
        if role == Qt.ItemDataRole.EditRole:
            return foreign_key
        if foreign_key is None:
            return None
        relationship = self.o2m_relationships[idx.column()]
        query = f"""
            SELECT {relationship.target_field} 
            FROM {relationship.target_table}
            WHERE {relationship.target_key} == {foreign_key}
        """
        sql = QSqlQuery()
        sql.prepare(query)
        success = sql.exec()
        if not success:
            print(f"Failed to get value. Query: {query}")
            return None
        sql.next()
        return sql.value(relationship.target_field)

    def _data_boolean(self, idx, role: int):
        """Boolean field handling"""
        value = super().data(idx, role=role)
        if role == Qt.ItemDataRole.DisplayRole:
            return "Yes" if value == 1 else "No"
        return value

    def data(self, idx: QModelIndex, role: int):
        """Return many-to-many relationships as well"""
        if idx.column() >= super().columnCount():
            return self._data_m2m(idx, role)

        if idx.column() in self.o2m_relationships:
            return self._data_o2m(idx, role)

        if idx.column() in self.boolean_fields:
            return self._data_boolean(idx, role)

        return super().data(idx, role=role)

    def _set_data_o2m(self, index: QModelIndex, value, role: Qt.ItemDataRole) -> bool:
        """One to many relationship column setting"""
        return super().setData(index, value, role)

    def _set_data_m2m(self, index: QModelIndex, value, role: Qt.ItemDataRole) -> bool:
        """Many to many relationship column"""
        if role != Qt.ItemDataRole.EditRole:
            print("Don't set anything other than EditRole")
            return False

        source_id = index.siblingAtColumn(0).data()
        remove_all_tags_for_base(self.db_context, source_id)
        tags: List[Tag] = value
        for tag in tags:
            add_tag_to_base(self.db_context, source_id, tag.tag_id)
        return True

    # pylint: disable=invalid-name
    def setData(
        self, index: QModelIndex, value, role: int = Qt.ItemDataRole.EditRole
    ) -> bool:
        """Update the data in the model"""
        if index.column() == 0:  # Ensure that id is always null
            return True  # Don't update anything, key columns can't be changed

        if index.column() >= super().columnCount():
            return self._set_data_m2m(index, value, role)
        if index.column() in self.o2m_relationships:
            return self._set_data_o2m(index, value, role)

        return super().setData(index, value, role=role)

    def columnCount(self, _: QModelIndex = None) -> int:
        """Override for the column count"""
        return super().columnCount() + len(self.m2m_relationships)
