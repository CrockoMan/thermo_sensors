from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router_pages = APIRouter(prefix="/pages", tags=["frontend"])

templates = Jinja2Templates(directory="templates")

@router_pages.get('/')
async def get_sensors(request: Request):
    return templates.TemplateResponse(name="sensors.html",
                                      context={"request": request}
                                      )
