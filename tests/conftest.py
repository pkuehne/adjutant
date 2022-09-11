""" Fixtures """

from pathlib import Path
from unittest import mock

from dataclasses import dataclass
import pytest

from adjutant.context.context import Context
from adjutant.models.relational_model import RelationalModel
from adjutant.context.database_context import generate_uuid
import adjutant.context

# pylint: disable=redefined-outer-name


@dataclass
class BasesRecord:
    """Stand-in for the real database record"""

    base_id: str = None
    name: str = ""
    scale: str = ""
    base: str = ""
    width: int = 0
    depth: int = 0
    figures: int = 0
    status: str = 0
    storage: int = 0
    scheme_id: str = ""
    completed: str = None


class Models:
    """Utility class to connect add_* functions together"""

    def __init__(self, context: Context) -> None:
        self.context = context

    def add_base(self, item: BasesRecord):
        """Fixture to add a new base"""
        model = self.context.models.bases_model
        record = model.record()
        if item.base_id is None:
            uuid = generate_uuid()
            record.setValue("id", uuid)
        else:
            record.setValue("id", item.base_id)
        record.setValue("name", item.name)
        record.setValue("scale", item.scale)
        record.setValue("base", item.base)
        record.setValue("width", item.width)
        record.setValue("depth", item.depth)
        record.setValue("figures", item.figures)
        record.setValue("status_id", item.status)
        record.setValue("storages_id", item.storage)
        record.setValue("schemes_id", item.scheme_id)
        record.setValue("date_completed", item.completed)

        assert model.insertRecord(-1, record)
        model.submitAll()
        assert model.lastError().text() == ""
        return uuid

    def add_empty_bases(self, count: int) -> None:
        """Fixture to add a number of empty bases"""
        for _ in range(count):
            self.add_base(BasesRecord())

    def add_tag(self, name: str, id_: str = None):
        """Fixture to add a tag to the datbase"""
        model = self.context.models.tags_model
        record = model.record()
        uuid = id_ if id_ is not None else generate_uuid()
        record.setValue("id", uuid)
        record.setValue("name", name)
        assert model.insertRecord(-1, record)
        model.submitAll()
        assert model.lastError().text() == ""
        return uuid

    def add_tag_use(self, base: str, tag: str) -> None:
        """Fixture to add a connection between a base and a tag"""
        model = self.context.models.base_tags_model
        record = model.record()
        uuid = generate_uuid()
        record.setValue("id", uuid)
        record.setValue("bases_id", base)
        record.setValue("tags_id", tag)
        assert model.insertRecord(-1, record)
        model.submitAll()
        assert model.lastError().text() == ""
        return uuid

    def add_scheme(self, name: str):
        """Fixture to add a scheme to the database"""
        model = self.context.models.colour_schemes_model
        record = model.record()
        uuid = generate_uuid()
        record.setValue("id", uuid)
        record.setValue("name", name)
        assert model.insertRecord(-1, record)
        model.submitAll()
        assert model.lastError().text() == ""
        return uuid

    def add_component(self, scheme_id: int, name: str, recipe_id: int):
        """Fixture to add a record to the recipe steps table"""
        model = self.context.models.scheme_components_model
        record = model.record()
        uuid = generate_uuid()
        record.setValue("id", uuid)
        record.setValue("schemes_id", scheme_id)
        record.setValue("name", name)
        record.setValue("recipes_id", recipe_id)

        assert model.insertRecord(-1, record)
        model.submitAll()
        assert model.lastError().text() == ""
        return uuid

    def add_recipe(self, name):
        """Fixture to add a record to the colour recipes table"""
        model = self.context.models.recipes_model
        record = model.record()
        uuid = generate_uuid()
        record.setValue("id", uuid)
        record.setValue("name", name)
        assert model.insertRecord(-1, record)
        model.submitAll()
        assert model.lastError().text() == ""
        return uuid

    def add_search(self, name: str):
        """Fixture to add a record to the searches table"""
        model = self.context.models.searches_model
        record = model.record()
        uuid = generate_uuid()
        record.setValue("id", uuid)
        record.setValue("name", name)
        assert model.insertRecord(-1, record)
        model.submitAll()
        assert model.lastError().text() == ""
        return uuid

    def add_step(self, paint_id: str, recipe_id: str, step: int):
        """Fixture to add a record to the recipe steps table"""
        model = self.context.models.recipe_steps_model
        record = model.record()
        uuid = generate_uuid()
        record.setValue("id", uuid)
        record.setValue("paints_id", paint_id)
        record.setValue("recipes_id", recipe_id)
        record.setValue("priority", step)
        record.setValue("operations_id", 1)
        assert model.insertRecord(-1, record)
        model.submitAll()
        assert model.lastError().text() == ""
        return uuid

    def add_status(self, name: str):
        """Fixture to add a record to the statuses table"""
        model = self.context.models.statuses_model
        record = model.record()
        uuid = generate_uuid()
        record.setValue("id", uuid)
        record.setValue("name", name)
        assert model.insertRecord(-1, record)
        model.submitAll()
        assert model.lastError().text() == ""
        return uuid

    def add_storage(self, name: str):
        """Fixture to add a record to the storages table"""
        model = self.context.models.storages_model
        record = model.record()
        uuid = generate_uuid()
        record.setValue("id", uuid)
        record.setValue("name", name)
        assert model.insertRecord(-1, record)
        model.submitAll()
        assert model.lastError().text() == ""
        return uuid

    def add_paint(self, name: str):
        """Fixture to add a record to the paints table"""
        model = self.context.models.paints_model
        record = model.record()
        uuid = generate_uuid()
        record.setValue("id", uuid)
        record.setValue("name", name)
        assert model.insertRecord(-1, record)
        model.submitAll()
        assert model.lastError().text() == ""
        return uuid


@pytest.fixture
def models(context: Context) -> Models:
    """Fixture for model access"""
    models = Models(context)
    return models


@pytest.fixture
def context(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Sets up and tears down the database"""

    context = Context()
    monkeypatch.setattr(
        adjutant.context.settings_context, "SETTINGS_FILE", tmp_path / "settings.yaml"
    )
    monkeypatch.setattr(adjutant.context.database_context, "DATABASE_FILE", ":memory:")

    context.database.database.close()
    try:
        context.database.open_database()
    except RuntimeError:
        context.database.migrate()
    # context.database.execute_sql_file(":/populate_test_data.sql")
    context.models.load()
    context.models.refresh_models()

    context.controller.confirm_deletion = mock.Mock(return_value=True)
    return context


@pytest.fixture
def relational_model(context: Context) -> RelationalModel:
    """fixture to create a RelationalModel"""
    rmod = RelationalModel()
    rmod.setTable("bases")
    rmod.setEditStrategy(rmod.EditStrategy.OnManualSubmit)
    context.models.bases_model = rmod
    return rmod


@pytest.fixture(autouse=True)
def override_external_files(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """Overrides external files"""
    monkeypatch.setattr(
        adjutant.context.settings_context, "SETTINGS_FILE", tmp_path / "settings.yaml"
    )
    monkeypatch.setattr(adjutant.context.database_context, "DATABASE_FILE", ":memory:")
