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
