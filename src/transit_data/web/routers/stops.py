from fastapi import APIRouter

from ...gtfs import get_feed

router = APIRouter()


@router.get("/{location_code}/{agency}/stops", tags=["stops"])
async def get_stops(location_code: str, agency: str):
    feed = get_feed(location_code, agency)
    return feed
