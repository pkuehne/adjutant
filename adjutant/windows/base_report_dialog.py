"""Dialog for choosing colour scheme"""

from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
)
from adjutant.context import Context
from adjutant.models.row_zero_filter_model import RowZeroFilterModel
from adjutant.reports.painting_guide_report import PaintingGuideReport


class BaseReportDialog(QDialog):
    """Dialog for choosing a base"""

    dialog_reference = None

    def __init__(self, context: Context, parent, index=None) -> None:
        super().__init__(parent=parent)
        self.context = context
        self.index = index

        self.setWindowTitle("Painting Guide Report")
        self.scheme_combobox = QComboBox()
        model = RowZeroFilterModel()
        model.setSourceModel(context.models.bases_model)
        self.scheme_combobox.setModel(model)
        self.scheme_combobox.setModelColumn(1)
        self.cancel_button = QPushButton(self.tr("Cancel"))
        self.cancel_button.pressed.connect(self.reject)
        self.ok_button = QPushButton(self.tr("OK"))
        self.ok_button.pressed.connect(self.accept)

        self._setup_layout()
        self._setup_signals()

    def _setup_layout(self):
        """Layout the widgets"""

        options_layout = QFormLayout()
        options_layout.addRow(self.tr("Base (Miniature)"), self.scheme_combobox)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)

        central = QVBoxLayout()
        central.addLayout(options_layout)
        central.addLayout(button_layout)

        self.setLayout(central)

    def _setup_signals(self):
        self.accepted.connect(self.generate_report)

    def generate_report(self):
        """Generates the report with the options selected"""
        row = self.scheme_combobox.currentIndex()
        scheme_id = self.scheme_combobox.model().index(row, 0).data()
        report = PaintingGuideReport(self.context, scheme_id)
        report.prepare()
        report.generate()
        self.close()

    @classmethod
    def show(cls, context, parent, index=None):
        """Wraps the creation of the dialog, particularly for unit testing"""
        cls.dialog_reference = cls(context, parent, index)
        cls.dialog_reference.exec()
        cls.dialog_reference = None
