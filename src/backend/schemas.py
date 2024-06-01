from pydantic import BaseModel

class TextData(BaseModel):
    text: str

class AuthMessage(BaseModel):
    email: TextData
    password: TextData

class AuthResponse(BaseModel):
    status: TextData
    usertype: TextData
