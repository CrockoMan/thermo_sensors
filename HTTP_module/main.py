from datetime import datetime
from enum import Enum
from typing import List, Optional

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field

from pages.router import router_pages
from sensors.router import router_sensors

app = FastAPI(
    title='Thermo Sensors App'
)

app.include_router(router_sensors)
app.include_router(router_pages)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
