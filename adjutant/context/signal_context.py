""" Context for all signals """


from PyQt6.QtCore import QModelIndex, QObject, pyqtSignal


class SignalContext(QObject):
    """Collects all pan-application signals"""

    edit_base = pyqtSignal(QModelIndex)
    add_base = pyqtSignal()
    delete_base = pyqtSignal(QModelIndex)
    delete_bases = pyqtSignal(list)
    duplicate_base = pyqtSignal(QModelIndex, int)
    update_bases = pyqtSignal()

    save_search = pyqtSignal()
    load_search = pyqtSignal(int)
    delete_search = pyqtSignal(int)
    rename_search = pyqtSignal(int, str)
    apply_filter = pyqtSignal(int, object)

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
