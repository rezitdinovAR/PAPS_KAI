from fastapi import APIRouter, Body
from fastapi.responses import RedirectResponse
import starlette.status as status

from schemas import TextData, AuthMessage, AuthResponse
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

