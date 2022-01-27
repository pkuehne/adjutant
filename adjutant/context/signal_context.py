""" Context for all signals """


from PyQt6.QtCore import QModelIndex, QObject, pyqtSignal


class SignalContext(QObject):
    """Collects all pan-application signals"""

    show_add_base_dialog = pyqtSignal()
    show_edit_base_dialog = pyqtSignal(QModelIndex)
    tags_updated = pyqtSignal(QModelIndex)

    load_search = pyqtSignal(int)
    save_search = pyqtSignal()

    show_add_dialog = pyqtSignal(str, dict)
    show_edit_dialog = pyqtSignal(str, QModelIndex, dict)

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
