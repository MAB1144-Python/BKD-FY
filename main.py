from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.routes_facturacion import  router_factura
from routes.rotes_auth import router_auth

app = FastAPI()

app.include_router(router_factura)
app.include_router(router_auth)

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
