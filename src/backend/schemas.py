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

class LoadOwnMessage(BaseModel):
    email:TextData

class LoadOwnResponse(BaseModel):
    info:StructData

class ListHallsResponse(BaseModel):
    info:StructData

class HallPageMessage(BaseModel):
    address:TextData

class HallPageResponse(BaseModel):
    capacity: int
    equip: TextData
    description: TextData
    price: int
    image:TextData

class ListReviewsMessage(BaseModel):
    address:TextData

class ListReviewsResponse(BaseModel):
    info:StructData

class ListTimesResponse(BaseModel):
    info:StructData

class AddReviewMessage(BaseModel):
    address:TextData
    revcom:TextData
    resp:TextData

class AddHallMessage(BaseModel):
    email:TextData
    loc:TextData
    capacity:int
    equip:TextData
    desc:TextData
    rent:int
    hall_img:TextData

class AddBookingMessage(BaseModel):
    email:TextData
    loc:TextData
    bkdate:TextData
    startdate:TextData
    enddate:TextData
    status:TextData