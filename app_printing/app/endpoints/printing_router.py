from uuid import UUID

import httpx
import prometheus_client
from app.models.printing import Printing, CreatePrintingRequest
from app.services.printing_service import PrintingService
from fastapi import APIRouter, Depends, HTTPException, Response
from starlette.requests import Request
from starlette.responses import RedirectResponse

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(
  TracerProvider(
    resource=Resource.create({SERVICE_NAME: "printing-Service"})
  )
)
jaeger_exporter = JaegerExporter(
  agent_host_name="localhost",
  agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
  BatchSpanProcessor(jaeger_exporter)
)

name='Printing Service'
tracer = trace.get_tracer(name)

printing_router = APIRouter(prefix='/printing', tags=['Printing'])
metrics_router = APIRouter(tags=['Metrics'])

# вынести в отдельный файл
import socket
h_name = socket.gethostname()
IP_addres = socket.gethostbyname(h_name)
print("Host Name is:" + h_name)
print("Computer IP Address is:" + IP_addres)
# --------------------------

host_ip = str(IP_addres)
keycloak_url = f"http://{host_ip}:8080/realms/clothes-delivery"
client_id = "clothes-delivery-client"
client_secret = "TgQ7Ak1AYieq8d9xtDYKpfNsBmsDxUad"
redirect_uri = f"http://{host_ip}:81/api/printing/callback"
userinfo_url = f"http://{host_ip}:8080/realms/clothes-delivery/protocol/openid-connect/userinfo"
keycloak_logout_uri = f"http://{host_ip}:8080/realms/clothes-delivery/protocol/openid-connect/logout"
scope = "openid profile"
user_role = "Not authorized"


@printing_router.get("/login")
def login():
    return request_auth_code()

def request_auth_code():

    auth_url = f"{keycloak_url}/protocol/openid-connect/auth?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"

    print(f"Redirected to: {auth_url}")
    return RedirectResponse(url=auth_url)

async def request_access_token(code: str):

    token_url = f"{keycloak_url}/protocol/openid-connect/token"

    token_data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "code": code,
        "scope": scope
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(token_url, data=token_data)
    return response

async def get_user_role(access_token: str):
    headers = {"Authorization": f"Bearer {access_token}"}

    global user_role

    async with httpx.AsyncClient() as client:
        response = await client.get(userinfo_url, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        print(f"User roles: {json_data}")
        if "admin" in json_data["realm_access"]["roles"]:
            user_role = "admin"
            print(f"Authorized! Your role is:{user_role}")
            return f"Authorized! Your role is:{user_role}"
        elif "customer" in json_data["realm_access"]["roles"]:
            user_role = "customer"
            print(f"Authorized! Your role is:{user_role}")
            return f"Authorized! Your role is: {user_role}"
        return "Not authorized"
    else:
        raise HTTPException(status_code=response.status_code,
                            detail=f"Failed to obtain userinfo with token: {access_token}, "
                                   f"ended up with code{response.status_code}")


@printing_router.get("/callback")
async def callback(request: Request):
    # Получение auth code
    code = request.query_params.get("code")
    print(f"Auth code{code}")
    if code:
        # Получение access token
        response = await request_access_token(code)
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            if access_token:
                try:
                    return await get_user_role(access_token)
                except:
                    raise HTTPException(status_code=response.status_code,
                                        detail=f"Failed to obtain role {response.status_code} {response.json()}")
            else:
                raise HTTPException(status_code=500, detail="Access token not found in the response")
        else:
            raise HTTPException(status_code=response.status_code,
                                detail=f"Failed to obtain access token {response.status_code} {response.json()}")
    else:
        raise HTTPException(status_code=400, detail="Authorization code not found in the query parameters")


@printing_router.get("/logout")
def logout():
    global user_role
    user_role = 'None'
    logout_url = f"{keycloak_logout_uri}"
    return RedirectResponse(url=logout_url)


get_printings_count = prometheus_client.Counter(
    "get_printings_count",
    "Total got all printings"
)

created_printing_count = prometheus_client.Counter(
    "created_printing_count",
    "Total created printings"
)

started_printing_count = prometheus_client.Counter(
    "started_printing_count",
    "Total started printings"
)

completed_printing_count = prometheus_client.Counter(
    "completed_printing_count",
    "Total completed printings"
)

cancelled_printing_count = prometheus_client.Counter(
    "cancelled_printing_count",
    "Total canceled printings"
)


@printing_router.get('/')
def get_printings(printing_service: PrintingService = Depends(PrintingService)) -> list[Printing]:
    with tracer.start_as_current_span("Get printings"):
        try:
            if user_role == "admin":
                print("Permitted action as admin")
                get_printings_count.inc(1)
                return printing_service.get_printings()
        except ValueError:
            raise HTTPException(status_code=403, detail="Permission denied, user must have 'admin' role")



@printing_router.post('/')
def add_printing(
        printing_info: CreatePrintingRequest,
        printing_service: PrintingService = Depends(PrintingService)
) -> Printing:
    with tracer.start_as_current_span("Add printing"):
        try:
            printing = printing_service.create_printing(printing_info.id, printing_info.date)
            created_printing_count.inc(1)
            return printing.dict()
        except KeyError:
            raise HTTPException(400, f'Printing with id={printing_info.id} already exists')


@printing_router.post('/{id}/begin')
def begin_printing(id: UUID, printing_service: PrintingService = Depends(PrintingService)) -> Printing:
    try:
        printing = printing_service.begin_printing(id)
        started_printing_count.inc(1)
        return printing.dict()
    except KeyError:
        raise HTTPException(404, f'Printing with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Printing with id={id} can\'t begin')


@printing_router.post('/{id}/finish')
def finish_printing(id: UUID, printing_service: PrintingService = Depends(PrintingService)) -> Printing:
    try:
        if user_role == "customer" or user_role == "admin":
            try:
                print(f"Permitted action as {user_role}")
                printing = printing_service.finish_printing(id)
                completed_printing_count.inc(1)
                return printing.dict()
            except KeyError:
                raise HTTPException(404, f'Printing with id={id} not found')
            except ValueError:
                raise HTTPException(400, f'Printing with id={id} can\'t be finished')
        else:
            print("Not enough privileges")
    except:
        raise HTTPException(status_code=403, detail="Permission denied, user must have 'admin' role")


@printing_router.post('/{id}/cancel')
def cancel_printing(id: UUID, printing_service: PrintingService = Depends(PrintingService)) -> Printing:
    try:
        printing = printing_service.cancel_printing(id)
        cancelled_printing_count.inc(1)
        return printing.dict()
    except KeyError:
        raise HTTPException(404, f'Printing with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Printing with id={id} can\'t be canceled')


@metrics_router.get('/metrics')
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest()
    )
