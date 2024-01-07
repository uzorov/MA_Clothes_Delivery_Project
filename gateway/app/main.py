from fastapi import FastAPI, HTTPException, Depends, Request, Form, APIRouter
from uuid import UUID
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware
import httpx
from endpoints.auth_router import get_user_role
from endpoints.auth_router import auth_router
from starlette.responses import RedirectResponse
from enum import Enum
import logging
host_ip = "192.168.1.92"

logging.basicConfig()

app = FastAPI()
user_router = APIRouter(tags=['user'])
staff_router = APIRouter(prefix='/staff', tags=['staff'])
app.add_middleware(SessionMiddleware, secret_key='asas12334sadfdsf')
app.include_router(auth_router)


# Пример конфигурации микросервисов
MICROSERVICES = {
    "order": "http://192.168.1.92:84/api",
    "promocode": "http://192.168.1.92:85/api",
    "item": "http://192.168.1.92:83/api",
    "cart": "http://192.168.1.92:86/api",
    "printing": "http://192.168.1.92:81/api",
    "payment": "http://192.168.1.92:82/api",
    "delivery": "http://192.168.1.92:80/api"
}

class dropdownChoices(str, Enum):
    xs = "xs"
    s = "s"
    m = "m"
    l = "l"

def proxy_request(service_name: str, path: str, user_info, request: Request):
    url = f"{MICROSERVICES[service_name]}{path}"
    timeout = 20
    headers = {
        'user': str(user_info)
    }
    print(request.method)
    if request.method == 'GET':
        response = httpx.get(url, headers=headers, timeout=timeout).json()
    elif request.method == 'POST':
        response = httpx.post(url, headers=headers, timeout=timeout).json()
    elif request.method == 'PUT':
        response = httpx.put(url, headers=headers).json()
    elif request.method == 'DELETE':
        response = httpx.delete(url, headers=headers).json()
    return response

@user_router.get("/order/")
def read_order(request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="order", path="/order/", user_info=current_user, request=request)  

@user_router.get("/order/{id}")
def read_order(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="order", path=f"/order/{id}", user_info=current_user, request=request)

@user_router.post("/promocode/discount")
def set_discount_to_order(code: str, order_id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="promocode", path=f"/promocode/discount?code={code}&id={order_id}&clear=false", user_info=current_user, request=request)
    

@user_router.get('/item/')
def get_items(request: Request, current_user: dict = Depends(get_user_role)):
    return proxy_request(service_name="item", path=f"/item/", user_info=current_user, request=request)
    
@user_router.get('/item/{id}')
def get_item_by_id(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    return proxy_request(service_name="item", path=f"/item/{id}", user_info=current_user, request=request)

@user_router.post('/item/add_to_cart')
def post_item_to_cart(
    item_id: UUID,
    count: int,
    request: Request,
    size: dropdownChoices = Form(dropdownChoices),
    current_user: dict = Depends(get_user_role)
    ):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="item", path=f"/item/add_to_cart?item_id={item_id}&size={str(size.value)}&count={count}", user_info=current_user, request=request)
    
@user_router.get('/cart/')
def get_cart_by_user_id(request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="cart", path=f"/cart/", user_info=current_user, request=request)
    
@user_router.post('/cart/create_order')
def create_order(request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="cart", path=f"/cart/create_order", user_info=current_user, request=request)
    

@user_router.get('/payment/get-user-payments')
def get_user_payments(request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="payment", path=f"/payments/get-user-payments", user_info=current_user, request=request)
    

@user_router.post('/payment/{id}/process')
def process_payment(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="payment", path=f"/payments/{id}/process", user_info=current_user, request=request)
    

@user_router.get('/delivery/{id}')
def get_delivery_by_id(id:UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="delivery", path=f"/delivery/{id}", user_info=current_user, request=request)

@user_router.post('/delivery/{id}/choose_pickup')
def choose_pickup(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="delivery", path=f"/delivery/{id}/choose_pickup", user_info=current_user, request=request)


@user_router.post('/delivery/{id}/choose_delivery')
def choose_delivery(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="delivery", path=f"/delivery/{id}/choose_delivery", user_info=current_user, request=request)
    
app.include_router(user_router)


@staff_router.get('/printing/all')
def get_printings(request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="printing", path=f"/printing/all", user_info=current_user, request=request)

@staff_router.get('/printing/{id}')
def get_printing_by_id(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="printing", path=f"/printing/{id}", user_info=current_user, request=request)

@staff_router.post('/printing/{id}/begin')
def begin_printing(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="printing", path=f"/printing/{id}/begin", user_info=current_user, request=request)

@staff_router.post('/printing/{id}/finish')
def finish_printing(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="printing", path=f"/printing/{id}/finish", user_info=current_user, request=request)

@staff_router.post('/printing/{id}/cancel')
def cancel_printing(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="printing", path=f"/printing/{id}/cancel", user_info=current_user, request=request)

@staff_router.get('/delivery/all')
def get_deliveries(request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="delivery", path=f"/delivery/all", user_info=current_user, request=request)

@staff_router.get('/delivery/{id}')
def get_delivery_by_id(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="delivery", path=f"/delivery/{id}", user_info=current_user, request=request)

@staff_router.post('/delivery/{id}/activate')
def activate_delivery(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="delivery", path=f"/delivery/{id}/activate", user_info=current_user, request=request)


@staff_router.post('/delivery/{id}/finish')
def finish_delivery(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="delivery", path=f"/delivery/{id}/finish", user_info=current_user, request=request)


@staff_router.post('/delivery/{id}/cancel')
def cancel_delivery(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="delivery", path=f"/delivery/{id}/cancel", user_info=current_user, request=request)


@staff_router.post('/item/')
def create_item(name: str,
        price: float,
        design: str,
        request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="item", path=f"/item?name={name}&price={price}&design={design}", user_info=current_user, request=request)


@staff_router.delete('/item/{id}')
def delete_item(id: UUID, request: Request, current_user: dict = Depends(get_user_role)):
    if current_user['id'] == '':
        request.session['prev_url'] = str(request.url)
        return RedirectResponse(url=f"http://127.0.0.1:8000/auth/login")
    else:
        return proxy_request(service_name="item", path=f"/item/{id}", user_info=current_user, request=request)



app.include_router(staff_router)