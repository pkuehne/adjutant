""" Data classes for context """

from dataclasses import dataclass


@dataclass
class OneToManyRelationship:
    """Defines a one-tomany relationship"""

    target_table: str
    target_key: str
    target_field: str


@dataclass
class ManyToManyRelationship:
    """Defines a many-to-many relationship"""

    target_table: str
    target_field: int


@dataclass(eq=True, frozen=True)
class Tag:
    """Tag"""

    tag_id: int
    tag_name: str


@dataclass(eq=True, frozen=True)
class SchemeComponent:
    """Colour scheme component"""

    name: str
    recipe_id: int
