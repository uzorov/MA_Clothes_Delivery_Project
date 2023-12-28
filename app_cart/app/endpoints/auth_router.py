from fastapi import APIRouter, Depends
import httpx
from starlette.requests import Request
from starlette.responses import RedirectResponse


host_ip = "172.19.64.1"
keycloak_authorization_url = f"http://{host_ip}:8080/realms/master/protocol/openid-connect/auth"
keycloak_token_url = f"http://{host_ip}:8080/realms/master/protocol/openid-connect/token"
keycloak_user_info_url = f"http://{host_ip}:8080/realms/master/protocol/openid-connect/userinfo"
keycloak_client_id = "order-app"
keycloak_client_secret = "OrnGoUO1UpESwIShI912z4D2wpgZBwcE"
keycloak_redirect_uri = f"http://{host_ip}:80/auth/callback"
keycloak_logout_uri = f"http://{host_ip}:8080/realms/master/protocol/openid-connect/logout"
home_page = f"http://{host_ip}:80/docs"

auth_router = APIRouter(prefix='/auth', tags=['auth'])


def get_user_role(request: Request):
    user_role = request.session.get('user_role')
    code = request.query_params.get("code")
    if not user_role and code:
        token = get_token(code)
        headers = {"Authorization": f"Bearer {token}"}
        roles = httpx.get(keycloak_user_info_url, headers=headers).json()
        if 'Viewer' in roles["realm_access"]["roles"]:
            user_role = "Viewer"
        elif "Customer" in roles["realm_access"]["roles"]:
            user_role = "Customer"
        request.session['user_role'] = user_role
    return user_role

@auth_router.get("/login")
def login():
    authorization_url = (f"{keycloak_authorization_url}?response_type=code&client_id={keycloak_client_id}&scope=openid profile&redirect_uri={keycloak_redirect_uri}")
    return RedirectResponse(url=authorization_url)

@auth_router.get("/logout")
def logout(request: Request):
    request.session['user_role'] = None
    logout_url = (f"{keycloak_logout_uri}")
    return RedirectResponse(url=logout_url)

@auth_router.get("/callback")
def callback(request: Request, user_role: str = Depends(get_user_role)):
    return RedirectResponse(url=home_page)

def get_token(code):
    data = {
            "grant_type": "authorization_code",
            "client_id": keycloak_client_id,
            "client_secret": keycloak_client_secret,
            "code": code,
            "redirect_uri": keycloak_redirect_uri,
            "scope": "openid profile roles",
        }
    response = httpx.post(keycloak_token_url, data=data)
    return response.json()['access_token']
