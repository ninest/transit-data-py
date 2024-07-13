from typing import List, Optional, Dict
from pydantic import BaseModel, ConfigDict, Field
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
    operators: list["Operator"]


class Operator(BaseSchema):
    id: str
    name: str  # name in GTFS agency.txt


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
    vehicle_type: Optional[str]  # TODO: make enum
    wheelchair_boarding: Optional[str]  # TODO: make enum


class StopId(BaseSchema):  # think of better name
    """Minimal information for stop"""

    id: str
    parent_station: str


class Line(BaseSchema):
    id: str = Field(validation_alias="line_id")
    color: str = Field(validation_alias="line_color")
    text_color: str = Field(validation_alias="line_text_color")
    long_name: str = Field(validation_alias="line_long_name")


class FullLine(Line):
    directions: List["Direction"]


class Direction(BaseSchema):
    id: str = Field(validation_alias="direction_id")
    name: str = Field(validation_alias="direction_name")
    destination: str
    stops: List[StopId]
    order: Dict[str, List[str]]  # Record of parent_station to List[parent_station]
