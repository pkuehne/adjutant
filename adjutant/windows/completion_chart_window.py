"""Window to show the completion charts"""

from dataclasses import dataclass
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QComboBox,
    QLabel,
)
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QBarCategoryAxis, QValueAxis
from PyQt6.QtSql import QSqlRecord

from adjutant.context import Context

MONTH_AXIS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

NUMERIC_MONTHS = [
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "11",
    "12",
]


@dataclass
class Data:
    """Processed data to show"""

    completion = {}
    years = []


@dataclass
class Widgets:
    """Widgets for the window"""

    close_button: QPushButton
    chart_view: QChartView
    year_select: QComboBox
    y_axis: QValueAxis


class CompletionChartWindow(QDialog):
    """Window to show completion charts"""

    def __init__(self, context: Context, parent):
        super().__init__(parent)
        self.context = context
        self.data = Data()
        self.chart = QChart()
        self.widgets = Widgets(
            QPushButton(self.tr("Close")),
            QChartView(self.chart, self),
            QComboBox(),
            QValueAxis(),
        )
        self.widgets.close_button.pressed.connect(self.reject)
        self.widgets.year_select.currentTextChanged.connect(self.update_chart)
        x_axis = QBarCategoryAxis()
        x_axis.append(MONTH_AXIS)
        self.chart.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)
        self.chart.addAxis(self.widgets.y_axis, Qt.AlignmentFlag.AlignLeft)

        self.setup_layout()
        self.resize(700, 400)
        # self.load_data()
        # self.update_chart()

    def setup_layout(self):
        """Setup the window layout"""
        select_layout = QHBoxLayout()
        select_layout.addStretch()
        select_layout.addWidget(QLabel(self.tr("Year")))
        select_layout.addWidget(self.widgets.year_select)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.widgets.close_button)

        layout = QVBoxLayout()
        layout.addLayout(select_layout)
        layout.addWidget(self.widgets.chart_view)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setWindowTitle(self.tr("Completion Chart"))

    def load_data(self):
        """Load data from bases"""
        self.data = Data()

        model = self.context.models.bases_model
        for row in range(model.rowCount()):
            record: QSqlRecord = model.record(row)
            completed: str = record.value("date_completed")
            if completed == "":
                continue
            (year, month, _) = completed.split("-")

            if not year in self.data.completion:
                self.data.years.insert(0, year)
                self.data.completion[year] = {}
                for mon in NUMERIC_MONTHS:
                    self.data.completion[year][mon] = 0

            self.data.completion[year][month] = self.data.completion[year][month] + 1

        self.data.years.sort()
        self.widgets.year_select.clear()
        self.widgets.year_select.addItems(self.data.years)

    def update_chart(self):
        """Update the series on the chart"""
        self.chart.removeAllSeries()

        line = QLineSeries()
        year = self.widgets.year_select.currentText()

        maximum = 0
        for month in reversed(NUMERIC_MONTHS):
            line.append(int(month), self.data.completion[year][month])
            maximum = max(self.data.completion[year][month], maximum)

        self.chart.addSeries(line)
        self.chart.setTitle(f"Completed Miniatures {year}")
        self.chart.legend().hide()

        self.widgets.y_axis.setRange(0, maximum)
        line.attachAxis(self.widgets.y_axis)

    @classmethod
    def show(cls, context, parent):
        """Wraps the creation of the dialog, particularly for unit testing"""
        cls.dialog_reference = cls(context, parent)
        cls.dialog_reference.load_data()
        cls.dialog_reference.update_chart()
        cls.dialog_reference.exec()
        cls.dialog_reference = None
