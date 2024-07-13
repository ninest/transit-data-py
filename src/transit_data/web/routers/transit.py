from fastapi import APIRouter


from transit_data.models import FullLine, Stop, Operator, Line
from transit_data.web.service import transit_service

router = APIRouter()


@router.get("/{location_code}")
async def get_operators_by_location(location_code: str) -> list[Operator]:
    operators = transit_service.get_operators(location_code=location_code)
    return operators


@router.get("/{location_code}/{operator_id}/stops")
async def get_stops(location_code: str, operator_id: str) -> list[Stop]:
    stops = transit_service.get_stops(location_code, operator_id)
    return stops


@router.get("/{location_code}/{operator_id}/lines")
async def get_lines(location_code: str, operator_id: str) -> list[Line]:
    lines = transit_service.get_lines(location_code, operator_id)
    return lines


@router.get("/{location_code}/{operator_id}/lines/{route_ud}")
async def get_line(location_code: str, operator_id: str, route_id) -> FullLine:
    lines = transit_service.get_line(location_code, operator_id, route_id)
    return lines
