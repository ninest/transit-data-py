from fastapi import FastAPI

from .routers import stops, lines

app = FastAPI(title="Transit Data Py", version="0.0.1")


@app.get("/ping")
def pong():
    return {"ping": "pong"}


app.include_router(stops.router, prefix="/transit")
app.include_router(lines.router, prefix="/transit")
