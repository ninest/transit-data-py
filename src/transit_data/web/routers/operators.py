from fastapi import APIRouter, HTTPException

from transit_data.gtfs import get_feed
from transit_data.models import Operator

router = APIRouter()


@router.get(
    "/{location_code}",
)
async def get_operators_by_location(location_code: str) -> list[Operator]:
    feed = get_feed(location_code)
    if feed is None:
        raise HTTPException(status_code=404, detail="Operators not found")
    return feed.operators
