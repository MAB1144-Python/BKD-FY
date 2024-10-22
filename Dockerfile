FROM tiangolo/uvicorn-gunicorn:python3.10

WORKDIR /back-end

ENV PYTHONUNBUFFERED 1 
ENV PYTHONPATH "${PYTHONPATH}:/app"


COPY ./requirements.txt .   

RUN pip install --no-cache-dir -r requirements.txt

COPY . /back-end/

CMD uvicorn --host 0.0.0.0 --port 8225 main:app
