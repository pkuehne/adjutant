""" Fixtures """

from typing import Callable, List


from dataclasses import dataclass
import pytest

from adjutant.context.context import Context
from adjutant.models.relational_model import RelationalModel

# pylint: disable=redefined-outer-name


@dataclass
class BasesRecord:
    """Stand-in for the real database record"""

    base_id: int = None
    name: str = ""
    scale: str = ""
    base: str = ""
    width: int = 0
    depth: int = 0
    figures: int = 0
    status: int = 0
    scheme_id: int = 0


AddBaseFunc = Callable[[List[BasesRecord]], None]


@pytest.fixture
def add_base(context: Context) -> AddBaseFunc:
    """Adds a base to the database"""

    def add_base_func(items: List[BasesRecord]):
        for item in items:
            record = context.models.bases_model.record()
            if item.base_id is None:
                record.setNull("id")
            else:
                record.setValue("id", item.base_id)
            record.setValue("name", item.name)
            record.setValue("scale", item.scale)
            record.setValue("base", item.base)
            record.setValue("width", item.width)
            record.setValue("depth", item.depth)
            record.setValue("figures", item.figures)
            record.setValue("status_id", item.status)

            assert context.models.bases_model.insertRecord(-1, record)
        context.models.bases_model.submitAll()
        assert context.models.bases_model.lastError().text() == ""

    return add_base_func


AddEmptyBasesFunc = Callable[[int], None]


@pytest.fixture
def add_empty_bases(add_base: AddBaseFunc) -> AddEmptyBasesFunc:
    """Adds a number of empty bases"""

    def add_empty_bases_func(num: int) -> None:
        add_base([BasesRecord()] * num)

    return add_empty_bases_func


AddTagFunc = Callable[[str], None]


@pytest.fixture
def add_tag(context: Context) -> AddTagFunc:
    """Fixture to add a record to the tags table"""

    def add_tag_func(name: str):
        record = context.models.tags_model.record()
        record.setNull("id")
        record.setValue("name", name)
        assert context.models.tags_model.insertRecord(-1, record)
        context.models.tags_model.submitAll()
        assert context.models.tags_model.lastError().text() == ""

    return add_tag_func


AddTagUseFunc = Callable[[int, int], None]


@pytest.fixture
def add_tag_use(context: Context) -> AddTagUseFunc:
    """Fixture to add a record to the base_tags table"""

    def add_tag_use_func(base: int, tag: int) -> None:
        record = context.models.base_tags_model.record()
        record.setNull("id")
        record.setValue("bases_id", base)
        record.setValue("tags_id", tag)
        assert context.models.base_tags_model.insertRecord(-1, record)
        context.models.base_tags_model.submitAll()
        assert context.models.base_tags_model.lastError().text() == ""

    return add_tag_use_func


AddSearchFunc = Callable[[str], None]


@pytest.fixture
def add_search(context: Context) -> AddSearchFunc:
    """Fixture to add a record to the searches table"""

    def add_search_func(name: str) -> None:
        record = context.models.searches_model.record()
        record.setNull("id")
        record.setValue("name", name)
        assert context.models.searches_model.insertRecord(-1, record)
        context.models.searches_model.submitAll()
        assert context.models.searches_model.lastError().text() == ""

    return add_search_func


AddStatusFunc = Callable[[str], None]


@pytest.fixture
def add_status(context: Context) -> AddStatusFunc:
    """Fixture to add a record to the statuses table"""

    def add_status_func(name: str) -> None:
        record = context.models.statuses_model.record()
        record.setNull("id")
        record.setValue("name", name)
        assert context.models.statuses_model.insertRecord(-1, record)
        context.models.statuses_model.submitAll()
        assert context.models.statuses_model.lastError().text() == ""

    return add_status_func


AddStorageFunc = Callable[[str], None]


@pytest.fixture
def add_storage(context: Context) -> AddStorageFunc:
    """Fixture to add a record to the storage table"""

    def internal_func(name: str) -> None:
        record = context.models.storage_model.record()
        record.setNull("id")
        record.setValue("name", name)
        assert context.models.storage_model.insertRecord(-1, record)
        context.models.storage_model.submitAll()
        assert context.models.storage_model.lastError().text() == ""

    return internal_func


AddColourFunc = Callable[[str], None]


