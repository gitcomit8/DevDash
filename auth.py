from fastapi import APIRouter, Request, HTTPException
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from config import GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, BASE_URL

router = APIRouter()

oauth = OAuth()
oauth.register(
    name='github',
    client_id=GITHUB_CLIENT_ID,
    client_secret=GITHUB_CLIENT_SECRET,
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'repo user:email'},
)

@router.get('/login')
async def login(request: Request):
    redirect_uri = BASE_URL + '/auth'
    # Using the registered client directly
    return await oauth.github.authorize_redirect(request, redirect_uri) # type: ignore

@router.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.github.authorize_access_token(request) # type: ignore
    except OAuthError as error:
        raise HTTPException(status_code=400, detail=f'OAuth error: {error}')
    user_data_response = await oauth.github.get('user', token=token) # type: ignore
    user_data = user_data_response.json()
    # Save both user data and the access token in session
    request.session['user'] = user_data
    request.session['github_token'] = token['access_token']
    return RedirectResponse(url='/dashboard')


@router.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')
