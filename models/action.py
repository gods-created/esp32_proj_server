from .base import Base 
from mongoengine import StringField, DateTimeField, ValidationError

from enums import ActionEnum

from datetime import datetime

def _if_action_correct(value: str) -> None:
    if value not in [
        item.value for item in ActionEnum
    ]:
        raise ValidationError('Action \'value\' is invalid')

class Action(Base):
    value = StringField(
        min_length=2,
        max_length=3,
        validation=_if_action_correct
    )

    created_at = DateTimeField(
        default=lambda: datetime.now()
    )

    meta = {
        'indexes': [
            'value',
            ('value', '-created_at')
        ],
        'collection': 'actions'
    }