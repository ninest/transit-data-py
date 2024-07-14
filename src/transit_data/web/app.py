from fastapi import FastAPI
from fastapi.routing import APIRoute
from scalar_fastapi import get_scalar_api_reference

from transit_data.web.routers import transit

app = FastAPI(title="Transit Data Py", version="0.0.1")
app.openapi_version = "3.0.0"


def custom_generate_unique_id(route: APIRoute):
    return f"{route.name}"


app = FastAPI(generate_unique_id_function=custom_generate_unique_id)


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


@app.get("/ping", tags=["test"])
def pong():
    return {"ping": "pong"}


app.include_router(transit.router, prefix="/v1/transit")
