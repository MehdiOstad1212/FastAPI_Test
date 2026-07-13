from pydantic import BaseModel,field_validator
import re

class BasePersonSchema (BaseModel):
    name: str

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) > 33:
            raise ValueError("Name must not exceed 33 characters")
        pattern = r'^[a-zA-Z\s]+$'
        if not bool(re.match(pattern, value)):
            raise ValueError("Name must only contain alphabetic characters and space")
        return value

class PersonCreateSchema (BasePersonSchema):
    pass

class PersonResponseSchema (BasePersonSchema):
    id: int

class PersonUpdateSchema (BasePersonSchema):
    pass