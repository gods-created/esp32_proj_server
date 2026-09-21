from .base import BaseSerializer

from models import Action
from mongoengine.errors import MongoEngineException, ValidationError

from typing import Optional
from json import loads

class ActionSerializer(BaseSerializer):
    def insert(self, value: str) -> dict:
        response = {
            'status': False,
            'err_description': None,
            'item': None
        } 

        try:
            item = Action(value=value)
            item.save()

            response['item'] = loads(item.to_json())
            response['status'] = True 

        except ValidationError as e:
            response['err_description'] = e.message

        except MongoEngineException as e:
            response['err_description'] = f'Database error: {str(e)}'

        except Exception as e:
            response['err_description'] = f'Unexpected error: {str(e)}'

        return response
    
    def select(self, id: Optional[str] = None) -> dict:
        response = {
            'status': False,
            'err_description': None,
            'items': []
        } 

        try:
            queryset = Action.objects
            if id is not None:
                queryset = queryset.filter(id=id)

            response['items'] = [loads(item.to_json()) for item in queryset]
            response['status'] = True 

        except MongoEngineException as e:
            response['err_description'] = f'Database error: {str(e)}'

        except Exception as e:
            response['err_description'] = f'Unexpected error: {str(e)}'

        return response 

    def delete(self, id: Optional[str] = None) -> dict:
        response = {
            'status': False,
            'err_description': None,
        } 

        try:
            queryset = Action.objects
            if id is not None:
                queryset = queryset.filter(id=id)

            queryset.delete()

            response['status'] = True 

        except MongoEngineException as e:
            response['err_description'] = f'Database error: {str(e)}'

        except Exception as e:
            response['err_description'] = f'Unexpected error: {str(e)}'

        return response 