@pytest.fixture
def add_colour(context: Context) -> AddColourFunc:
    """Fixture to add a record to the colours table"""

    def internal_func(name: str) -> None:
        record = context.models.colours_model.record()
        record.setNull("id")
        record.setValue("name", name)
        assert context.models.colours_model.insertRecord(-1, record)
        context.models.colours_model.submitAll()
        assert context.models.colours_model.lastError().text() == ""

    return internal_func


AddRecipeFunc = Callable[[str], None]


@pytest.fixture
def add_recipe(context: Context) -> AddRecipeFunc:
    """Fixture to add a record to the colour recipes table"""

    def internal_func(name: str) -> None:
        record = context.models.recipes_model.record()
        record.setNull("id")
        record.setValue("name", name)
        assert context.models.recipes_model.insertRecord(-1, record)
        context.models.recipes_model.submitAll()
        assert context.models.recipes_model.lastError().text() == ""

    return internal_func


AddStepFunc = Callable[[int, int, int], None]


@pytest.fixture
def add_step(context: Context) -> AddStepFunc:
    """Fixture to add a record to the recipe steps table"""

    def internal_func(recipe_id: int, colour_id: int, num: int) -> None:
        record = context.models.recipe_steps_model.record()
        record.setNull("id")
        record.setValue("colours_id", colour_id)
        record.setValue("recipes_id", recipe_id)
        record.setValue("step_num", num)

        assert context.models.recipe_steps_model.insertRecord(-1, record)
        context.models.recipe_steps_model.submitAll()
        assert context.models.recipe_steps_model.lastError().text() == ""

    return internal_func


class Models:
    """Utility class to connect add_* functions together"""

    def __init__(self, context: Context) -> None:
        self.context = context

    def add_base(self, item: BasesRecord):
        """Fixture to add a new base"""
        model = self.context.models.bases_model
        record = model.record()
        if item.base_id is None:
            record.setNull("id")
        else:
            record.setValue("id", item.base_id)
        record.setValue("name", item.name)
        record.setValue("scale", item.scale)
        record.setValue("base", item.base)
        record.setValue("width", item.width)
        record.setValue("depth", item.depth)
        record.setValue("figures", item.figures)
        record.setValue("status_id", item.status)
        record.setValue("schemes_id", item.scheme_id)

        assert model.insertRecord(-1, record)
        model.submitAll()
        assert model.lastError().text() == ""

    def add_scheme(self, name: str):
        """Fixture to add a scheme to the database"""
        model = self.context.models.colour_schemes_model
        record = model.record()
        record.setNull("id")
        record.setValue("name", name)
        assert model.insertRecord(-1, record)
        model.submitAll()
        assert model.lastError().text() == ""

    def add_component(self, scheme_id: int, name: str, recipe_id: int):
        """Fixture to add a record to the recipe steps table"""
        model = self.context.models.scheme_components_model
        record = model.record()
        record.setNull("id")
        record.setValue("schemes_id", scheme_id)
        record.setValue("name", name)
        record.setValue("recipes_id", recipe_id)

        assert model.insertRecord(-1, record)
        model.submitAll()
        assert model.lastError().text() == ""

    def add_recipe(self, name):
        """Fixture to add a record to the colour recipes table"""
        model = self.context.models.recipes_model
        record = model.record()
        record.setNull("id")
        record.setValue("name", name)
        assert model.insertRecord(-1, record)
        model.submitAll()
        assert model.lastError().text() == ""

    def add_search(self, name: str):
        """Fixture to add a record to the searches table"""
        model = self.context.models.searches_model
        record = model.record()
        record.setNull("id")
        record.setValue("name", name)
        assert model.insertRecord(-1, record)
        model.submitAll()
        assert model.lastError().text() == ""


@pytest.fixture
def models(context: Context):
    """Fixture for model access"""
    models = Models(context)
    return models


@pytest.fixture
def context():
    """Sets up and tears down the database"""

    context = Context()
    context.settings.database_version = 1
    context.load_database(":memory:")
    # context.database.execute_sql_file(":/populate_test_data.sql")
    context.models.refresh_models()

    return context


@pytest.fixture
def relational_model(context: Context):
    """fixture to create a RelationalModel"""
    rmod = RelationalModel()
    rmod.setTable("bases")
    rmod.setEditStrategy(rmod.EditStrategy.OnManualSubmit)
    context.models.bases_model = rmod
    return rmod
