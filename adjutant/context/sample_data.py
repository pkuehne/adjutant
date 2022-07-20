""" Provide sample data for a first run """

from adjutant.context.model_context import ModelContext
from adjutant.context.database_context import generate_uuid
from adjutant.models.relational_model import RelationalModel


# 9a1885b7-2fa4-4269-9e97-5f54540adffa
# 02078bcb-ab49-42f5-8e32-e5db3fcb4b62
# f80aad0f-2327-4c5b-8ded-11a0bbe6489f
# d18ad8a7-3cd3-4419-8df7-d49991c6441b
# c153e96c-18b6-4f2a-8c51-144dc7e3fc41
# 4b422834-396b-4db9-90fd-df8c43540c78
# 5b29c22c-8447-451f-a20e-0bf6d5e54125
# a74ed3c0-e2d6-49fd-a172-64ada33d660b
# 2cf37d45-32f7-4fd7-855d-c1ca10e810fb
# 7db5c7e5-a953-4100-b2ec-6f8377d15672
# 36f3b3b5-93c0-4534-b3ce-c28085ba0802
# d683932f-6dd7-416c-a3a6-025bc5a3e0fd
# fdeb5349-e53f-4994-82e7-964ce6b65c0f
# 884ab6cb-dbbb-4cdf-a99a-cc24d5951f9d
# b004c6ae-cbfa-4f40-a8fd-db05393b9773
# 438018b1-eb06-48fd-81bf-474ceef654e6
# 2d2c1ca1-5a79-416b-99a7-cc7f8b710256
# a74834a1-3daf-4238-a321-928b27fc8792
# 45dcb88b-6a8c-4aca-a7d2-e6680711ec20

tags = [
    {"id": "eae75e52-d387-4423-abd1-13350d64e181", "name": "Weapon: Boltgun"},
    {"id": "d19b95e0-5103-4f6c-b284-523078a41795", "name": "Weapon: Flamer"},
    {"id": "1135ddfe-d851-4fe0-b661-b69e7b7c82b4", "name": "Weapon: Chainsword"},
    {"id": "76ab2998-b649-4802-89c7-75ea71e86688", "name": "Type: Hero"},
]

bases = [
    {
        "id": "e9896f2a-1bea-47b8-bd6a-f5799627afcc",
        "name": "Space Marine",
        "scale": "32mm",
        "base": "Round",
        "width": 32,
        "depth": 0,
        "figures": 1,
        "material": "Plastic",
        "manufacturer": "Games Workshop",
        "retailer": "GW Online",
        "notes": "not varnished",
        "date_acquired": "2006-03-15",
        "date_completed": "2006-04-07",
        "custom_id": "Ultramarines-1",
        "storages_id": "3affe44f-1f1d-43f2-a85b-cad24b79c19a",
        "status_id": "00200f74-5d1d-4d49-94a0-4b133243c011",
        "schemes_id": "1da82f45-9288-49df-b06b-1af14904414e",
    },
    {
        "id": "b2844056-574f-4f56-b0d8-9143dfb7170f",
        "name": "Space Marine",
        "scale": "32mm",
        "base": "Round",
        "width": 32,
        "depth": 0,
        "figures": 1,
        "material": "Plastic",
        "manufacturer": "Games Workshop",
        "retailer": "GW Online",
        "notes": "not varnished",
        "date_acquired": "2006-03-15",
        "date_completed": "2006-04-07",
        "custom_id": "Ultramarines-2",
        "storages_id": "3affe44f-1f1d-43f2-a85b-cad24b79c19a",
        "status_id": "00200f74-5d1d-4d49-94a0-4b133243c011",
        "schemes_id": "1da82f45-9288-49df-b06b-1af14904414e",
    },
    {
        "id": "1e90a438-2757-44f5-bffc-4125233cddda",
        "name": "Space Marine",
        "scale": "32mm",
        "base": "Round",
        "width": 32,
        "depth": 0,
        "figures": 1,
        "material": "Plastic",
        "manufacturer": "Games Workshop",
        "retailer": "GW Online",
        "notes": "not varnished",
        "date_acquired": "2006-03-15",
        "date_completed": "2006-04-07",
        "custom_id": "Ultramarines-3",
        "storages_id": "3affe44f-1f1d-43f2-a85b-cad24b79c19a",
        "status_id": "00200f74-5d1d-4d49-94a0-4b133243c011",
        "schemes_id": "1da82f45-9288-49df-b06b-1af14904414e",
    },
    {
        "id": "cdbc6ec9-3065-4e9f-9c02-99e6e3bfcbfc",
        "name": "Space Marine Captain",
        "scale": "32mm",
        "base": "Round",
        "width": 32,
        "depth": 0,
        "figures": 1,
        "material": "Plastic",
        "manufacturer": "Games Workshop",
        "retailer": "GW Online",
        "notes": "not varnished",
        "date_acquired": "2006-03-15",
        "custom_id": "Ultramarines-Cap",
        "storages_id": "3affe44f-1f1d-43f2-a85b-cad24b79c19a",
        "status_id": "60adfe10-9c13-4ca9-9bbc-c1bf830ad64a",
        "schemes_id": "1da82f45-9288-49df-b06b-1af14904414e",
    },
]

