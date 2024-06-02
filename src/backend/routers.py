from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse
import starlette.status as status

from schemas import TextData, AuthMessage, AuthResponse, RegMessage, RegResponse, StructData, LoadOrgMessage, LoadOrgResponse, DelBookMessage, LoadOwnMessage, LoadOwnResponse, ListHallsResponse
from db import DB

router = APIRouter()
executor = DB()

@router.get("/", tags=["Default"])
async def main():
    # Redirect to /docs (relative URL)
    return RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)

path='/api'

@router.post(path + '/auth', tags=["Authorization"], response_model=AuthResponse)
def authentification(auth_message: AuthMessage) -> AuthResponse:

    email, password = auth_message.email.text, auth_message.password.text

    auth_response = executor.authorize(email, password)

    if auth_response in ['org', 'own']:
        return AuthResponse(
            status=TextData(
                text='OK'
            ),
            usertype=TextData(
                text=auth_response
            )
        )
    else:
        return AuthResponse(
            status=TextData(
                text=auth_response
            ),
            usertype=TextData(
                text='None'
            )
        )

@router.post(path + '/reg', tags=["Registration"], response_model=RegResponse)
def registration(auth_message: RegMessage) -> RegResponse:

    email, password, user_type = auth_message.email.text, auth_message.password.text, auth_message.usertype.text

    reg_response = executor.registrate(email, password, user_type)

    if reg_response is "OK":
        return RegResponse(
            status=TextData(
                text=reg_response
            )
        )
    else:
        return RegResponse(
            status=TextData(
                text=reg_response
            )
        )

@router.post(path + '/load_org', tags=["LoadOrg"], response_model=LoadOrgResponse)
def load_org(to_load: LoadOrgMessage) -> LoadOrgResponse:
    raw_info = executor.load_org(to_load.email.text)
    info = {}

    for key in raw_info.keys():
        info[raw_info[key][3]] = [raw_info[key][0], raw_info[key][1], raw_info[key][2], raw_info[key][4]]

    return LoadOrgResponse(
        info=StructData(
            data=info
        )
    )

@router.post(path + '/del_booking', tags=["DeleteBooking"], response_model=RegResponse)
def delete_booking(to_delete:DelBookMessage) -> RegResponse:
    status = executor.delete_booking(to_delete.address.text, to_delete.date_of_book.text,
                                     to_delete.start_date.text, to_delete.end_date.text)

    return RegResponse(
        status=TextData(
            text=status
        )
    )

@router.post(path + '/load_own', tags=["LoadOwn"], response_model=LoadOwnResponse)
def load_own(to_load: LoadOwnMessage) -> LoadOwnResponse:
    info = executor.load_own(to_load.email.text)

    return LoadOwnResponse(
        info=StructData(
            data=info
        )
    )

@router.post(path+'list_halls', tags=["ListHalls"], response_model=ListHallsResponse)
def list_halls() -> ListHallsResponse:
    info = executor.list_halls()

    return ListHallsResponse(
        info=StructData(
            data=info
        )
    )
