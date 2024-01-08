from fastapi import APIRouter, Depends
import httpx
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
import logging

host_ip = "158.160.14.173"
keycloak_client_id = "gateway"
keycloak_authorization_url = f"http://{host_ip}:8080/realms/master/protocol/openid-connect/auth"
keycloak_token_url = f"http://{host_ip}:8080/realms/master/protocol/openid-connect/token"
keycloak_user_info_url = f"http://{host_ip}:8080/realms/master/protocol/openid-connect/userinfo"
keycloak_client_secret = "rZirLHpuGn1lp4nO8dad5WumKwLhzNbW"
keycloak_redirect_uri = f"https://bbaaj0q6vsmkrjslmt4i.containers.yandexcloud.net/auth/callback"
keycloak_logout_uri = f"http://{host_ip}:8080/realms/master/protocol/openid-connect/logout"

auth_router = APIRouter(prefix='/auth', tags=['auth'])

logging.basicConfig()


def get_user_role(request: Request):
    token = request.session.get('auth_token')
    headers = {"Authorization": f"Bearer {token}"}
    user = {'role': '', 'id': '', 'username': ''}
    try:
        roles = httpx.get(keycloak_user_info_url, headers=headers).json()
        if 'admin' in roles["realm_access"]["roles"]:
            user['role'] = "admin"
        elif "client" in roles["realm_access"]["roles"]:
            user['role'] = "client"
        elif "staff" in roles["realm_access"]["roles"]:
            user['role'] = "staff"
        if roles["sub"]:
            user['id'] = roles["sub"]
        user['username'] = roles['preferred_username']
        return user
    except:
        request.session['id'] = None
        return user


def _get_token(request: Request):
    code = request.query_params.get("code")
    auth_token = request.session.get('auth_token')
    if code:
        auth_token = get_token(code)
        request.session['auth_token'] = auth_token
    return auth_token


@auth_router.get("/login")
def login(request: Request):
    authorization_url = (
        f"{keycloak_authorization_url}?response_type=code&client_id={keycloak_client_id}&scope=openid profile&redirect_uri={keycloak_redirect_uri}")
    return RedirectResponse(url=authorization_url)


@auth_router.get("/logout")
def logout(request: Request):
    request.session['user_role'] = None
    logout_url = (f"{keycloak_logout_uri}")
    return RedirectResponse(url=logout_url)


@auth_router.get("/callback")
def callback(request: Request, token: str = Depends(_get_token)):
    return token
    # RedirectResponse(url=request.session.get('prev_url'))


def get_token(code):
    data = {
        "grant_type": "authorization_code",
        "client_id": keycloak_client_id,
        "client_secret": keycloak_client_secret,
        "code": code,
        "redirect_uri": keycloak_redirect_uri,
        "scope": "openid profile",
    }
    try:
        response = httpx.post(keycloak_token_url, data=data)
        return response.json()['access_token']
    except Exception as e:
        raise Exception(f"An error occurred: {e}")


