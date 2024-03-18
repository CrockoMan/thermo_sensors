from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent

from main import app
from sensors.dao import SensorDAO
from sensors.router import get_sensors

router_pages = APIRouter(prefix="", tags=["frontend"])

templates = Jinja2Templates(directory="templates")

@router_pages.get('/')
async def get_sensors(request: Request,
                      sensors=Depends(get_sensors)):
    return templates.TemplateResponse(name='sensors.html',
                                      context={'request': request,
                                               'sensors': sensors}
                                      )


@app.get("/api/view/", response_model=FastUI, response_model_exclude_none=True)
async def users_table() -> list[AnyComponent]:
    """
    Show a table of four users, `/api` is the endpoint the frontend will connect to
    when a user visits `/` to fetch components to render.
    """
    return [
        c.Page(
            components=[
                c.Heading(text='Users', level=2),  # renders `<h2>Users</h2>`
                c.Table(
                    data=await SensorDAO.find_all(),
                    columns=[
                        DisplayLookup(field='name', ),
                        # DisplayLookup(field='name', on_click=GoToEvent(url='/user/{id}/')),
                        # DisplayLookup(field='dob', mode=DisplayMode.date),
                    ],
                ),
            ]
        ),
    ]