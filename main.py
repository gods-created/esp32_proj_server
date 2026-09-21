from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from mongoengine import connect, disconnect
from mongoengine.errors import MongoEngineException

from config import *
from exceptions import UnicornException

from routers import app_router

from uvicorn import run

from loguru import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        if not all((
            DB_NAME, DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD
        )):
            raise ValueError('One of requried ENV parameters is not specified')

        if not DB_PORT.isdigit():
            raise ValueError('\'DB_PORT\' has invalid value')
            
        connect(
            db=DB_NAME, 
            host=DB_HOST, 
            port=int(DB_PORT), 
            username=DB_USERNAME, 
            password=DB_PASSWORD
        )
    
        app.state.db_connection = True

        logger.success('The connection with database is established successfully')

    except ValueError as e:
        logger.error(str(e))

    except MongoEngineException as e:
        logger.error(f'Database error: {str(e)}')

    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')

    yield

    if app.state.db_connection:
        disconnect('default')

app = FastAPI(
    title='Some App title',
    description='Some description',
    version='0.0.1',
    lifespan=lifespan,
    redoc_url=None,
    docs_url='/api/docs'
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_headers=['*'],
    allow_methods=['*'],
    allow_origins=['*']
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'status': False, 'err_description': str(exc.detail)},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    msg = errors[0].get('msg')

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'status': False, 'err_description': msg},
    )

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'status': False, 'err_description': exc.err_description},
    )

app.include_router(app_router, prefix='/api', tags=['API'])

if __name__ == '__main__':
    run('main:app', host='0.0.0.0', port=8001, reload=True)