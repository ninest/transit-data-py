from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from transit_data.web.routers import transit

app = FastAPI(title="Transit Data Py", version="0.0.1")


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


@app.get("/ping")
def pong():
    return {"ping": "pong"}


app.include_router(transit.router, prefix="/transit")
