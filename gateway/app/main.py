from fastapi import FastAPI, HTTPException, Depends, Request
from uuid import UUID
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
import httpx
from endpoints.auth_router import get_user_role
from endpoints.auth_router import auth_router
from starlette.responses import RedirectResponse
import logging
host_ip = "192.168.1.92"

logging.basicConfig()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key='asas12334sadfdsf')
app.include_router(auth_router)
# Пример конфигурации микросервисов
MICROSERVICES = {
    "order": "http://192.168.1.92:80",
    "promocode": "http://192.168.1.92:81",
}


def proxy_request(service_name: str, path: str, user_info, request: Request):
    url = f"{MICROSERVICES[service_name]}{path}"
    headers = {
        'user': str(user_info)
    }
    print(request.method)
    if request.method == 'GET':
        response = httpx.get(url, headers=headers).json()
    elif request.method == 'POST':
        response = httpx.post(url, headers=headers).json()
    return response

@app.get("/order/")
def read_order(request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:82/auth/login")
    else:
        return proxy_request(service_name="order", path="/order/", user_info=current_user, request=request)  

@app.get("/order/{id}")
def read_order(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:82/auth/login")
    else:
        return proxy_request(service_name="order", path=f"/order/{id}", user_info=current_user, request=request)

@app.post("/promocode/discount")
def set_discount_to_order(code: str, order_id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:82/auth/login")
    else:
        return proxy_request(service_name="promocode", path=f"/promocode/discount?code={code}&id={order_id}&clear=false", user_info=current_user, request=request)