# BKD-FY
Backend proyecto ferreteria

## Ejecución

> El proyecto se ejecuta con version de Python Los pasos para el despliegue de este proyecto se detallan a continuación:

> - Paso 1: Clonar el repositorio 
>```
> git clone https://github.com/MAB1144-Python/Backend_general.git
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

https://www.deadbear.io/simple-serverless-fastapi-with-aws-lambda/

git remote show origin
git reset HEAD^ --soft
