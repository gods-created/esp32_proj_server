from fastapi import APIRouter, Depends, Request, Query, status
from fastapi.responses import JSONResponse

from exceptions import UnicornException
from serializers import ActionSerializer
from validators import ActionValidator

from typing import Optional

async def _if_db_connection_exists(request: Request):
    if not hasattr(request.app.state, 'db_connection'):
        raise UnicornException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            err_description='The connection with database doesn\'t exist'
        )
    
router = APIRouter(
    prefix='/action',
    tags=['ACTION'],
    default_response_class=JSONResponse,
    dependencies=[Depends(_if_db_connection_exists)]
)

serializer = ActionSerializer()

@router.post('')
async def _post(
    request: Request,
    data: ActionValidator
) -> JSONResponse:
    response = serializer.insert(value=data.value)
    return JSONResponse(
        content=response,
        status_code=status.HTTP_200_OK
    )

@router.get('')
async def _get(
    request: Request,
    id: Optional[str] = Query(default=None)
) -> JSONResponse:
    response = serializer.select(id=id)
    return JSONResponse(
        content=response,
        status_code=status.HTTP_200_OK
    )

@router.delete('')
async def _delete(
    request: Request,
    id: Optional[str] = Query(default=None)
) -> JSONResponse:
    response = serializer.delete(id=id)
    return JSONResponse(
        content=response,
        status_code=status.HTTP_200_OK
    )