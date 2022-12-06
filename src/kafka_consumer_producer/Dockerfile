FROM python:3.9

WORKDIR /code

COPY src/kafka_consumer_producer/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY src/kafka_consumer_producer/predict_consumer1.py /code/predict_consumer1.py
COPY src/svm_model.joblib /code/svm_model.joblib
COPY src/utils.py /code/utils.py

CMD python predict_consumer1.py