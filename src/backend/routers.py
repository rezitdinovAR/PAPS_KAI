from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse
import starlette.status as status

from schemas import TextData, AuthMessage, AuthResponse, RegMessage, RegResponse
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