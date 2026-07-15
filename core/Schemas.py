from pydantic import BaseModel, field_validator, Field, field_serializer
import re

class BasePersonSchema (BaseModel):
    name: str = Field(..., description = "Enter the student's name")

    @field_validator("name")
    def validate_name(cls, value):
        if len(value) > 33:
            raise ValueError("Name must not exceed 33 characters")
        pattern = r'^[a-zA-Z\s]+$'
        if not bool(re.match(pattern, value)):
            raise ValueError("Name must only contain alphabetic characters and space")
        return value
    
    @field_serializer("name")
    def capitalize_name(self, value: str):
        return value.title()

class PersonCreateSchema (BasePersonSchema):
    pass

class PersonResponseSchema (BasePersonSchema):
    id: int = Field(..., description = "Unique user identifier")

class PersonUpdateSchema (BasePersonSchema):
    pass