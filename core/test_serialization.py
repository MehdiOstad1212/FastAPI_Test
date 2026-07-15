from pydantic import BaseModel, EmailStr, field_serializer

class User(BaseModel):
    name: str
    email: EmailStr
    account_id: int

    @field_serializer("name")
    def serialize_name(self, value):
        return value.title()

class Model(BaseModel):
    number: float
    @field_serializer("number")
    def serializ_float(self, value):
        return round(value, 5)


user = User(name = "mehdi", email = "Ostad@gmail.com", account_id= "123")

A = user.model_dump()
print (A)

B = user.model_dump_json(indent = 5)
print (B)

C = Model (number = 2/3)
print (C.model_dump())