bases_tags = [
    {
        "id": generate_uuid(),
        "bases_id": "e9896f2a-1bea-47b8-bd6a-f5799627afcc",
        "tags_id": "eae75e52-d387-4423-abd1-13350d64e181",
    },
    {
        "id": generate_uuid(),
        "bases_id": "b2844056-574f-4f56-b0d8-9143dfb7170f",
        "tags_id": "eae75e52-d387-4423-abd1-13350d64e181",
    },
    {
        "id": generate_uuid(),
        "bases_id": "1e90a438-2757-44f5-bffc-4125233cddda",
        "tags_id": "d19b95e0-5103-4f6c-b284-523078a41795",
    },
    {
        "id": generate_uuid(),
        "bases_id": "cdbc6ec9-3065-4e9f-9c02-99e6e3bfcbfc",
        "tags_id": "1135ddfe-d851-4fe0-b661-b69e7b7c82b4",
    },
    {
        "id": generate_uuid(),
        "bases_id": "cdbc6ec9-3065-4e9f-9c02-99e6e3bfcbfc",
        "tags_id": "76ab2998-b649-4802-89c7-75ea71e86688",
    },
]

storages = [
    {
        "id": "3affe44f-1f1d-43f2-a85b-cad24b79c19a",
        "name": "Warhammer Foam Case",
        "location": "Under desk",
        "notes": "Has two layers",
    },
    {
        "id": "f17189a3-5d8d-41c8-aed7-51a40f71a2a1",
        "name": "Storage Box - Space Marines",
        "location": "Bottom Shelf",
        "magnetized": True,
    },
]

statuses = [
    {"id": "8a36df29-16ce-4b66-a411-064d85df9e28", "name": "Boxed"},
    {"id": "238c432f-2673-4eb5-acbf-c507e4d92088", "name": "Built"},
    {"id": "0be8d78c-6069-4f94-a45b-8f1617458f19", "name": "Sprayed"},
    {"id": "60adfe10-9c13-4ca9-9bbc-c1bf830ad64a", "name": "Painted"},
    {"id": "563cc84b-3b5f-4046-a664-809c7edd0192", "name": "Based"},
    {"id": "00200f74-5d1d-4d49-94a0-4b133243c011", "name": "Complete"},
]

step_operations = [
    {"id": "cf61fd6e-a143-448e-86be-d89bb0227001", "name": "Base"},
    {"id": "851ee12a-33dc-43da-8948-febc319ed4c6", "name": "Wash"},
    {"id": "3f7941fd-f39f-4590-a9ed-8ce94b519bc7", "name": "Layer"},
    {"id": "02073773-7bb3-4478-8926-1930ecfc27f0", "name": "Highlight"},
    {"id": "f23b70cc-f32a-4936-acc3-a67bfd13957a", "name": "Glaze"},
    {"id": "78ea793b-c40a-482d-99cb-47360af170d8", "name": "Varnish"},
]

paints = [
    {
        "id": "7768e2eb-4e21-4920-b7ce-f940f8d83b0f",
        "name": "Macragge Blue",
        "manufacturer": "Games Workshop",
        "range": "Base",
        "hexvalue": "#0D407F",
    },
    {
        "id": "43ec89fa-c29b-48eb-a52a-61d843e34309",
        "name": "Kantor Blue",
        "manufacturer": "Games Workshop",
        "range": "Base",
        "hexvalue": "#002151",
    },
    {
        "id": "7f360576-f09c-4a27-93f4-03f7928e8d27",
        "name": "Calgar Blue",
        "manufacturer": "Games Workshop",
        "range": "Layer",
        "hexvalue": "#4272B8",
    },
    {
        "id": "c3bf6dd6-a79c-4528-98de-b77138c79fab",
        "name": "Fenrisian Grey",
        "manufacturer": "Games Workshop",
        "range": "Layer",
        "hexvalue": "#719BB7",
    },
    {
        "id": "bb833e44-5516-4247-9686-0e872af98e42",
        "name": "Abaddon Black",
        "manufacturer": "Games Workshop",
        "range": "Base",
        "hexvalue": "#231F20",
    },
    {
        "id": "e7ebfecf-2576-4127-b70f-8c0cddff0dd2",
        "name": "Mechanicus Standard Grey",
        "manufacturer": "Games Workshop",
        "range": "Base",
        "hexvalue": "#3D4B4D",
    },
    {
        "id": "6aaeaac6-bc03-403b-9c6e-a8a6a8935084",
        "name": "Administratum Grey",
        "manufacturer": "Games Workshop",
        "range": "Layer",
        "hexvalue": "#949B95",
    },
]

recipes = [
    {
        "id": "2b007536-b1ea-4511-bc96-cfbd5ce8064f",
        "name": "Ultramarine Armour",
        "notes": "Final highlight should only be at the highest points",
    },
    {
        "id": "0bb6beb5-9ed1-41e6-b0de-ed42d2c6146c",
        "name": "Black bits",
        "notes": "Administratum should be on the corners",
    },
]

