from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, validator
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )


class GTFSFeed(BaseSchema):
    id: str
    location_code: str
    url: str  # download URL
    name: str
    operators: list["Operator"]


class Operator(BaseSchema):
    id: str
    name: str  # agency_name in GTFS agency.txt
    full_name: str
    short_name: str


class Location(BaseSchema):
    lat: float
    lon: float


class Stop(BaseSchema):
    id: str = Field(validation_alias="stop_id")
    name: str = Field(validation_alias="stop_name")
    url: Optional[str] = Field(validation_alias="stop_url")
    address: Optional[str] = Field(validation_alias="stop_address")
    parent_station: str
    location: Optional[Location]
    zone_id: Optional[str]
    # vehicle_type: Optional[str]  # TODO: make enum
    # wheelchair_boarding: Optional[str]  # TODO: make enum


class StopId(BaseSchema):  # think of better name
    """Minimal information for stop"""

    id: str = Field(validation_alias="stop_id")
    parent_station: str


class Line(BaseSchema):
    id: str = Field(validation_alias="line_id")
    color: str = Field(validation_alias="line_color")
    text_color: str = Field(validation_alias="line_text_color")
    short_name: Optional[str] = Field(validation_alias="line_short_name")
    long_name: Optional[str] = Field(validation_alias="line_long_name")
    url: Optional[str] = Field(validation_alias="line_url")
    type: "RouteTypeEnum" = Field(validation_alias="route_type")


class RouteTypeEnum(int, Enum):
    light_rail = 0
    subway = 1
    rail = 2
    bus = 3
    ferry = 4
    cable_tram = 5
    aerial_lift = 6
    funicular = 7
    trolleybus = 11
    monorail = 12


class FullLine(BaseSchema):
    id: str = Field(validation_alias="line_id")
    color: str = Field(validation_alias="line_color")
    text_color: str = Field(validation_alias="line_text_color")
    long_name: str = Field(validation_alias="line_long_name")
    url: None | str = Field(validation_alias="line_url")
    directions: Dict[str, "Direction"]


class Direction(BaseSchema):
    id: str = Field(validation_alias="direction_id", coerce_numbers_to_str=True)
    name: str = Field(validation_alias="direction_name")
    destination: str
    stops: List[StopId]
    order: Dict[str, List[str]]  # Record of parent_station to List[parent_station]
