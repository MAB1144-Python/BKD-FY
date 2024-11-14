# BKD-FY
Backend proyecto ferreteria

## Ejecución

> El proyecto se ejecuta con version de Python Los pasos para el despliegue de este proyecto se detallan a continuación:

> - Paso 1: Clonar el repositorio 
>```
> git clone https://github.com/MAB1144-Python/BKD-FY.git
>```
>- Paso 3: Crear el ambiente virtual mediante el comando:
>```
> python3 -m venv venv/
>```
>- Paso 4: Activar el ambiente virtual en linux mediante el comando o (.\venv\Scripts\activate en Windows):
>```
>  source venv/bin/activate
>```
>```
>  .\venv\Scripts\activate
>```
>- Paso 4: Intalar las librerias necesarias mediante el comando:
>```
>  pip install -r requirements.txt
>```
>```
>- Paso 6: Lanzar la aplicación con uvicorn mediante el comando.
>```
>  uvicorn main:app --reload
>```
>- Paso 7: Desde un navegador ir a:
>```
>  http://localhost:8000/docs
>```

## Creación de imagen docker:

>- Paso 2: Construir la imagen
>```
>  
>  docker build -t backend-general .

>- Paso 3: El contenedor se puede ejecutar en local con el comando:
>```
>  docker run -d -p 8225:8225 backend-general
>```
guia base de datos postgres
https://neon.tech/postgresql/postgresql-python/create-tables

https://www.deadbear.io/simple-serverless-fastapi-with-aws-lambda/

git remote show origin
git reset HEAD^ --soft


docker images
docker PS
docker -e PASSWORD_POSTGRES=Mab880821@ postgres
docker exec -it eager_maxwell bash
psql -U postgres --password


docker run -it -e POSTGRES_USER="root" -e POSTGRES_PASSWORD=Mab880821  -d -p 5432:5432  postgres

docker run -d --name my_postgres -e POSTGRES_USER=myuser -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=mydatabase -p 5432:5432 -v pg_data:/var/lib/postgresql/data postgres:latest

## docker-compose up

## docker-compose up --build

Cuales volumenes hay

## docker volume ls

Eliminar todos los volúmenes junto con los contenedores de un docker-compose

##  docker-compose down -v

volumen especifico
## docker volume rm nombre_del_volumen

## docker stop -t 0 postgres_db_Ferroelectricos_Yambitara
## docker stop -t 0 Backend_Ferroelectricos_Yambitara
## docker rm -f postgres_db_Ferroelectricos_Yambitara
## docker rm -f Backend_Ferroelectricos_Yambitara
## docker rmi bkd-fy-app
## docker rmi bkd-fy-db
## docker volume rm db_volumes_Ferroelectricos_Yambitara