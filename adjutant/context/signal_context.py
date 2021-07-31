""" Context for all signals """


from PyQt6.QtCore import QModelIndex, QObject, pyqtSignal


class SignalContext(QObject):
    """Collects all pan-application signals"""

    show_add_base_dialog = pyqtSignal()
    show_edit_base_dialog = pyqtSignal(QModelIndex)
    tags_updated = pyqtSignal(QModelIndex)
    search_loaded = pyqtSignal()

    apply_filter = pyqtSignal(int, object)
    filter_by_id = pyqtSignal(list)

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
