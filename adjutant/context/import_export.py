""" Import/Export functionality """

import logging
from typing import Dict, List
import yaml

from adjutant.models.relational_model import RelationalModel


def write_models_to_yaml(models: Dict[str, RelationalModel], filename: str):
    """Write the data to the given filename"""

    data = {}

    for name, model in models.items():
        data_records: List[Dict] = []
        for row in range(model.rowCount()):
            record = model.record(row)
            data_record = {}
            for column in range(model.columnCount()):
                field_name = record.fieldName(column)
                if field_name == "":
                    continue
                data_record[record.fieldName(column)] = record.value(column)
            data_records.append(data_record)
        data[name] = data_records

    with open(filename, "w") as file:
        yaml.safe_dump(data, file)


def read_models_from_yaml(models: Dict[str, RelationalModel], filename: str):
    """Loads the data from the given filename"""

    with open(filename, "r") as file:
        data = yaml.safe_load(file)

    for name, model in models.items():
        data_records = data.get(name, [])
        for data_record in data_records:
            record = model.record()
            for field, value in data_record.items():
                record.setValue(field, value)
            model.insertRecord(-1, record)
        success = model.submitAll()
        if not success:
            logging.error("Failed to import record into %s", name)
