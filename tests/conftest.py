""" Fixtures """

from typing import Callable, List


from dataclasses import dataclass
import pytest

from adjutant.context.context import Context
import adjutant.resources  # pylint: disable=unused-import

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
        assert context.models.bases_model.submitAll()

    return add_base_func


AddEmptyBasesFunc = Callable[[int], None]


@pytest.fixture
def add_empty_bases(add_base: AddBaseFunc) -> AddEmptyBasesFunc:
    """Adds a number of empty bases"""

    def add_empty_bases_func(num: int) -> None:
        add_base([BasesRecord()] * num)

    return add_empty_bases_func


@pytest.fixture
def context():
    """Sets up and tears down the database"""

    context = Context()
    context.settings.set_version("0.0.0-test")
    context.load_database(":memory:")
    # context.database.execute_sql_file(":/populate_test_data.sql")
    context.models.refresh_models()

    return context
