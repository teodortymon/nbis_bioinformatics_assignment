FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY ./app /app/app
COPY config.yml /app/