# Dockerize the application and run it

FROM python:3.9

WORKDIR /code

COPY src/data_drift_backend/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY src/data_drift_backend/app /code/app

CMD uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 80