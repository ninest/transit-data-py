from fastapi import APIRouter


from transit_data.models import FullLine, GTFSFeed, Stop, Operator, Line
from transit_data.web.service import transit_service

router = APIRouter()


@router.get("/{location_code}", tags=["operators"])
async def get_feeds(location_code: str) -> list[GTFSFeed]:
    print(location_code)
    feeds = transit_service.get_feeds_by_location(location_code)
    return feeds


@router.get("/{location_code}/stops", tags=["stops"])
async def get_stops(location_code: str) -> list[Stop]:
    stops = transit_service.get_stops_by_location(location_code)
    return stops


@router.get("/{location_code}/{operator_id}", tags=["operators"])
async def get_operator(location_code: str, operator_id: str) -> Operator:
    operator = transit_service.get_operator(location_code, operator_id)
    return operator


@router.get("/{location_code}/lines", tags=["lines"])
async def get_lines_by_location(location_code: str) -> list[Line]:
    lines = transit_service.get_lines_by_location(
        location_code,
    )
    return lines


# @router.get("/{location_code}/lines", tags=["lines"])
# async def get_lines(location_code: str, operator_id: str) -> list[Line]:
#     lines = transit_service.get_lines(location_code, operator_id)
#     return lines


@router.get("/{location_code}/lines/{route_id}", tags=["lines"])
async def get_line(location_code: str, route_id: str) -> FullLine:
    lines = transit_service.get_line(location_code, route_id)
    return lines
