""" Context for all signals """


from PyQt6.QtCore import QModelIndex, QObject, pyqtSignal


class SignalContext(QObject):
    """Collects all pan-application signals"""

    show_add_base_dialog = pyqtSignal()
    show_edit_base_dialog = pyqtSignal(QModelIndex)
    tags_updated = pyqtSignal(QModelIndex)

    load_search = pyqtSignal(int)
    save_search = pyqtSignal()

    show_add_storage_dialog = pyqtSignal()
    show_edit_storage_dialog = pyqtSignal(QModelIndex)

    show_add_colour_dialog = pyqtSignal()
    show_edit_colour_dialog = pyqtSignal(QModelIndex)

    show_add_recipe_dialog = pyqtSignal()
    show_edit_recipe_dialog = pyqtSignal(QModelIndex)

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
