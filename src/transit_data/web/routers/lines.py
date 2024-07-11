from fastapi import APIRouter

from transit_data.models import Line

router = APIRouter()


@router.get("/{location_code}/{agency}/lines", tags=["lines"])
async def get_lines(agency: str) -> list[Line]:
    d = [
        {
            "line_id": "1",
            "line_color": "a",
            "line_text_color": "a",
            "line_long_name": "asdf",
            "directions": [],
        }
    ]
    return [Line(**d[0])]
