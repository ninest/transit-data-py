from fastapi import FastAPI

from transit_data.web.routers import operators, stops, lines


app = FastAPI(title="Transit Data Py", version="0.0.1")


@app.get("/ping")
def pong():
    return {"ping": "pong"}


app.include_router(operators.router, prefix="/transit")
app.include_router(stops.router, prefix="/transit")
app.include_router(lines.router, prefix="/transit")
