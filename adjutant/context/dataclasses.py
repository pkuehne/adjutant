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
    select_query: str = None
    delete_query: str = None
    insert_query: str = None


@dataclass(eq=True, frozen=True)
class Tag:
    """Tag"""

    tag_id: int
    tag_name: str