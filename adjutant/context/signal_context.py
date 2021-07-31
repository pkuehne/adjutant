""" Context for all signals """


from PyQt6.QtCore import QModelIndex, QObject, pyqtSignal


class SignalContext(QObject):
    """Collects all pan-application signals"""

    show_add_base_dialog = pyqtSignal()
    show_edit_base_dialog = pyqtSignal(QModelIndex)

    delete_base = pyqtSignal(QModelIndex)
    delete_bases = pyqtSignal(list)
    duplicate_base = pyqtSignal(QModelIndex, int)
    update_bases = pyqtSignal()
    tags_updated = pyqtSignal(QModelIndex)

    save_search = pyqtSignal()
    load_search = pyqtSignal(int)
    delete_search = pyqtSignal(int)
    rename_search = pyqtSignal(int, str)
    apply_filter = pyqtSignal(int, object)
    filter_by_id = pyqtSignal(list)

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
