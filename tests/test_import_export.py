""" Tests for the yaml import/export functionality"""

from pathlib import Path

from adjutant.context.import_export import write_models_to_yaml, read_models_from_yaml
from adjutant.context.context import Context
from .conftest import Models


def test_write_creates_yaml_of_model(tmp_path: Path, context: Context, models: Models):
    """The list of models should be turned into yaml"""
    # Given
    file = tmp_path / "export.yaml"
    content = "tags:\n- id: Bar\n  name: Foo\n"
    models.add_tag("Foo", "Bar")

    # When
    write_models_to_yaml({"tags": context.models.tags_model}, str(file))

    # Then
    assert file.read_text() == content


def test_read_updates_model_from_yaml(tmp_path: Path, context: Context):
    """The yaml should be read into the model"""
    # Given
    file = tmp_path / "import.yaml"
    content = "tags:\n- id: Bar\n  name: Foo\n"
    file.write_text(content)

    # When
    read_models_from_yaml({"tags": context.models.tags_model}, str(file))

    # Then
    assert context.models.tags_model.rowCount() == 1
    record = context.models.tags_model.record(0)
    assert record.field("id").value() == "Bar"
    assert record.field("name").value() == "Foo"
