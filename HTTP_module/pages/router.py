from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

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
