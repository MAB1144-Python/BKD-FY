FROM tiangolo/uvicorn-gunicorn:python3.10

# WORKDIR /back-end

# ENV PYTHONUNBUFFERED 1 
# ENV PYTHONPATH "${PYTHONPATH}:/app"


# COPY ./requirements.txt .   

# RUN pip install --no-cache-dir -r requirements.txt

# COPY . /back-end/

# CMD uvicorn --host 0.0.0.0 --port 8225 main:app

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requerimientos y los instala
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia el código de la aplicación al contenedor
COPY app.py .

# Comando de ejecución por defecto
CMD ["python", "app.py"]
