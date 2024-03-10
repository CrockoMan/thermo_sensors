import uvicorn
from fastapi import FastAPI
from sqladmin import Admin

from admin.views import SensorAdmin, SensorDataAdmin
from database import engine
from pages.router import router_pages
from sensors.router import router_sensors

app = FastAPI(
    title='Thermo Sensors App'
)

app.include_router(router_sensors)
app.include_router(router_pages)


admin = Admin(app, engine)

admin.add_view(SensorAdmin)
admin.add_view(SensorDataAdmin)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