recipe_steps = [
    {
        "id": "ba2c6c81-90eb-48dd-9d05-854fba59f337",
        "recipes_id": "2b007536-b1ea-4511-bc96-cfbd5ce8064f",
        "paints_id": "7768e2eb-4e21-4920-b7ce-f940f8d83b0f",
        "operations_id": "cf61fd6e-a143-448e-86be-d89bb0227001",
        "priority": 1,
    },
    {
        "id": "9656ec20-1d06-4342-8611-2456d3c27c17",
        "recipes_id": "2b007536-b1ea-4511-bc96-cfbd5ce8064f",
        "paints_id": "43ec89fa-c29b-48eb-a52a-61d843e34309",
        "operations_id": "851ee12a-33dc-43da-8948-febc319ed4c6",
        "priority": 2,
    },
    {
        "id": "1f31b28b-8714-47bc-b6a8-337e8194e6c8",
        "recipes_id": "2b007536-b1ea-4511-bc96-cfbd5ce8064f",
        "paints_id": "7f360576-f09c-4a27-93f4-03f7928e8d27",
        "operations_id": "02073773-7bb3-4478-8926-1930ecfc27f0",
        "priority": 3,
    },
    {
        "id": "06b3086b-5b35-479c-a0c3-9b391d4e030e",
        "recipes_id": "2b007536-b1ea-4511-bc96-cfbd5ce8064f",
        "paints_id": "c3bf6dd6-a79c-4528-98de-b77138c79fab",
        "operations_id": "02073773-7bb3-4478-8926-1930ecfc27f0",
        "priority": 4,
    },
    {
        "id": "20907be9-7e08-47fd-9940-0132b64bbfce",
        "recipes_id": "0bb6beb5-9ed1-41e6-b0de-ed42d2c6146c",
        "paints_id": "bb833e44-5516-4247-9686-0e872af98e42",
        "operations_id": "cf61fd6e-a143-448e-86be-d89bb0227001",
        "priority": 1,
    },
    {
        "id": "ca2b2b74-4467-4d91-aaec-4ce9a8145e68",
        "recipes_id": "0bb6beb5-9ed1-41e6-b0de-ed42d2c6146c",
        "paints_id": "e7ebfecf-2576-4127-b70f-8c0cddff0dd2",
        "operations_id": "02073773-7bb3-4478-8926-1930ecfc27f0",
        "priority": 2,
    },
    {
        "id": "6abe4899-3e93-4b5d-9175-5acc561738b8",
        "recipes_id": "0bb6beb5-9ed1-41e6-b0de-ed42d2c6146c",
        "paints_id": "6aaeaac6-bc03-403b-9c6e-a8a6a8935084",
        "operations_id": "02073773-7bb3-4478-8926-1930ecfc27f0",
        "priority": 3,
    },
]


colour_schemes = [
    {
        "id": "1da82f45-9288-49df-b06b-1af14904414e",
        "name": "Ultramarines",
        "notes": "Basic colour scheme for fast painting armies",
    },
]

scheme_components = [
    {
        "id": "2c6283a4-2194-4f1a-81e3-d57b8b275c1f",
        "schemes_id": "1da82f45-9288-49df-b06b-1af14904414e",
        "name": "Armour",
        "recipes_id": "2b007536-b1ea-4511-bc96-cfbd5ce8064f",
    },
    {
        "id": "d4b19c85-a780-4260-8e07-d740cbad4a0a",
        "schemes_id": "1da82f45-9288-49df-b06b-1af14904414e",
        "name": "Boltgun",
        "recipes_id": "0bb6beb5-9ed1-41e6-b0de-ed42d2c6146c",
    },
]


class SampleData:
    """Provides Sample data to the models"""

    def __init__(self, models: ModelContext) -> None:
        self.models = models

    def _load_records(self, source_list, model: RelationalModel) -> None:
        """Loads an array of fields into the given model"""
        for source in source_list:
            record = model.record()
            for key, value in source.items():
                record.setValue(key, value)
            model.insertRecord(-1, record)
        model.submitAll()

    def load_all(self) -> None:
        """Loads all sample data"""
        # for _ in range(10):
        #     print(generate_uuid())

        self._load_records(statuses, self.models.statuses_model)
        self._load_records(storages, self.models.storages_model)
        self._load_records(step_operations, self.models.step_operations_model)
        self._load_records(paints, self.models.paints_model)
        self._load_records(recipes, self.models.recipes_model)
        self._load_records(recipe_steps, self.models.recipe_steps_model)
        self._load_records(colour_schemes, self.models.colour_schemes_model)
        self._load_records(scheme_components, self.models.scheme_components_model)

        self._load_records(tags, self.models.tags_model)
        self._load_records(bases, self.models.bases_model)
        self._load_records(bases_tags, self.models.base_tags_model)

        self.models.refresh_models()
