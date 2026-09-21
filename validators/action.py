from pydantic import BaseModel, Field, field_validator

from enums import ActionEnum

class ActionValidator(BaseModel):
    value: str = Field(default='on', description='Only \'off\' or \'on\' value')

    @field_validator('value')
    @classmethod
    def validate_value(cls, value: str) -> str:
        lower_characters = value.lower()

        if not lower_characters in [
            item.value for item in ActionEnum
        ]:
            raise ValueError('Action \'value\' is invalid')

        return lower_characters