from pydantic import BaseModel

class TextData(BaseModel):
    text: str

class StructData(BaseModel):
    data: dict

class AuthMessage(BaseModel):
    email: TextData
    password: TextData

class AuthResponse(BaseModel):
    status: TextData
    usertype: TextData

class RegMessage(BaseModel):
    email: TextData
    password: TextData
    usertype: TextData

class RegResponse(BaseModel):
    status: TextData

class LoadOrgMessage(BaseModel):
    email:TextData

class LoadOrgResponse(BaseModel):
    info: StructData

class DelBookMessage(BaseModel):
    address:TextData
    date_of_book:TextData
    start_date:TextData
    end_date:TextData