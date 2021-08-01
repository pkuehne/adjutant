""" Tests for the sidebar model"""

from PyQt6.QtCore import QModelIndex
from PyQt6.QtSql import QSqlTableModel
from adjutant.models.sidebar_model import Section, SidebarModel


def test_model_valid(qtmodeltester):
    """Check that the model is generally valid"""
    # Given
    model = SidebarModel()
    searches = QSqlTableModel()

    model.add_section(Section("Foo", None, "", None))
    model.add_section(Section("Searches", searches, "", None))

    # Then
    qtmodeltester.check(model)


def test_all_value():
    """Test that the (0,0) index returns All"""
    # Given
    model = SidebarModel()
    model.add_section(Section("All", None, "", None))

    # Then
    assert model.index(0, 0, QModelIndex()).data() == "All"


def test_all_has_no_children():
    """The 'All' entry shouldn't have any children"""
    # Given
    model = SidebarModel()
    model.add_section(Section("Foo", None, "", None))

    # Then
    assert model.hasChildren(model.index(0, 0, QModelIndex())) is False
