""" Data context """


from adjutant.context.controller import Controller
from adjutant.context.model_context import ModelContext
from adjutant.context.signal_context import SignalContext
from adjutant.context.settings_context import SettingsContext
from adjutant.context.database_context import DatabaseContext


class Context:
    """Data Context"""

    def __init__(self) -> None:
        self.settings = SettingsContext()
        self.signals = SignalContext()
        self.database = DatabaseContext()
        self.models = ModelContext()
        self.controller = Controller(
            self.models, self.database, self.signals, self.settings
        )
