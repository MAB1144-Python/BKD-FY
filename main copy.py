from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.route_menu import RouteProductos
from routes.route_login_Gamer import RoutesUserGamer
from routes.route_Login_Bcat import RoutesUserBcat
from routes.route_softest import RoutesUserSoftest
from routes.route_general_test import RoutesGeneralTest
from routes.route_atlas import RoutesUserAtlas
from routes.route_gamificacion import RoutesUserGamificacion
from routes.route_womenfit import RoutesUserWomenfit
from routes.route_conecta import RoutesUserConecta
from routes.route_tio_conejo import RoutesUserTio_Conejo
from routes.route_amazonas import RoutesUserAmazonas
from routes.route_ls import RoutesUserls

app = FastAPI()

app.include_router(RoutesUserGamer)
app.include_router(RoutesUserSoftest)
app.include_router(RoutesUserBcat)
app.include_router(RouteProductos)
app.include_router(RoutesGeneralTest)
app.include_router(RoutesUserAtlas)
app.include_router(RoutesUserGamificacion)
app.include_router(RoutesUserWomenfit)
app.include_router(RoutesUserConecta)
app.include_router(RoutesUserTio_Conejo)
app.include_router(RoutesUserAmazonas)
app.include_router(RoutesUserls)



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
