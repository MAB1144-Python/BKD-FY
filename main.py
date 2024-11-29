from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.routes_facturacion import  router_factura
from routes.routes_auth import router_auth
from routes.routes_product import router_product
from routes.routes_supplier import router_supplier
from routes.routes_user import router_user

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_user)
app.include_router(router_product)
app.include_router(router_supplier)
app.include_router(router_factura)

origins = [
    #local v1
    "http://localhost:4200",
    "http://localhost:3000",
    "http://localhost:8225",
    "http://127.0.0.1:4200",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
