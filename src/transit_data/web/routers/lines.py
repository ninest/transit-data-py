from fastapi import APIRouter

router = APIRouter()


@router.get("/{location_code}/{agency}/lines", tags=["lines"])
async def get_lines(agency: str):
    return "lines"
