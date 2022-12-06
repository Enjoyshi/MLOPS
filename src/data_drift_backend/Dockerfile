# Dockerize the application and run it

FROM amd64/python:3.9-buster

WORKDIR /code

COPY src/data_drift_backend/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY src/data_drift_backend/app /code/app
COPY src/svm_model.joblib /code/svm_model.joblib
COPY data/train.csv /code/train.csv

CMD uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 80